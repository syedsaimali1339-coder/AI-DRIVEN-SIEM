from kafka import KafkaConsumer
import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime

# =========================
# LOAD THREAT INTELLIGENCE
# =========================
with open("threat_intel.json", "r") as f:
    threat_db = json.load(f)

consumer = KafkaConsumer(
    'security-logs',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='siem-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("🔥 SIEM Consumer Running...")

stream_data = []
alerts = []
blocked_ips = set()

def to_safe_int(x):
    return int(x)

def to_safe_bool(x):
    return bool(x)


# =========================
# COMPLIANCE REPORT FUNCTION (NEW)
# =========================
def generate_compliance_report(alerts, logs):
    report = {
        "generated_at": str(datetime.now()),
        "total_logs": len(logs),
        "total_alerts": len(alerts),
        "critical_alerts": sum(1 for a in alerts if a["severity"] == "CRITICAL"),
        "high_alerts": sum(1 for a in alerts if a["severity"] == "HIGH"),
        "low_alerts": sum(1 for a in alerts if a["severity"] == "LOW"),
        "blocked_ips": len(set(a["ip"] for a in alerts if a["blocked"]))
    }

    with open("compliance_report.json", "w") as f:
        json.dump(report, f, indent=4)


for msg in consumer:

    log = msg.value
    print("RAW:", log)

    if "src_ip" not in log:
        log["src_ip"] = log.get("ip", "UNKNOWN")

    log["failed_logins"] = log.get("failed_logins", 0)
    log["event_count"] = log.get("event_count", 0)

    stream_data.append(log)

    df = pd.DataFrame(stream_data)

    # =========================
    # AI ANOMALY DETECTION
    # =========================
    X = df[["failed_logins", "event_count"]]

    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    model.fit(X)

    df["anomaly"] = model.predict(X)

    # =========================
    # UEBA
    # =========================
    ueba = df.groupby("src_ip").agg({
        "failed_logins": "mean",
        "event_count": "mean"
    }).reset_index()

    ueba_model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    ueba_model.fit(
        ueba[["failed_logins", "event_count"]]
    )

    ueba["ueba_anomaly"] = ueba_model.predict(
        ueba[["failed_logins", "event_count"]]
    )

    # =========================
    # LATEST EVENT
    # =========================
    latest = df.iloc[-1]

    ip = latest["src_ip"]

    anomaly = bool(latest["anomaly"] == -1)

    user = ueba[ueba["src_ip"] == ip]

    ueba_flag = (
        bool(user["ueba_anomaly"].values[0] == -1)
        if len(user) > 0
        else False
    )

    # =========================
    # THREAT INTELLIGENCE
    # =========================
    threat_match = ip in threat_db

    threat_actor = threat_db.get(ip, "None")

    # =========================
    # DYNAMIC RULE GENERATION
    # =========================

    avg_failed_logins = df["failed_logins"].mean()
    dynamic_threshold = avg_failed_logins * 2

    dynamic_rule = (
        latest["failed_logins"] > dynamic_threshold
    )

    attack_signature = "NORMAL"

    if dynamic_rule:
        attack_signature = "DYNAMIC_BRUTE_FORCE_PATTERN"

    # =========================
    # RISK ENGINE
    # =========================
    risk = int(latest["failed_logins"] * 2)

    if anomaly:
        risk += 30

    if ueba_flag:
        risk += 40

    if threat_match:
        risk += 50

    if dynamic_rule:
        risk += 20

    # =========================
    # SEVERITY
    # =========================
    if risk > 80:
        severity = "CRITICAL"
    elif risk > 40:
        severity = "HIGH"
    else:
        severity = "LOW"

    # =========================
    # SOAR
    # =========================
    action = "MONITOR"

    if risk > 60:
        action = "BLOCK_IP"
        blocked_ips.add(ip)

    elif risk > 40:
        action = "RATE_LIMIT"

    # =========================
    # ALERT
    # =========================
    alert = {
        "ip": str(ip),
        "risk": to_safe_int(risk),
        "severity": severity,
        "ueba": to_safe_bool(ueba_flag),
        "anomaly": to_safe_bool(anomaly),
        "threat_match": to_safe_bool(threat_match),
        "threat_actor": threat_actor,
        "dynamic_rule": to_safe_bool(dynamic_rule),
        "attack_signature": attack_signature,
        "action": action,
        "blocked": action == "BLOCK_IP"
    }

    alerts.append(alert)

    print("🚨 ALERT:", alert)

    # =========================
    # SAVE ALERTS
    # =========================
    with open("alerts.json", "w") as f:
        json.dump(alerts, f, indent=4)

    # =========================
    # COMPLIANCE AUTO GENERATION (NEW)
    # =========================
    generate_compliance_report(alerts, stream_data)
