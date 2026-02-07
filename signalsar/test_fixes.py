#!/usr/bin/env python3
"""Test script to verify regulator-hardening fixes"""

import sqlite3
import json
from app import TYPOLOGIES, calculate_risk_score, get_mock_txn_history

print("=" * 60)
print("REGULATOR-HARDENING PATCH VERIFICATION")
print("=" * 60)

# Test 1: Typology truncation fix
print("\n1. Testing typology truncation fix...")
customer_id = 'CUST-8821'
txn_history = get_mock_txn_history(customer_id)
risk_score, reasons, evidence_map, typology = calculate_risk_score(customer_id, txn_history)
print(f"   Typology returned: '{typology}'")
print(f"   Length: {len(typology)} characters")
if len(typology) > 3:
    print("   ✓ PASS: Full typology string returned (not truncated)")
else:
    print("   ✗ FAIL: Typology appears truncated")

# Test 2: NEW TYPOLOGY mapping
print("\n2. Testing NEW TYPOLOGY mapping...")
customer_id = 'CUST-4455'
txn_history = get_mock_txn_history(customer_id)
risk_score, reasons, evidence_map, typology = calculate_risk_score(customer_id, txn_history)
print(f"   Typology for CUST-4455: '{typology}'")
if typology in TYPOLOGIES:
    print(f"   ✓ PASS: Typology '{typology}' is valid enum code")
else:
    print(f"   ✗ FAIL: Typology '{typology}' not in TYPOLOGIES enum")

# Test 3: Database foreign keys
print("\n3. Testing database foreign keys...")
conn = sqlite3.connect('signalsar.db')
c = conn.cursor()
c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='cases'")
cases_schema = c.fetchone()[0]
if 'FOREIGN KEY' in cases_schema:
    print("   ✓ PASS: Foreign keys present in cases table")
else:
    print("   ✗ FAIL: Foreign keys missing in cases table")

# Test 4: Unique indexes on submissions
print("\n4. Testing unique indexes on submissions...")
c.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='submissions'")
indexes = [row[0] for row in c.fetchall()]
if 'idx_submissions_submission_id' in indexes and 'idx_submissions_checksum' in indexes:
    print("   ✓ PASS: Unique indexes on submission_id and checksum")
else:
    print("   ✗ FAIL: Missing unique indexes")
    print(f"   Found indexes: {indexes}")

# Test 5: Append-only triggers
print("\n5. Testing append-only triggers...")
c.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
triggers = [row[0] for row in c.fetchall()]
expected_triggers = [
    'prevent_audit_log_update',
    'prevent_audit_log_delete',
    'prevent_submissions_update',
    'prevent_submissions_delete'
]
if all(t in triggers for t in expected_triggers):
    print("   ✓ PASS: All append-only triggers present")
else:
    print("   ✗ FAIL: Missing triggers")
    print(f"   Expected: {expected_triggers}")
    print(f"   Found: {triggers}")

# Test 6: Evidence validation
print("\n6. Testing evidence_ids validation...")
c.execute("SELECT * FROM reason_evidence LIMIT 1")
re = c.fetchone()
if re:
    evidence_ids = json.loads(re[4])  # evidence_ids column
    print(f"   Sample evidence_ids: {evidence_ids}")
    if evidence_ids and len(evidence_ids) > 0:
        print("   ✓ PASS: Evidence IDs are non-empty")
    else:
        print("   ✗ FAIL: Evidence IDs are empty")
else:
    print("   ⚠ SKIP: No reason_evidence records to test")

conn.close()

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
