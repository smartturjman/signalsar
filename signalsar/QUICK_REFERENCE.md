# SignalSAR - Quick Reference

## 🚀 Start Application
```bash
cd signalsar
source venv/bin/activate
python3 app.py
```
Open: http://127.0.0.1:5000

## 🧪 Run Tests
```bash
./test_features.sh
```

## 📋 Challenge Features

### 1️⃣ Analyst Feedback Learning Loop
**Where:** Case Detail page, SAR Draft page
**Actions:**
- Click "✓ Mark True Positive"
- Click "✗ Mark False Positive"
**Result:** Adaptive threshold adjusts automatically (visible as badge)

### 2️⃣ Real-Time Intervention
**Where:** Case Detail page (high-risk cases only)
**Action:** Click "🛑 Hold Withdrawal"
**Result:** Account frozen, status updated to "intervened"

### 3️⃣ Evidence Pack
**Where:** Case Detail page → "Evidence Sources" section
**Contains:**
- 📊 Trading Behavior Summary
- 🌐 Network Links
- 📱 Device/IP Logs

## 🎯 Demo Flow (3 min)

1. **Alert Queue** (30s)
   - View KPI dashboard
   - Click "Investigate" on NEW TYPOLOGY alert

2. **Case Detail** (90s)
   - Review Evidence Sources
   - Click "Hold Withdrawal" → Confirm
   - Click "Mark True Positive"

3. **SAR Draft** (60s)
   - Review AI narrative
   - Click "Submit to Regulatory Portal"

4. **Audit Log** (30s)
   - View complete action trail

## 🔌 New API Endpoints

### Submit Feedback
```bash
POST /api/cases/{id}/feedback
Body: {"label": "true_positive", "analyst": "analyst@signalsar.com"}
```

### Execute Intervention
```bash
POST /api/cases/{id}/intervene
Body: {"action": "hold_withdrawal", "reason": "High risk", "analyst": "analyst@signalsar.com"}
```

### Get Case with Evidence
```bash
GET /api/cases/{id}
Returns: case, alert, enriched_data, evidence_pack, adaptive_threshold, interventions
```

## 📊 Database Tables

**Core:**
- alerts, cases, submissions, audit_log

**New:**
- analyst_feedback
- interventions
- adaptive_thresholds

## 🎨 UI Components

**Alert Queue:**
- KPI cards (alert reduction, SAR time, FP reduction)
- NEW TYPOLOGY badge

**Case Detail:**
- Evidence Sources section
- Adaptive threshold badge
- Hold Withdrawal button
- Mark TP/FP buttons

**SAR Draft:**
- Mark TP/FP buttons
- Evidence-referenced narrative

## ✅ Verification Checklist

- [ ] Alert Queue loads with 6 alerts
- [ ] KPI dashboard shows metrics
- [ ] NEW TYPOLOGY badge visible on alert #2
- [ ] Investigation creates case with evidence pack
- [ ] Hold Withdrawal button appears on high-risk cases
- [ ] Intervention executes and updates status
- [ ] Feedback buttons work on Case Detail and SAR pages
- [ ] Adaptive threshold displays after feedback
- [ ] SAR submission generates unique ID
- [ ] Audit log shows all actions

## 🐛 Troubleshooting

**API not responding:**
```bash
pkill -f "python3 app.py"
cd signalsar && source venv/bin/activate && python3 app.py
```

**Database issues:**
```bash
rm signalsar.db
python3 init_db.py
```

**UI not updating:**
- Hard refresh: `Cmd+Shift+R` (macOS) or `Ctrl+Shift+R` (Windows)

## 📁 Project Structure
```
signalsar/
├── app.py                    # Flask backend
├── init_db.py               # Database setup
├── requirements.txt         # Dependencies
├── test_features.sh         # Automated tests
├── README.md                # Full documentation
├── CHALLENGE_FEATURES.md    # Feature summary
├── QUICK_REFERENCE.md       # This file
└── static/
    ├── index.html          # Alert Queue
    ├── case.html           # Case Detail
    ├── sar.html            # SAR Draft
    ├── audit.html          # Audit Log
    └── styles.css          # Styling
```
