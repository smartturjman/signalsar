# SignalSAR - AI-Powered Transaction Monitoring & Financial Crime Detection

## Overview
SignalSAR is a hackathon MVP demonstrating end-to-end AI-powered SAR (Suspicious Activity Report) generation for financial institutions.

## Architecture

### Data Flow
1. **Alert Ingestion**: Transaction monitoring → Webhook → Alert queue
2. **Data Enrichment**: Customer profile + 90-day transaction history + documents
3. **AI Processing**: Risk scoring + narrative generation + compliance checking
4. **Human Review**: Analyst review → Edit/approve → Submit
5. **Submission**: Regulatory portal (mock) + audit log + compliance manifest

### Risk Scoring Engine
Hybrid scoring model (0-100):
- **Rule Score**: Rapid deposit→trade→withdrawal patterns, tiny profit laundering
- **Behavior Score**: Velocity spikes, deviation from baseline
- **Network Score**: Shared IP/device/card links
- **Output**: Final score + top 3 reason codes

### Compliance Checker
- Validates SAR field completeness
- Returns compliance score percentage
- Flags missing required fields

### Audit System
- Logs every analyst action (view, edit, submit)
- Immutable audit trail with timestamps
- Analyst attribution

## Features

### 1. Alert Queue Page
- Risk-sorted table (highest first)
- Status filters (open/investigating/closed)
- Priority badges (critical/high/medium/low)
- NEW TYPOLOGY badge for unknown patterns
- One-click investigation
- **KPI Dashboard**: Alert reduction, SAR generation time, false positive reduction

### 2. Case Detail Page
- Customer profile panel
- 90-day transaction timeline
- Risk analysis with reason codes
- **Evidence Sources Section**:
  - Trading behavior summary
  - Network links (shared IPs, device fingerprints, linked accounts)
  - Device/IP logs
  - KYC snapshot
- Linked entities and evidence
- Activity audit trail
- **Adaptive threshold display** (learning from feedback)
- **Real-time intervention**: Hold Withdrawal button for high-risk cases
- **Analyst feedback**: Mark True/False Positive buttons

### 3. SAR Draft Page
- AI-generated narrative with evidence references
- Compliance score indicator
- Editable text area
- **Analyst feedback buttons**
- Save draft / Submit actions
- Evidence summary panel

### 4. Analyst Feedback Learning Loop
- Mark cases as True Positive or False Positive
- Adaptive threshold adjustment per alert type
- System learns from analyst decisions:
  - High false positives → Increase threshold (reduce alerts)
  - High true positives → Decrease threshold (catch more)
- Threshold adjustments visible in UI

### 5. Real-Time Intervention
- "Hold Withdrawal" action for high-risk cases (score ≥70)
- Immediate account freeze capability
- Intervention logged in audit trail
- Case status updated to "intervened"

### 6. Evidence Pack
- Comprehensive evidence collection:
  - Transaction timeline with full history
  - Trading behavior metrics
  - Network correlation analysis
  - Device and IP logs
  - KYC profile snapshot
- SAR narratives reference evidence sources
- Plain-language explanations

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Vanilla JavaScript + HTML/CSS
- **API**: RESTful JSON endpoints

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation & Run

```bash
# Navigate to project directory
cd signalsar

# Install dependencies
pip install -r requirements.txt

# Initialize database with mock data
python init_db.py

# Start the server
python app.py
```

The application will be available at: **http://localhost:5000**

## Demo Flow (3 minutes)

1. **Alert Queue** (30s)
   - Show KPI dashboard (2,000→50 alerts, 90sec generation, 67% FP reduction)
   - Show risk-sorted alerts with NEW TYPOLOGY badge
   - Click "Investigate" on alert #2 (NEW TYPOLOGY, score 89)

2. **Case Detail** (90s)
   - Review Unknown Pattern Discovery explanation
   - Show adaptive threshold (if any)
   - Examine Evidence Sources:
     - Trading behavior: 47 micro-transactions
     - Network links: 8 linked accounts, shared IPs
     - Device logs
   - Click "🛑 Hold Withdrawal" → Confirm intervention
   - Click "✓ Mark True Positive" → Record feedback
   - View updated audit trail

3. **SAR Draft** (60s)
   - Show AI-generated narrative with evidence references
   - Point out compliance score (100%)
   - Demonstrate editable narrative
   - Click "Submit to Regulatory Portal"
   - Show submission confirmation with ID

4. **Audit Log** (30s)
   - Navigate to Audit Log page
   - Show complete action trail:
     - case_created
     - intervention_executed
     - feedback_submitted
     - sar_submitted

## Full Test Flow

