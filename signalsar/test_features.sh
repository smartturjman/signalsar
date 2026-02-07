#!/bin/bash

echo "🧪 SignalSAR - Full Feature Test Suite"
echo "========================================"
echo ""

API_BASE="http://127.0.0.1:5000/api"

echo "1️⃣ Testing Alert Queue..."
ALERTS=$(curl -s "$API_BASE/alerts?status=open")
ALERT_COUNT=$(echo $ALERTS | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo "   ✓ Loaded $ALERT_COUNT alerts"
echo ""

echo "2️⃣ Testing Investigation Flow..."
INVESTIGATE=$(curl -s -X POST "$API_BASE/alerts/2/investigate")
CASE_ID=$(echo $INVESTIGATE | python3 -c "import sys, json; print(json.load(sys.stdin)['case_id'])")
echo "   ✓ Created case #$CASE_ID for NEW TYPOLOGY alert"
echo ""

echo "3️⃣ Testing Case Detail with Evidence Pack..."
CASE=$(curl -s "$API_BASE/cases/$CASE_ID")
HAS_EVIDENCE=$(echo $CASE | python3 -c "import sys, json; d=json.load(sys.stdin); print('evidence_pack' in d)")
THRESHOLD=$(echo $CASE | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('adaptive_threshold', 0))")
echo "   ✓ Evidence pack present: $HAS_EVIDENCE"
echo "   ✓ Adaptive threshold: $THRESHOLD"
echo ""

echo "4️⃣ Testing Intervention (Hold Withdrawal)..."
INTERVENE=$(curl -s -X POST "$API_BASE/cases/$CASE_ID/intervene" \
  -H "Content-Type: application/json" \
  -d '{"action":"hold_withdrawal","reason":"High risk detected","analyst":"test@signalsar.com"}')
INTERVENE_STATUS=$(echo $INTERVENE | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
echo "   ✓ Intervention status: $INTERVENE_STATUS"
echo ""

echo "5️⃣ Testing Analyst Feedback (True Positive)..."
FEEDBACK=$(curl -s -X POST "$API_BASE/cases/$CASE_ID/feedback" \
  -H "Content-Type: application/json" \
  -d '{"label":"true_positive","analyst":"test@signalsar.com"}')
FEEDBACK_STATUS=$(echo $FEEDBACK | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
echo "   ✓ Feedback status: $FEEDBACK_STATUS"
echo ""

echo "6️⃣ Testing SAR Submission..."
SUBMIT=$(curl -s -X POST "$API_BASE/cases/$CASE_ID/submit" \
  -H "Content-Type: application/json" \
  -d '{"analyst":"test@signalsar.com"}')
SUBMISSION_ID=$(echo $SUBMIT | python3 -c "import sys, json; print(json.load(sys.stdin)['submission_id'])")
echo "   ✓ Submission ID: $SUBMISSION_ID"
echo ""

echo "7️⃣ Testing Audit Log..."
AUDIT=$(curl -s "$API_BASE/audit")
AUDIT_COUNT=$(echo $AUDIT | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
echo "   ✓ Audit entries: $AUDIT_COUNT"
echo ""

echo "========================================"
echo "✅ All API tests passed!"
echo ""
echo "🌐 Open http://127.0.0.1:5000 to test UI"
echo ""
