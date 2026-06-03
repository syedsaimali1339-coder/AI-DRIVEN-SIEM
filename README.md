# AI-Driven SIEM with Real-Time Threat Detection, UEBA, Threat Intelligence, and SOAR Automation

## Project Overview

This project is an AI-powered Security Information and Event Management (SIEM) system that provides real-time threat detection, behavioral analytics, threat intelligence correlation, and automated incident response using machine learning and stream processing.

The system simulates a modern SOC (Security Operations Center) pipeline using:

* Apache Kafka for real-time log streaming
* Machine Learning (Isolation Forest) for anomaly detection
* UEBA (User and Entity Behavior Analytics)
* Threat Intelligence integration (IOC matching)
* Dynamic Rule Generation (adaptive detection logic)
* Risk-based alerting engine
* SOAR automation (security response actions)
* Flask-based real-time dashboard

---

## Key Features

## 1. Real-Time Security Monitoring (Kafka Streaming)

The system uses Apache Kafka to simulate real-time ingestion of security logs.

* Producer generates continuous security events
* Consumer processes logs instantly
* Enables high-speed threat detection pipeline

---

## 2. AI-Based Threat Detection

Machine learning is used to detect abnormal behavior in security logs.

### Model Used:

* Isolation Forest (unsupervised anomaly detection)

### Features analyzed:

* Failed login attempts
* Event count

The model identifies suspicious activity without needing labeled attack data.

---

## 3. UEBA (User and Entity Behavior Analytics)

The system builds behavioral profiles per IP address.

It detects deviations such as:

* Unusual login attempts
* Abnormal event spikes
* Behavioral anomalies per user/entity

This enhances detection beyond simple rule-based systems.

---

## 4. Threat Intelligence Integration

The SIEM integrates a local Threat Intelligence database:

```json
threat_intel.json
```

### Functionality:

* Matches incoming IPs against known malicious indicators (IOCs)
* Identifies threat actors (e.g., APT groups)
* Enhances risk scoring when a match is found

### Example Threat Intelligence Data:

| IP Address  | Threat Actor |
| ----------- | ------------ |
| 45.12.34.56 | APT28        |
| 103.12.5.10 | APT29        |

### Impact:

* Known malicious IPs are immediately flagged
* Increases confidence in detection accuracy

---

## 5. Dynamic Rule Generation (NEW)

The system automatically generates detection rules based on real-time behavior.

### How it works:

* The system calculates the average failed login attempts from streaming data

* It builds a dynamic threshold:

  ```
  dynamic_threshold = average_failed_logins × 2
  ```

* If an event exceeds this threshold:

  * A dynamic rule is triggered
  * A new attack signature is generated

### Example:

* Normal behavior: 2–5 failed logins
* Dynamic threshold adapts automatically
* If a user exceeds learned baseline → flagged as anomaly

### Generated Signature Example:

* `DYNAMIC_BRUTE_FORCE_PATTERN`

### Benefits:

* Eliminates static rule dependency
* Adapts to evolving attack patterns
* Reduces false positives
* Mimics real SOC behavior

---

## 6. Risk Scoring Engine

Each event is assigned a dynamic risk score based on:

* Failed login attempts
* ML anomaly detection
* UEBA anomalies
* Threat intelligence matches
* Dynamic rule triggers

### Risk Formula:

* Base risk from failed logins
* +30 if ML anomaly detected
* +40 if UEBA anomaly detected
* +50 if threat intelligence match
* +20 if dynamic rule triggered

---

## 7. Alert Severity Classification

Alerts are categorized into:

| Severity | Description            |
| -------- | ---------------------- |
| LOW      | Normal activity        |
| HIGH     | Suspicious activity    |
| CRITICAL | Severe threat detected |

---

## 8. SOAR Automation (Response Engine)

Based on risk score, automated responses are triggered:

| Risk Level | Action     |
| ---------- | ---------- |
| Low        | Monitor    |
| Medium     | Rate Limit |
| High       | Block IP   |

### Actions include:

* IP blocking
* Rate limiting
* Monitoring only

---

## 9. Real-Time Dashboard

A Flask-based dashboard displays live security events.

### Features:

* Live event updates (every 2 seconds)
* Severity classification
* Threat intelligence correlation
* Dynamic rule status
* Risk score visualization
* SOAR action tracking

---

## Project Architecture

```
Kafka Producer
     ↓
Apache Kafka Topic
     ↓
Kafka Consumer
     ↓
┌──────────────────────────────┐
│ AI Detection (Isolation Forest) │
│ UEBA Analysis                 │
│ Threat Intelligence Match     │
│ Dynamic Rule Generation       │
│ Risk Scoring Engine           │
│ SOAR Automation              │
└──────────────────────────────┘
     ↓
alerts.json
     ↓
Flask Dashboard
```

---

## Technologies Used

* Python
* Flask
* Apache Kafka
* Scikit-learn
* Pandas
* HTML, CSS, JavaScript
* JSON

---

## Files Description

### app.py

Flask backend serving API and dashboard.

### producer.py

Simulates real-time security log generation.

### consumer.py

Core SIEM engine:

* ML detection
* UEBA
* Threat intelligence
* Dynamic rule generation
* Risk scoring
* SOAR automation

### dashboard.html

Real-time visualization dashboard.

### alerts.json

Stores generated alerts for UI display.

### threat_intel.json

Contains known malicious IPs and threat actors.

### evidence.txt

Sample security event dataset for testing.

### compliance_report.txt

Basic audit and compliance output.

---

## Industry Relevance

This system simulates enterprise-level security environments used in:

* Security Operations Centers (SOC)
* Managed Security Service Providers (MSSP)
* Government cyber defense systems
* Enterprise threat monitoring platforms

---

## Open Source Tools Used

* SIEM: Custom Flask-based system
* ML: scikit-learn (Isolation Forest)
* Streaming: Apache Kafka
* Visualization: Custom dashboard
* Threat Intelligence: JSON-based IOC database

---

## Conclusion

This project demonstrates a full modern SIEM pipeline integrating:

* Real-time streaming security analytics
* Machine learning-based anomaly detection
* Behavioral analytics (UEBA)
* Threat intelligence correlation
* Dynamic rule generation
* Automated incident response (SOAR)

The system provides adaptive, intelligent, and automated cybersecurity monitoring similar to enterprise SOC platforms.