Run automated tests:
```bash
cd signalsar
./test_features.sh
```

Manual UI test flow:
1. Open http://127.0.0.1:5000
2. Alert Queue → Click "Investigate" on high-risk alert
3. Case Detail → Click "Hold Withdrawal" → Confirm
4. Case Detail → Click "Mark True Positive"
5. Case Detail → Click "View SAR Draft"
6. SAR Draft → Edit narrative → Click "Submit"
7. Navigate to Audit Log → Verify all actions logged

Expected results:
- ✓ Intervention executed and logged
- ✓ Feedback recorded and adaptive threshold updated
- ✓ SAR submitted with unique ID
- ✓ All actions in audit trail
- ✓ Case status updated to "submitted"
- ✓ Alert status updated to "closed"

## API Endpoints

### Alerts
- `GET /api/alerts?status=open` - List alerts
- `POST /api/alerts` - Create alert (webhook endpoint)
- `POST /api/alerts/{id}/investigate` - Start investigation

### Cases
- `GET /api/cases/{id}` - Get case details with evidence pack
- `PUT /api/cases/{id}/sar` - Update SAR draft
- `POST /api/cases/{id}/submit` - Submit SAR
- `POST /api/cases/{id}/feedback` - Submit analyst feedback (true_positive/false_positive)
- `POST /api/cases/{id}/intervene` - Execute intervention (hold_withdrawal)

### Audit
- `GET /api/audit` - Get audit log

## New API Endpoints

### Analyst Feedback
```bash
curl -X POST http://127.0.0.1:5000/api/cases/1/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "label": "true_positive",
    "analyst": "analyst@signalsar.com"
  }'
```

### Real-Time Intervention
```bash
curl -X POST http://127.0.0.1:5000/api/cases/1/intervene \
  -H "Content-Type: application/json" \
  -d '{
    "action": "hold_withdrawal",
    "reason": "High-risk activity detected",
    "analyst": "analyst@signalsar.com"
  }'
```

## Webhook Example

```bash
curl -X POST http://localhost:5000/api/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST-9999",
    "alert_type": "High Velocity",
    "risk_score": 85
  }'
```

## Mock Data
The system uses mock data for:
- Customer profiles (CRM simulation)
- Transaction history (90-day window, or 3-day for NEW TYPOLOGY)
- Document metadata
- Device fingerprints and IP logs
- Network correlation data

All mock data generators are in `app.py` and can be replaced with real API calls by modifying:
- `get_mock_customer_data()` → Call real CRM API
- `get_mock_txn_history()` → Call real transaction database

## Database Schema

### Core Tables
- `alerts` - Transaction monitoring alerts
- `cases` - Investigation cases with enriched data
- `submissions` - Submitted SARs
- `audit_log` - Complete action trail

### New Tables (Challenge Features)
- `analyst_feedback` - True/False positive labels
- `interventions` - Real-time actions (hold_withdrawal, etc.)
- `adaptive_thresholds` - Learning-based threshold adjustments per alert type

## Challenge Alignment

### 1. Analyst Feedback Learning Loop ✅
- Mark True/False Positive on Case Detail and SAR pages
- Feedback stored in `analyst_feedback` table
- Adaptive logic adjusts thresholds:
  - High FP rate → +5 threshold (reduce alerts)
  - High TP rate → -5 threshold (catch more)
- Current threshold displayed as badge in UI
- System learns from last 10 feedback entries per alert type

### 2. Real-Time Intervention Action ✅
- "Hold Withdrawal" button on high-risk cases (score ≥70)
- Intervention stored in `interventions` table
- Case/alert status updated to "intervened"
- Action logged in audit trail with analyst attribution
- Confirmation dialog prevents accidental execution

### 3. Stronger Evidence Pack ✅
- Explicit "Evidence Sources" section on Case Detail:
  - Transaction timeline (full history)
  - Trading behavior summary (counts, volumes)
  - Network links (shared IPs, device fingerprints, linked accounts)
  - KYC profile snapshot
  - Device/IP logs with timestamps and locations
- SAR narratives reference evidence in plain language
- Evidence data included in API response (`evidence_pack` field)

## Production Considerations

To make this production-ready:
1. Replace SQLite with PostgreSQL
2. Add authentication/authorization
3. Integrate real LLM API (OpenAI/Anthropic) for narrative generation
4. Connect to actual CRM and transaction databases
5. Implement real regulatory submission API
6. Add encryption for sensitive data
7. Implement proper error handling and logging
8. Add unit and integration tests
9. Deploy with proper WSGI server (Gunicorn/uWSGI)
10. Add monitoring and alerting

## License
MIT (Hackathon MVP)
