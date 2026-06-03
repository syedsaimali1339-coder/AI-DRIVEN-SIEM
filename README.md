# AI-Driven SIEM with Real-Time Monitoring, UEBA, Threat Intelligence, and SOAR

## Project Overview

This project is an AI-Driven Security Information and Event Management (SIEM) system designed to detect, analyze, and respond to cybersecurity threats in real time.

The system combines:

* Real-Time Log Monitoring using Apache Kafka
* Artificial Intelligence (Isolation Forest)
* User and Entity Behavior Analytics (UEBA)
* Threat Intelligence Correlation
* Risk-Based Alerting
* SOAR (Security Orchestration, Automation and Response)
* Interactive Web Dashboard

The goal is to improve threat detection accuracy and automate incident response compared to traditional SIEM solutions.

---

## Key Features

### Real-Time Monitoring

Apache Kafka is used to simulate a real-time log collection environment.

A Kafka Producer continuously generates security events and sends them to a Kafka topic.

A Kafka Consumer receives these events in real time and processes them immediately for threat detection and response.

---

### AI-Powered Threat Detection

The system uses the Isolation Forest Machine Learning algorithm from Scikit-Learn.

The model analyzes security metrics such as:

* Failed Login Attempts
* Event Count

The algorithm automatically identifies abnormal behavior and flags suspicious activities without requiring labeled attack data.

---

### User and Entity Behavior Analytics (UEBA)

UEBA is used to identify unusual user or device behavior.

The system learns normal activity patterns for each source IP address and detects deviations from established baselines.

Examples include:

* Excessive login failures
* Unusual event volumes
* Abnormal user activity

UEBA provides an additional layer of detection beyond traditional rule-based monitoring.

---

### Threat Intelligence Integration

The SIEM integrates Threat Intelligence to identify known malicious infrastructure.

A local Threat Intelligence database is maintained in:

```json
threat_intel.json
```

Example Threat Intelligence Data:

```json
{
  "45.12.34.56": "APT28",
  "103.12.5.10": "APT29"
}
```

Whenever a security event is received, the source IP address is automatically checked against the Threat Intelligence database.

If a match is found:

* The event is marked as a Threat Intelligence Match.
* The associated threat actor is identified.
* Additional risk points are added.
* The attack is classified as a Known Malicious IP.
* Automated response actions may be triggered.

Examples:

| Malicious IP | Threat Actor |
| ------------ | ------------ |
| 45.12.34.56  | APT28        |
| 103.12.5.10  | APT29        |

This process is known as Indicator of Compromise (IOC) Correlation.

Threat Intelligence enables the SIEM to detect known threats even when behavioral anomalies are not present.

---

### Risk Scoring Engine

Each event is assigned a dynamic risk score.

The score is calculated using:

* Failed Login Attempts
* AI Anomaly Detection Results
* UEBA Detection Results
* Threat Intelligence Matches

Example Logic:

* Failed Logins contribute to the base score.
* AI anomalies increase risk.
* UEBA anomalies increase risk.
* Threat Intelligence matches increase risk.

This approach allows the system to prioritize the most dangerous threats.

---

### Alert Severity Classification

Based on the calculated risk score, alerts are categorized into:

| Severity | Description                                 |
| -------- | ------------------------------------------- |
| LOW      | Minimal threat activity                     |
| HIGH     | Suspicious activity requiring investigation |
| CRITICAL | Immediate security threat                   |

This helps analysts focus on the most important incidents first.

---

### SOAR Automation

The project includes Security Orchestration, Automation and Response (SOAR) capabilities.

Based on the calculated risk score, the system automatically performs response actions.

Possible actions include:

| Risk Level | Action     |
| ---------- | ---------- |
| Low        | Monitor    |
| Medium     | Rate Limit |
| High       | Block IP   |

Automated response reduces analyst workload and accelerates incident containment.

---

## Dashboard Features

The web dashboard provides real-time visibility into security events.

Displayed information includes:

* Source IP Address
* Incident Severity
* Threat Risk Score
* Threat Classification
* Threat Intelligence Correlation
* Threat Attribution
* Behavioral Analytics Status
* AI Detection Status
* Automated Response Actions
* Containment Status

Dashboard statistics include:

* Total Security Events
* Critical Alerts
* High-Risk Alerts
* Low-Risk Alerts

All alerts are automatically updated in real time.

---

## Project Architecture

```text
Security Logs
      │
      ▼
Kafka Producer
      │
      ▼
Apache Kafka
      │
      ▼
Kafka Consumer
      │
      ├── AI Detection (Isolation Forest)
      ├── UEBA Analysis
      ├── Threat Intelligence Correlation
      ├── Risk Scoring
      └── SOAR Automation
      │
      ▼
alerts.json
      │
      ▼
Flask Dashboard
```

---

## Technologies Used

* Python
* Flask
* Apache Kafka
* Scikit-Learn
* Pandas
* HTML
* CSS
* JavaScript
* JSON

---

## Files Description

### app.py

Flask application that serves the dashboard and provides API access to security alerts.

### producer.py

Generates simulated security logs and streams them to Apache Kafka.

### consumer.py

Processes incoming logs, performs AI detection, UEBA analysis, Threat Intelligence correlation, risk scoring, and automated response actions.

### dashboard.html

Interactive web dashboard used to visualize security events and alerts.

### alerts.json

Stores generated alerts for dashboard visualization.

### threat_intel.json

Threat Intelligence database containing known malicious IP addresses and associated threat actors.

### users.json

Sample user account data used for authentication simulation.

### evidence.txt

Sample security event evidence used for testing and validation.

### compliance_report.txt

Generated compliance and audit reporting information.

---

## Conclusion

This project demonstrates how Artificial Intelligence, Threat Intelligence, UEBA, SOAR, and Real-Time Monitoring can be integrated into a modern SIEM platform.

The solution provides proactive threat detection, automated incident response, behavioral analytics, and threat intelligence correlation, helping security teams identify and respond to cyber threats more efficiently.

