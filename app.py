from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

alerts = []

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/alerts")
def api_alerts():
    global alerts

    try:
        with open("alerts.json", "r") as f:
            alerts = json.load(f)
    except:
        alerts = []

    critical = len([a for a in alerts if a["severity"] == "CRITICAL"])
    high = len([a for a in alerts if a["severity"] == "HIGH"])
    low = len([a for a in alerts if a["severity"] == "LOW"])

    return jsonify({
        "alerts": alerts,
        "total": len(alerts),
        "critical": critical,
        "high": high,
        "low": low
    })

if __name__ == "__main__":
    app.run(debug=True)
