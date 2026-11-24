# 🛡️ NetShield

### Machine Learning-Based Network Security Analytics System

NetShield is a full-stack network security analytics
project that demonstrates network flow analysis,
machine learning classification, feature validation,
database management and interactive visualization.

## Features

- Network flow feature extraction
- Random Forest classification
- CIC-IDS2017 dataset preprocessing
- Dataset cleaning and validation
- CICFlowMeter feature compatibility testing
- SQLite database integration
- FastAPI REST API
- Interactive React dashboard
- Classification visualization
- Searchable analysis records
- CSV report export
- Offline synthetic traffic analysis

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js, CSS, Vite |
| Backend | Python, FastAPI |
| Database | SQLite |
| Machine Learning | Scikit-learn |
| Algorithm | Random Forest |
| Packet Analysis | Scapy |
| Visualization | Recharts |
| Icons | Lucide React |
| Dataset | CIC-IDS2017 |

## System Architecture

Offline Synthetic Data
        ↓
Network Flow Feature Extraction
        ↓
Random Forest Classification
        ↓
SQLite Database
        ↓
FastAPI REST API
        ↓
React Dashboard

## Machine Learning Performance

| Metric | Result |
|---|---:|
| Accuracy | 99.95% |
| Precision | 99.97% |
| Recall | 99.94% |
| F1 Score | 99.96% |
| Cleaned Dataset Records | 209,306 |
| Input Features | 9 |

These metrics were obtained using a random held-out
dataset split and do not establish independent
real-world detection performance.

## Feature Compatibility Validation

NetShield's feature extraction was compared against
CICFlowMeter using synthetic offline PCAP files.

| Metric | Result |
|---|---:|
| Extended Test Cases | 6 |
| Network Flows | 7 |
| Feature Values Checked | 63 |
| Passed | 61 |
| Failed | 0 |
| Undefined Rates | 2 |
| Comparable Feature Agreement | 100% |

## Dashboard Modules

1. Overview
2. Traffic Analysis
3. Network Flows
4. ML Predictions
5. Security Alerts
6. Model Performance
7. Feature Validation
8. Reports
9. Settings

## Installation

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the backend from the project root:

```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Start the frontend in a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

The offline demonstration requires the locally trained
model and generated synthetic feature files.

## Project Limitations

- Currently operates as an offline analytics demonstration.
- Model classifications are not confirmed security incidents.
- Real-world detection performance requires further validation.
- Repeated analysis runs create additional database records.
- Zero-duration flow rates are mathematically undefined.

## Future Enhancements

- Independent dataset evaluation
- Improved model generalization
- Automated testing
- Enhanced reporting
- User authentication
- Containerized deployment

## Educational Purpose

NetShield was developed as an educational cybersecurity,
machine learning and full-stack development project.

---

Built using Python, Machine Learning, FastAPI and React.