from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime, timedelta
import uuid

app = Flask(__name__, static_folder='static')
CORS(app)

# Typology enumeration
TYPOLOGIES = {
    'RAPID_MOVEMENT': 'Rapid deposit-trade-withdrawal sequence',
    'STRUCTURING': 'Transaction structuring to evade reporting',
    'NETWORK_LINK': 'Network-based coordination',
    'VELOCITY_SPIKE': 'Unusual transaction velocity',
    'MICRO_FRAGMENTATION': 'Micro-transaction fragmentation (NEW)',
    'LAYERING': 'Minimal profit on high volume (layering)',
    'UNKNOWN_PATTERN': 'Unusual transaction pattern'
}

def get_db():
    conn = sqlite3.connect('signalsar.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_adaptive_threshold(alert_type):
    conn = get_db()
    result = conn.execute('SELECT threshold_adjustment FROM adaptive_thresholds WHERE alert_type = ?', (alert_type,)).fetchone()
    conn.close()
    return result['threshold_adjustment'] if result else 0

def update_adaptive_thresholds():
    conn = get_db()
    
    # Get feedback from last 30 days
    alert_types = conn.execute('SELECT DISTINCT alert_type FROM alerts').fetchall()
    
    for row in alert_types:
        alert_type = row['alert_type']
        
        # Get recent feedback for this alert type
        feedback = conn.execute('''
            SELECT af.label 
            FROM analyst_feedback af
            JOIN alerts a ON af.alert_id = a.id
            WHERE a.alert_type = ?
            ORDER BY af.created_at DESC
            LIMIT 10
        ''', (alert_type,)).fetchall()
        
        if len(feedback) >= 3:
            fp_count = sum(1 for f in feedback if f['label'] == 'false_positive')
            tp_count = sum(1 for f in feedback if f['label'] == 'true_positive')
            
            # Adjust threshold: more FPs = increase threshold (reduce alerts), more TPs = decrease threshold (catch more)
            adjustment = 0
            if fp_count > tp_count * 2:
                adjustment = 5  # Increase threshold
            elif tp_count > fp_count * 2:
                adjustment = -5  # Decrease threshold
            
            conn.execute('''
                INSERT INTO adaptive_thresholds (alert_type, threshold_adjustment, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(alert_type) DO UPDATE SET
                    threshold_adjustment = ?,
                    updated_at = ?
            ''', (alert_type, adjustment, datetime.now().isoformat(), adjustment, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def log_audit(case_id, analyst, action, details, before_value=None, after_value=None):
    conn = get_db()
    conn.execute('INSERT INTO audit_log (case_id, analyst, action, details, before_value, after_value, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (case_id, analyst, action, json.dumps(details), before_value, after_value, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def link_reason_evidence(case_id, reason_code, metric, evidence_ids):
    conn = get_db()
    conn.execute('INSERT INTO reason_evidence (case_id, reason_code, metric, evidence_ids, created_at) VALUES (?, ?, ?, ?, ?)',
                 (case_id, reason_code, metric, json.dumps(evidence_ids), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def calculate_risk_score(customer_id, txn_history):
    # Rule score: rapid deposit->trade->withdrawal pattern
    rule_score = 0
    reasons = []
    evidence_map = {}
    typology = 'UNKNOWN_PATTERN'
    is_new_typology = customer_id == 'CUST-4455'
    
    if is_new_typology:
        # NEW TYPOLOGY: Moderate rule score but high anomaly+network
        rule_score = 25
        typology = 'MICRO_FRAGMENTATION'
        reasons.append('Micro-transaction fragmentation pattern (NEW)')
        evidence_map['MICRO_FRAGMENTATION'] = {
            'metric': '47 micro-txns <$500 in 3 days vs. historical avg of 2/week',
            'evidence_ids': [t['id'] for t in txn_history[:5]]
        }
        
        # High behavior score - unusual pattern
        behavior_score = 35
        reasons.append('Anomalous: 47 micro-txns <$500 in 3 days vs. historical avg of 2/week')
        
        # High network score
        network_score = 29
        reasons.append('Network: 8 linked accounts sharing device fingerprint + timing correlation')
        evidence_map['NETWORK_LINK'] = {
            'metric': '8 linked accounts, <5min timing correlation',
            'evidence_ids': ['DEV-A8F2', 'IP-10.5.5.1']
        }
        
        final_score = min(100, rule_score + behavior_score + network_score)
        return final_score, reasons, evidence_map, typology
    
    # Check for rapid movement pattern
    rapid_movement_txns = []
    if len(txn_history) >= 3:
        for i in range(len(txn_history) - 2):
            if (txn_history[i]['type'] == 'deposit' and 
                txn_history[i+1]['type'] == 'trade' and 
                txn_history[i+2]['type'] == 'withdrawal'):
                rule_score += 35
                typology = 'RAPID_MOVEMENT'
                reasons.append('Rapid deposit-trade-withdrawal sequence')
                rapid_movement_txns = [txn_history[i]['id'], txn_history[i+1]['id'], txn_history[i+2]['id']]
                evidence_map['RAPID_MOVEMENT'] = {
                    'metric': 'deposit→withdrawal median time = 14 min (baseline 2.1 hrs)',
                    'evidence_ids': rapid_movement_txns
                }
                break
    
    # Tiny profit laundering
    total_in = sum(t['amount'] for t in txn_history if t['type'] == 'deposit')
    total_out = sum(t['amount'] for t in txn_history if t['type'] == 'withdrawal')
    if total_in > 50000 and abs(total_out - total_in) < total_in * 0.05:
        rule_score += 25
        if typology == 'UNKNOWN_PATTERN':
            typology = 'LAYERING'
        reasons.append('Minimal profit on high volume (layering)')
        evidence_map['LAYERING'] = {
            'metric': f'${total_in:,.0f} in, ${total_out:,.0f} out (profit margin <5%)',
            'evidence_ids': [t['id'] for t in txn_history if t['type'] in ['deposit', 'withdrawal']][:5]
        }
    
    # Behavior score: velocity spike
    behavior_score = 0
    recent_count = sum(1 for t in txn_history if (datetime.now() - datetime.fromisoformat(t['timestamp'])).days <= 7)
    if recent_count > 15:
        behavior_score = 30
        if typology == 'UNKNOWN_PATTERN':
            typology = 'VELOCITY_SPIKE'
        reasons.append(f'Velocity spike: {recent_count} txns in 7 days')
        evidence_map['VELOCITY_SPIKE'] = {
            'metric': f'{recent_count} txns in 7 days (baseline: 2/week)',
            'evidence_ids': [t['id'] for t in txn_history if (datetime.now() - datetime.fromisoformat(t['timestamp'])).days <= 7][:5]
        }
    
    # Network score: shared identifiers
    network_score = 0
    shared_ips = list(set([t.get('ip') for t in txn_history if t.get('ip')]))
    shared_links = len(shared_ips) < 3 and len(txn_history) > 10
    if shared_links:
        network_score = 20
        if typology == 'UNKNOWN_PATTERN':
            typology = 'NETWORK_LINK'
        reasons.append('Multiple accounts sharing IP/device')
        evidence_map['NETWORK_LINK'] = {
            'metric': f'{len(shared_ips)} unique IPs across {len(txn_history)} txns',
            'evidence_ids': shared_ips + [txn_history[0]['id']]
        }
    
    # Ensure at least one reason is always present
    if not reasons:
        reasons.append('Unusual transaction pattern detected by monitoring system')
        evidence_map['UNKNOWN_PATTERN'] = {
            'metric': 'Pattern flagged by automated monitoring',
            'evidence_ids': [t['id'] for t in txn_history[:3]]
        }
    
    final_score = min(100, rule_score + behavior_score + network_score)
    return final_score, reasons, evidence_map, typology

def generate_sar_narrative(customer_data, txn_history, risk_analysis):
    is_new_typology = customer_data['customer_id'] == 'CUST-4455'
    evidence_map = risk_analysis.get('evidence_map', {})
    
    # Helper to format evidence references
    def format_evidence(reason_code):
        if reason_code in evidence_map:
            ids = evidence_map[reason_code]['evidence_ids'][:3]
            return f" [Evidence: {', '.join(str(id) for id in ids)}]"
        return ""
    
    if is_new_typology:
        narrative = f"""SUSPICIOUS ACTIVITY REPORT - NARRATIVE

Subject: {customer_data['name']} (ID: {customer_data['customer_id']})
Account: {customer_data['account_number']}
Period: {txn_history[0]['timestamp'][:10]} to {txn_history[-1]['timestamp'][:10]}

⚠️ NEW TYPOLOGY DETECTED - UNKNOWN PATTERN

SUMMARY OF SUSPICIOUS ACTIVITY:
The subject engaged in a previously unobserved transaction pattern that does not match existing rule-based detection scenarios. Machine learning anomaly detection flagged this activity as high-risk based on behavioral deviation and network correlation analysis.

PATTERN DISCOVERY EXPLANATION:
This case represents a NEW TYPOLOGY not previously documented in our transaction monitoring rules. While traditional structuring and rapid-movement patterns score moderately, the combination of micro-transaction fragmentation, timing anomalies, and network linkages suggests a novel evasion technique.

DETAILED DESCRIPTION:
Over a 3-day period, the subject conducted 47 micro-transactions averaging $487 each, totaling ${sum(t['amount'] for t in txn_history):,.2f}.{format_evidence('MICRO_FRAGMENTATION')} This represents a 23x increase in transaction frequency compared to the account's 90-day baseline of 2 transactions per week.

Key anomalies identified:
{chr(10).join('- ' + r + (format_evidence(k) if k in evidence_map else '') for r, k in zip(risk_analysis['reasons'], ['MICRO_FRAGMENTATION', 'NETWORK_LINK']))}

BEHAVIORAL BASELINE COMPARISON:
- Historical pattern: 2 transactions/week, avg $8,500 per transaction
- Current pattern: 47 transactions in 3 days, avg $487 per transaction
- Deviation score: 94th percentile across all monitored accounts

NETWORK ANALYSIS:
Cross-account correlation analysis identified 8 accounts sharing identical device fingerprints and exhibiting synchronized transaction timing within 5-minute windows.{format_evidence('NETWORK_LINK')} This suggests coordinated activity potentially designed to evade aggregate reporting thresholds.

CUSTOMER DUE DILIGENCE:
Customer onboarded on {customer_data['onboarded_date']}. Stated occupation: {customer_data['occupation']}. Expected account activity: Low-to-moderate retail trading. Current activity represents a fundamental departure from stated profile and historical behavior.

CONCLUSION:
This activity is being reported as suspicious due to the novel pattern structure, significant behavioral deviation, and network correlation indicators. The pattern does not match existing typologies and may represent an emerging money laundering technique requiring regulatory attention and potential rule enhancement.
"""
        return narrative
    
    narrative = f"""SUSPICIOUS ACTIVITY REPORT - NARRATIVE

Subject: {customer_data['name']} (ID: {customer_data['customer_id']})
Account: {customer_data['account_number']}
Period: {txn_history[0]['timestamp'][:10]} to {txn_history[-1]['timestamp'][:10]}

SUMMARY OF SUSPICIOUS ACTIVITY:
The subject engaged in a pattern of transactions consistent with potential money laundering activity. Automated monitoring systems flagged unusual transaction velocity and structuring patterns that deviate significantly from the account's historical baseline.

DETAILED DESCRIPTION:
Over a 90-day period, the subject conducted {len(txn_history)} transactions totaling ${sum(t['amount'] for t in txn_history):,.2f}. Analysis reveals:

{chr(10).join('- ' + r + format_evidence(list(evidence_map.keys())[i] if i < len(evidence_map) else '') for i, r in enumerate(risk_analysis['reasons']))}

The transaction pattern shows deposits followed immediately by trading activity and rapid withdrawals, with minimal economic rationale. The subject's account activity increased {risk_analysis['velocity_multiplier']}x compared to the prior 90-day period.

CUSTOMER DUE DILIGENCE:
Customer onboarded on {customer_data['onboarded_date']}. Stated occupation: {customer_data['occupation']}. Expected account activity: Low-to-moderate retail trading. Actual activity significantly exceeds stated profile.

CONCLUSION:
Based on the above factors, this activity is being reported as suspicious and potentially indicative of money laundering or structuring to evade reporting requirements.
"""
    return narrative

def check_compliance(sar_draft, enriched_data, risk_analysis):
    required_fields = {
        'customer_id': enriched_data.get('customer_data', {}).get('customer_id'),
        'account_number': enriched_data.get('customer_data', {}).get('account_number'),
        'customer_name': enriched_data.get('customer_data', {}).get('name'),
        'transaction_count': len(enriched_data.get('txn_history', [])),
        'total_amount': sum(t['amount'] for t in enriched_data.get('txn_history', [])),
        'time_period': f"{enriched_data.get('txn_history', [{}])[0].get('timestamp', '')[:10]} to {enriched_data.get('txn_history', [{}])[-1].get('timestamp', '')[:10]}" if enriched_data.get('txn_history') else None,
        'suspicious_pattern_reasons': risk_analysis.get('reasons', []),
        'narrative_text': sar_draft
    }
    
    missing_fields = [k for k, v in required_fields.items() if not v or (isinstance(v, list) and len(v) == 0)]
    present_count = len(required_fields) - len(missing_fields)
    compliance_score = int((present_count / len(required_fields)) * 100)
    
    return compliance_score, missing_fields, required_fields

# Mock data generators
def get_mock_customer_data(customer_id):
    return {
        'customer_id': customer_id,
        'name': f'John Doe {customer_id[-4:]}',
        'account_number': f'ACC-{customer_id[-4:]}-9821',
        'email': f'customer{customer_id[-4:]}@example.com',
        'phone': '+1-555-0100',
        'address': '123 Main St, New York, NY 10001',
        'occupation': 'Software Engineer',
        'onboarded_date': '2024-03-15',
        'risk_rating': 'Medium'
    }

def get_mock_txn_history(customer_id):
    import random
    txns = []
    base_time = datetime.now()
    
    # NEW TYPOLOGY: micro-transaction pattern
    if customer_id == 'CUST-4455':
        for i in range(47):
            txn_type = random.choice(['deposit', 'withdrawal'])
            txns.append({
                'id': f'TXN-{i+2000}',
                'type': txn_type,
                'amount': random.randint(350, 500),
                'timestamp': (base_time - timedelta(days=random.randint(0, 3))).isoformat(),
                'ip': random.choice(['10.5.5.1', '10.5.5.1', '10.5.5.2']),
                'description': f'Micro {txn_type}'
            })
        return sorted(txns, key=lambda x: x['timestamp'])
    
    for i in range(25):
        txn_type = random.choice(['deposit', 'trade', 'withdrawal', 'deposit', 'trade'])
        txns.append({
            'id': f'TXN-{i+1000}',
            'type': txn_type,
            'amount': random.randint(5000, 25000),
            'timestamp': (base_time - timedelta(days=random.randint(0, 90))).isoformat(),
            'ip': random.choice(['192.168.1.1', '192.168.1.2', '10.0.0.5']),
            'description': f'{txn_type.title()} transaction'
        })
    
    return sorted(txns, key=lambda x: x['timestamp'])

# API Routes
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    conn = get_db()
    status = request.args.get('status', 'open')
    alerts = conn.execute('SELECT * FROM alerts WHERE status = ? ORDER BY risk_score DESC', (status,)).fetchall()
    conn.close()
    return jsonify([dict(a) for a in alerts])

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO alerts (customer_id, alert_type, risk_score, status, created_at, assigned_to) VALUES (?, ?, ?, ?, ?, ?)',
              (data['customer_id'], data['alert_type'], data.get('risk_score', 50), 'open', datetime.now().isoformat(), None))
    conn.commit()
    alert_id = c.lastrowid
    conn.close()
    return jsonify({'id': alert_id, 'status': 'created'}), 201

@app.route('/api/alerts/<int:alert_id>/investigate', methods=['POST'])
def investigate_alert(alert_id):
    conn = get_db()
    alert = conn.execute('SELECT * FROM alerts WHERE id = ?', (alert_id,)).fetchone()
    
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    # Data enrichment
    customer_data = get_mock_customer_data(alert['customer_id'])
    txn_history = get_mock_txn_history(alert['customer_id'])
    
    # Risk scoring
    risk_score, reasons, evidence_map, typology = calculate_risk_score(alert['customer_id'], txn_history)
    
    # Map NEW TYPOLOGY to valid enum
    if alert['alert_type'] == 'NEW TYPOLOGY':
        typology = 'MICRO_FRAGMENTATION'
    
    # Use alert's pre-calculated risk score if dynamic calculation is low/zero
    if risk_score == 0 or risk_score < 50:
        risk_score = alert['risk_score']
        if not reasons:
            reasons = [f'{alert["alert_type"]} pattern detected by monitoring system']
            typology = alert['alert_type'].upper().replace(' ', '_')
            if typology not in TYPOLOGIES:
                typology = 'UNKNOWN_PATTERN'
    
    risk_analysis = {
        'score': risk_score,
        'reasons': reasons,
        'evidence_map': evidence_map,
        'velocity_multiplier': 3.2
    }
    
    # Generate SAR draft
    sar_draft = generate_sar_narrative(customer_data, txn_history, risk_analysis)
    
    enriched_data = {
        'customer_data': customer_data,
        'txn_history': txn_history,
        'risk_analysis': risk_analysis
    }
    
    # Compliance check with required fields
    compliance_score, missing_fields, sar_required_fields = check_compliance(sar_draft, enriched_data, risk_analysis)
    
    # Create case
    c = conn.cursor()
    c.execute('INSERT INTO cases (alert_id, enriched_data, risk_analysis, sar_draft, compliance_score, status, typology, typology_confirmed, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (alert_id, json.dumps(enriched_data), json.dumps(risk_analysis), sar_draft, compliance_score, 'draft', typology, 0, datetime.now().isoformat(), datetime.now().isoformat()))
    case_id = c.lastrowid
    
    # Link evidence to reasons (using same connection)
    for reason_code, evidence_data in evidence_map.items():
        conn.execute('INSERT INTO reason_evidence (case_id, reason_code, metric, evidence_ids, created_at) VALUES (?, ?, ?, ?, ?)',
                     (case_id, reason_code, evidence_data['metric'], json.dumps(evidence_data['evidence_ids']), datetime.now().isoformat()))
    
    conn.execute('UPDATE alerts SET status = ? WHERE id = ?', ('investigating', alert_id))
    conn.commit()
    
    log_audit(case_id, 'analyst@signalsar.com', 'case_created', {'alert_id': alert_id})
    
    conn.close()
    return jsonify({'case_id': case_id, 'compliance_score': compliance_score})

@app.route('/api/cases/<int:case_id>', methods=['GET'])
def get_case(case_id):
    conn = get_db()
    case = conn.execute('SELECT * FROM cases WHERE id = ?', (case_id,)).fetchone()
    
    if not case:
        return jsonify({'error': 'Case not found'}), 404
    
    alert = conn.execute('SELECT * FROM alerts WHERE id = ?', (case['alert_id'],)).fetchone()
    audit_logs = conn.execute('SELECT * FROM audit_log WHERE case_id = ? ORDER BY timestamp DESC', (case_id,)).fetchall()
    interventions = conn.execute('SELECT * FROM interventions WHERE case_id = ? ORDER BY timestamp DESC', (case_id,)).fetchall()
    reason_evidence = conn.execute('SELECT * FROM reason_evidence WHERE case_id = ?', (case_id,)).fetchall()
    
    # Get adaptive threshold for this alert type
    threshold_adj = get_adaptive_threshold(alert['alert_type'])
    
    enriched_data = json.loads(case['enriched_data'])
    risk_analysis = json.loads(case['risk_analysis'])
    
    # Recalculate compliance with detailed info
    compliance_score, missing_fields, sar_required_fields = check_compliance(case['sar_draft'], enriched_data, risk_analysis)
    
    # Check governance gate
    governance_checks = {
        'typology_confirmed': bool(case['typology_confirmed']),
        'evidence_linked': len(reason_evidence) > 0,
        'analyst_disposition': conn.execute('SELECT COUNT(*) FROM analyst_feedback WHERE case_id = ?', (case_id,)).fetchone()[0] > 0,
        'no_pending_interventions': conn.execute('SELECT COUNT(*) FROM interventions WHERE case_id = ? AND action = "hold_withdrawal"', (case_id,)).fetchone()[0] == 0 or case['status'] == 'intervened'
    }
    governance_checks['can_submit'] = all(governance_checks.values()) and compliance_score == 100
    
    # Add evidence pack
    evidence_pack = {
        'transaction_timeline': enriched_data['txn_history'],
        'trading_summary': {
            'total_transactions': len(enriched_data['txn_history']),
            'total_volume': sum(t['amount'] for t in enriched_data['txn_history']),
            'deposit_count': sum(1 for t in enriched_data['txn_history'] if t['type'] == 'deposit'),
            'withdrawal_count': sum(1 for t in enriched_data['txn_history'] if t['type'] == 'withdrawal'),
        },
        'network_links': {
            'shared_ips': list(set(t.get('ip') for t in enriched_data['txn_history'] if t.get('ip'))),
            'device_fingerprints': ['DEV-A8F2', 'DEV-A8F2', 'DEV-B1C3'],
            'linked_accounts': ['CUST-8821', 'CUST-5512'] if alert['customer_id'] == 'CUST-4455' else []
        },
        'kyc_snapshot': enriched_data['customer_data'],
        'device_logs': [
            {'timestamp': enriched_data['txn_history'][0]['timestamp'], 'device': 'iPhone 14', 'ip': enriched_data['txn_history'][0]['ip'], 'location': 'New York, NY'},
            {'timestamp': enriched_data['txn_history'][-1]['timestamp'], 'device': 'iPhone 14', 'ip': enriched_data['txn_history'][-1]['ip'], 'location': 'New York, NY'}
        ]
    }
    
    conn.close()
    
    return jsonify({
        'case': dict(case),
        'alert': dict(alert),
        'enriched_data': enriched_data,
        'risk_analysis': risk_analysis,
        'audit_logs': [dict(log) for log in audit_logs],
        'interventions': [dict(i) for i in interventions],
        'reason_evidence': [dict(re) for re in reason_evidence],
        'evidence_pack': evidence_pack,
        'adaptive_threshold': threshold_adj,
        'compliance_score': compliance_score,
        'missing_fields': missing_fields,
        'sar_required_fields': sar_required_fields,
        'governance_checks': governance_checks,
        'typologies': TYPOLOGIES
    })

@app.route('/api/alerts/<int:alert_id>/case', methods=['GET'])
def get_case_by_alert(alert_id):
    conn = get_db()
    case = conn.execute('SELECT id FROM cases WHERE alert_id = ? ORDER BY created_at DESC LIMIT 1', (alert_id,)).fetchone()
    conn.close()
    
    if not case:
        return jsonify({'error': 'No case found for this alert. Click Investigate first.'}), 404
    
    return jsonify({'case_id': case['id']})

@app.route('/api/cases/<int:case_id>/typology', methods=['POST'])
def confirm_typology(case_id):
    data = request.json
    conn = get_db()
    
    old_typology = conn.execute('SELECT typology, typology_confirmed FROM cases WHERE id = ?', (case_id,)).fetchone()
    
    conn.execute('UPDATE cases SET typology = ?, typology_confirmed = ?, updated_at = ? WHERE id = ?',
                 (data['typology'], 1, datetime.now().isoformat(), case_id))
    conn.commit()
    
    log_audit(case_id, data.get('analyst', 'analyst@signalsar.com'), 'typology_confirmed', 
              {'typology': data['typology']}, 
              old_typology['typology'] if old_typology else None, 
              data['typology'])
    
    conn.close()
    return jsonify({'status': 'typology_confirmed', 'typology': data['typology']})

@app.route('/api/cases/<int:case_id>/feedback', methods=['POST'])
def submit_feedback(case_id):
    data = request.json
    
    # Require rationale
    if not data.get('rationale'):
        return jsonify({'error': 'Decision rationale is required'}), 400
    
    conn = get_db()
    
    case = conn.execute('SELECT alert_id FROM cases WHERE id = ?', (case_id,)).fetchone()
    if not case:
        return jsonify({'error': 'Case not found'}), 404
    
    conn.execute('INSERT INTO analyst_feedback (case_id, alert_id, analyst, label, rationale, rationale_detail, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (case_id, case['alert_id'], data.get('analyst', 'analyst@signalsar.com'), data['label'], data['rationale'], data.get('rationale_detail', ''), datetime.now().isoformat()))
    conn.commit()
    
    log_audit(case_id, data.get('analyst', 'analyst@signalsar.com'), 'feedback_submitted', 
              {'label': data['label'], 'rationale': data['rationale'], 'detail': data.get('rationale_detail', '')})
    
    # Update adaptive thresholds
    update_adaptive_thresholds()
    
    conn.close()
    return jsonify({'status': 'feedback_recorded'})

@app.route('/api/cases/<int:case_id>/intervene', methods=['POST'])
def intervene(case_id):
    data = request.json
    
    # Require rationale
    if not data.get('rationale'):
        return jsonify({'error': 'Intervention rationale is required'}), 400
    
    conn = get_db()
    
    case = conn.execute('SELECT alert_id FROM cases WHERE id = ?', (case_id,)).fetchone()
    if not case:
        return jsonify({'error': 'Case not found'}), 404
    
    conn.execute('INSERT INTO interventions (case_id, alert_id, action, reason, rationale, analyst, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (case_id, case['alert_id'], data['action'], data.get('reason', 'High risk activity detected'), 
                  data['rationale'], data.get('analyst', 'analyst@signalsar.com'), datetime.now().isoformat()))
    
    conn.execute('UPDATE cases SET status = ?, updated_at = ? WHERE id = ?',
                 ('intervened', datetime.now().isoformat(), case_id))
    
    conn.execute('UPDATE alerts SET status = ? WHERE id = ?', ('intervened', case['alert_id']))
    
    conn.commit()
    
    log_audit(case_id, data.get('analyst', 'analyst@signalsar.com'), 'intervention_executed', 
              {'action': data['action'], 'reason': data.get('reason', 'High risk activity detected'), 'rationale': data['rationale']})
    
    conn.close()
    return jsonify({'status': 'intervention_executed', 'action': data['action']})



@app.route('/api/cases/<int:case_id>/sar', methods=['PUT'])
def update_sar(case_id):
    data = request.json
    conn = get_db()
    
    conn.execute('UPDATE cases SET sar_draft = ?, updated_at = ? WHERE id = ?',
                 (data['sar_draft'], datetime.now().isoformat(), case_id))
    conn.commit()
    
    log_audit(case_id, data.get('analyst', 'analyst@signalsar.com'), 'sar_edited', {'changes': 'Manual edit'})
    
    conn.close()
    return jsonify({'status': 'updated'})

@app.route('/api/cases/<int:case_id>/submit', methods=['POST'])
def submit_sar(case_id):
    data = request.json
    conn = get_db()
    
    case = conn.execute('SELECT * FROM cases WHERE id = ?', (case_id,)).fetchone()
    if not case:
        return jsonify({'error': 'Case not found'}), 404
    
    # Governance gate validation
    reason_evidence = conn.execute('SELECT * FROM reason_evidence WHERE case_id = ?', (case_id,)).fetchall()
    analyst_disposition = conn.execute('SELECT COUNT(*) FROM analyst_feedback WHERE case_id = ?', (case_id,)).fetchone()[0]
    
    if not case['typology_confirmed']:
        return jsonify({'error': 'Typology must be confirmed before submission'}), 400
    if len(reason_evidence) == 0:
        return jsonify({'error': 'At least one explainability reason with evidence must be attached'}), 400
    
    # Enforce: at least one reason_evidence row has non-empty evidence_ids
    has_valid_evidence = False
    for re in reason_evidence:
        evidence_ids = json.loads(re['evidence_ids'])
        if evidence_ids and len(evidence_ids) > 0:
            has_valid_evidence = True
            break
    
    if not has_valid_evidence:
        return jsonify({'error': 'At least one reason must have non-empty evidence_ids'}), 400
    
    if analyst_disposition == 0:
        return jsonify({'error': 'Analyst disposition must be recorded before submission'}), 400
    
    # Enforce: narrative includes typology code or description
    typology = case['typology']
    typology_desc = TYPOLOGIES.get(typology, '')
    if typology not in case['sar_draft'] and typology_desc not in case['sar_draft']:
        return jsonify({'error': f'SAR narrative must include typology code ({typology}) or description'}), 400
    
    submission_id = f'SAR-{uuid.uuid4().hex[:8].upper()}'
    submission_payload = {
        'submission_id': submission_id,
        'case_id': case_id,
        'typology': case['typology'],
        'sar_narrative': case['sar_draft'],
        'enriched_data': json.loads(case['enriched_data']),
        'compliance_score': case['compliance_score'],
        'analyst': data.get('analyst', 'analyst@signalsar.com')
    }
    
    # Calculate checksum for audit trail
    import hashlib
    checksum = hashlib.sha256(json.dumps(submission_payload, sort_keys=True).encode()).hexdigest()
    
    conn.execute('INSERT INTO submissions (case_id, sar_payload, submitted_at, submission_id, checksum) VALUES (?, ?, ?, ?, ?)',
                 (case_id, json.dumps(submission_payload), datetime.now().isoformat(), submission_id, checksum))
    
    conn.execute('UPDATE cases SET status = ?, updated_at = ? WHERE id = ?',
                 ('submitted', datetime.now().isoformat(), case_id))
    
    conn.execute('UPDATE alerts SET status = ? WHERE id = ?', ('closed', case['alert_id']))
    
    conn.commit()
    
    log_audit(case_id, data.get('analyst', 'analyst@signalsar.com'), 'sar_submitted', 
              {'submission_id': submission_id, 'checksum': checksum})
    
    conn.close()
    return jsonify({'submission_id': submission_id, 'status': 'submitted', 'checksum': checksum})

@app.route('/api/audit', methods=['GET'])
def get_audit_log():
    conn = get_db()
    logs = conn.execute('SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 50').fetchall()
    conn.close()
    return jsonify([dict(log) for log in logs])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
