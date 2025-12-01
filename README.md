### NimbusGuard - Autonomous Self-Healing Network Platform

NimbusGuard is an AI powered autonomous self healing network infrastructure platform that monitors network devices, analyzes performance metrics, detects anomalies, predicts failures and automatically executes remediation actions.

Think of NimbusGuard as a Smart Doctor for Networks - continuously monitoring, diagnosing and healing network issues before they turn into outages.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 1. Table of Contents
-	Overview￼Key Features￼
*	Architecture￼
+	Tech Stack￼
-	Project Structure￼
*	Getting Started￼
+	Setup Instructions￼
-	Backend Setup￼
*	Database Setup￼
+	AI Engine Setup￼
-	Frontend Setup￼
*	Use Cases￼
+	12-Week Roadmap￼
-	Contributing￼	

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 2. Overview
NimbusGuard is designed for organizations that lack expensive enterprise monitoring tools — such as NGO offices, schools, clinics, community centers and small businesses.

It delivers:
	-	Continuous network monitoring
	*	AI-based anomaly detection
	+	Failure prediction
	-	Autonomous remediation
	*	Clean dashboard visualization

Provides a predictive, self-healing network system that dramatically reduces downtime and manual troubleshooting.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 3. Key Features
1. Data Collection Layer
	-	SNMP polling
	-	Syslog/API ingestion
	-	Cloud metrics (AWS/GCP)

2. Data Storage Layer
	-	Time series metrics in TimescaleDB
	*	Device inventory, alerts & configs in PostgreSQL
	+	Real-time cache in Redis

3. Intelligence Layer (AI/ML)
	-	Baseline learning
	*	Z-score anomaly detection
	+	Trend-based failure prediction
	-	Basic root-cause analysis

4. Automation Layer
	-	Playbook-driven remediation
	*	Safe automatic fixes
	+	Manual approval workflow

5. Dashboard Layer
	-	Real-time device overview
	*	Alerts & predictions
	+	Device details
	-	System health metrics

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 4. Architecture
<img width="291" height="431" alt="image" src="https://github.com/user-attachments/assets/45a3c06b-db4d-4b1d-a0d3-156bb834d8bf" />

## Tech Stack
1. Backend
	-	Python
	*	FastAPI
	+	SQLAlchemy
	-	APScheduler

2. AI/ML
	-	Python
	*	Pandas, Numpy
	+	Statistical anomaly detection

3. Frontend
	-	React
	*	Tailwind CSS

4. Databases
	-	TimescaleDB (metrics)
	*	PostgreSQL (inventory & alerts)
	+	Redis (cache)

5. Infrastructure
	-	Docker
	*	docker-compose

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 5. Project Structure
<img width="339" height="508" alt="Screenshot 2025-11-28 at 8 11 50 PM" src="https://github.com/user-attachments/assets/def29729-60dd-43d0-b4ec-cc97f6569769" />

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 6. Getting Started
Prerequisites
	-	Python 3.9+
	*	Node.js 18+
	+	Docker Desktop
	-	Git

## Clone the repository:
	git clone https://github.com/AshokKumarReddyNaguri24/nimbusguard.git
	cd nimbusguard

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Setup Instructions
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 7. Backend Setup
	cd backend
	python -m venv venv
	source venv/bin/activate   # Windows: venv\Scripts\activate
	pip install -r requirements.txt
	uvicorn app.main:app --reload

Visit: 
http://localhost:8000/healthcheck

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 8. Database Setup
	cd database
	docker-compose up -d

This starts:
	-	TimescaleDB
	*	PostgreSQL
	+	Redis

Check containers:
docker ps

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 9. AI Engine Setup
	cd ai-engine
	python baseline_model.py

This module powers:
	-	baseline learning
	*	anomaly detection
	+	prediction

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 10. Frontend Setup
	cd frontend/nimbusguard-ui
	npm install
	npm start

Visit:
http://localhost:3000

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 11. Use Cases
- Detect high CPU/memory usage
* Predict device failures
+ Automatically restart stuck services
- Block malicious IPs
* Visualize performance over time
+ Group alerts into incidents

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 12. 12-Week Roadmap

- Phase 1 – Foundation
	-	Repo, folder structure
	*	Backend skeleton
	+	AI skeleton
	-	UI skeleton
	*	Dockerized databases

- Phase 2 – Data Collection
	-	SNMP poller
	*	Metrics ingestion
	+	Device inventory APIs

- Phase 3 – AI Baseline & Anomaly Detection
	-	Baseline training
	*	Z-score anomaly detection
	+	Alert generation

- Phase 4 - Automation
	-	Playbooks
	*	Rule engine
	+	Safe execution

- Phase 5 - Dashboard
	-	Global overview
	*	Device details
	+	Alerts & predictions

- Phase 6 - Integration & Demo
	-	E2E integration
	*	Load testing
	+	Documentation
	-	Final MVP demo

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 13. Contributing
	1.	Fork the repository
	2.	Create a feature branch
	3.	Commit with clear messages
	4.	Submit a pull request

Please review our CONTRIBUTING.md before starting.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Contact
- Project Lead:
Ashok Kumar Reddy Naguri
* For questions or volunteer contributions, please reach out.
