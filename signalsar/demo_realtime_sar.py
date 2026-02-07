#!/usr/bin/env python3
"""
Demo: Real-Time SAR Generation
Shows how quickly the system generates a complete SAR narrative
"""

import time
from app import (
    get_mock_customer_data, 
    get_mock_txn_history, 
    calculate_risk_score,
    generate_sar_narrative,
    check_compliance
)

print("=" * 70)
print("REAL-TIME SAR GENERATION DEMO")
print("=" * 70)
print()

# Simulate analyst clicking "Investigate" on alert
customer_id = 'CUST-4455'  # NEW TYPOLOGY case
print(f"📋 Investigating Alert: {customer_id}")
print()

# Start timer
start_time = time.time()

# Step 1: Data Enrichment
print("⏳ Step 1: Data Enrichment...")
step1_start = time.time()
customer_data = get_mock_customer_data(customer_id)
txn_history = get_mock_txn_history(customer_id)
step1_time = (time.time() - step1_start) * 1000
print(f"   ✓ Fetched customer profile: {customer_data['name']}")
print(f"   ✓ Retrieved {len(txn_history)} transactions")
print(f"   ⚡ Time: {step1_time:.2f}ms")
print()

# Step 2: Risk Scoring
print("⏳ Step 2: Risk Scoring Engine...")
step2_start = time.time()
risk_score, reasons, evidence_map, typology = calculate_risk_score(customer_id, txn_history)
step2_time = (time.time() - step2_start) * 1000
print(f"   ✓ Risk Score: {risk_score}")
print(f"   ✓ Typology: {typology}")
print(f"   ✓ Reasons: {len(reasons)} detected")
print(f"   ✓ Evidence: {len(evidence_map)} reason codes linked")
print(f"   ⚡ Time: {step2_time:.2f}ms")
print()

# Step 3: Evidence Linking
print("⏳ Step 3: Evidence Linking...")
step3_start = time.time()
total_evidence = sum(len(v['evidence_ids']) for v in evidence_map.values())
step3_time = (time.time() - step3_start) * 1000
print(f"   ✓ Linked {total_evidence} evidence items")
for reason_code, data in evidence_map.items():
    print(f"   • {reason_code}: {len(data['evidence_ids'])} items")
print(f"   ⚡ Time: {step3_time:.2f}ms")
print()

# Step 4: SAR Narrative Generation
print("⏳ Step 4: SAR Narrative Generation...")
step4_start = time.time()
risk_analysis = {
    'score': risk_score,
    'reasons': reasons,
    'evidence_map': evidence_map,
    'velocity_multiplier': 3.2
}
sar_draft = generate_sar_narrative(customer_data, txn_history, risk_analysis)
step4_time = (time.time() - step4_start) * 1000
print(f"   ✓ Generated {len(sar_draft)} character narrative")
print(f"   ✓ Includes evidence references: {sar_draft.count('[Evidence:')} citations")
print(f"   ⚡ Time: {step4_time:.2f}ms")
print()

# Step 5: Compliance Check
print("⏳ Step 5: Compliance Check...")
step5_start = time.time()
enriched_data = {
    'customer_data': customer_data,
    'txn_history': txn_history,
    'risk_analysis': risk_analysis
}
compliance_score, missing_fields, required_fields = check_compliance(sar_draft, enriched_data, risk_analysis)
step5_time = (time.time() - step5_start) * 1000
print(f"   ✓ Compliance Score: {compliance_score}%")
print(f"   ✓ Required Fields: {len(required_fields)}")
print(f"   ✓ Missing Fields: {len(missing_fields)}")
print(f"   ⚡ Time: {step5_time:.2f}ms")
print()

# Total time
total_time = (time.time() - start_time) * 1000

print("=" * 70)
print("✅ SAR DRAFT READY FOR ANALYST REVIEW")
print("=" * 70)
print()
print(f"⚡ TOTAL TIME: {total_time:.2f}ms ({total_time/1000:.3f} seconds)")
print()
print("📊 Performance Breakdown:")
print(f"   • Data Enrichment:      {step1_time:6.2f}ms ({step1_time/total_time*100:5.1f}%)")
print(f"   • Risk Scoring:         {step2_time:6.2f}ms ({step2_time/total_time*100:5.1f}%)")
print(f"   • Evidence Linking:     {step3_time:6.2f}ms ({step3_time/total_time*100:5.1f}%)")
print(f"   • Narrative Generation: {step4_time:6.2f}ms ({step4_time/total_time*100:5.1f}%)")
print(f"   • Compliance Check:     {step5_time:6.2f}ms ({step5_time/total_time*100:5.1f}%)")
print()

print("=" * 70)
print("SAR NARRATIVE PREVIEW (First 500 characters)")
print("=" * 70)
print()
print(sar_draft[:500] + "...")
print()

print("=" * 70)
print("💡 This is what happens when you click 'Investigate' on an alert!")
print("   The entire SAR is generated in REAL-TIME, ready for review.")
print("=" * 70)
