// Governance UI Components for SignalSAR

// Rationale options for analyst decisions
const RATIONALE_OPTIONS = {
    true_positive: [
        'Pattern matches known typology',
        'Evidence strongly supports suspicious activity',
        'Customer profile inconsistent with activity',
        'Network analysis confirms coordination',
        'Regulatory threshold exceeded'
    ],
    false_positive: [
        'Legitimate business activity',
        'Customer profile supports activity',
        'Insufficient evidence of intent',
        'System misconfiguration',
        'Duplicate alert'
    ],
    intervention: [
        'Imminent risk of fund movement',
        'High-value suspicious activity',
        'Regulatory obligation to freeze',
        'Customer unresponsive to inquiries',
        'Pattern indicates ongoing criminal activity'
    ]
};

// Show rationale modal
function showRationaleModal(action, callback) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    
    const options = RATIONALE_OPTIONS[action] || [];
    
    modal.innerHTML = `
        <div class="modal-content governance-modal">
            <h2>Decision Rationale Required</h2>
            <p>Regulatory compliance requires documented rationale for all analyst decisions.</p>
            
            <div class="form-group">
                <label><strong>Select Primary Rationale:</strong></label>
                <select id="rationaleSelect" class="form-control" required>
                    <option value="">-- Select Rationale --</option>
                    ${options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}
                </select>
            </div>
            
            <div class="form-group">
                <label><strong>Additional Details (Optional):</strong></label>
                <textarea id="rationaleDetail" class="form-control" rows="3" placeholder="Provide additional context if needed..."></textarea>
            </div>
            
            <div class="modal-actions">
                <button class="btn btn-secondary" onclick="closeRationaleModal()">Cancel</button>
                <button class="btn btn-primary" onclick="submitRationale()">Confirm</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    window.closeRationaleModal = () => {
        document.body.removeChild(modal);
    };
    
    window.submitRationale = () => {
        const rationale = document.getElementById('rationaleSelect').value;
        const detail = document.getElementById('rationaleDetail').value;
        
        if (!rationale) {
            alert('Please select a rationale');
            return;
        }
        
        callback(rationale, detail);
        document.body.removeChild(modal);
    };
}

// Render typology confirmation UI
function renderTypologyConfirmation(caseData, typologies) {
    return `
        <div class="card full-width governance-card">
            <h2>🏛️ Typology Attribution (Regulatory Requirement)</h2>
            <div class="typology-section">
                <div class="typology-detected">
                    <strong>Machine-Detected Typology:</strong>
                    <span class="typology-badge">${caseData.typology || 'UNKNOWN_PATTERN'}</span>
                </div>
                
                <div class="typology-confirm">
                    <label><strong>Analyst Confirmation:</strong></label>
                    <select id="typologySelect" class="form-control" ${caseData.typology_confirmed ? 'disabled' : ''}>
                        ${Object.entries(typologies).map(([code, desc]) => `
                            <option value="${code}" ${caseData.typology === code ? 'selected' : ''}>${code}: ${desc}</option>
                        `).join('')}
                    </select>
                    
                    ${caseData.typology_confirmed ? 
                        '<div class="success">✓ Typology confirmed by analyst</div>' :
                        '<button class="btn btn-primary" onclick="confirmTypology()">Confirm Typology</button>'
                    }
                </div>
            </div>
        </div>
    `;
}

// Render evidence-linked reasons
function renderEvidenceReasons(reasonEvidence, riskAnalysis) {
    if (!reasonEvidence || reasonEvidence.length === 0) {
        return '<div class="warning">⚠️ No evidence links established</div>';
    }
    
    return `
        <div class="evidence-reasons">
            ${reasonEvidence.map(re => {
                const evidence = JSON.parse(re.evidence_ids);
                return `
                    <div class="evidence-reason-item">
                        <div class="reason-header">
                            <strong>${re.reason_code}</strong>
                            <span class="evidence-count">${evidence.length} evidence items</span>
                        </div>
                        <div class="reason-metric">${re.metric}</div>
                        <div class="reason-evidence">
                            <details>
                                <summary>View Supporting Evidence</summary>
                                <ul class="evidence-list">
                                    ${evidence.map(id => `<li><code>${id}</code></li>`).join('')}
                                </ul>
                            </details>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;
}

// Render governance gate status
function renderGovernanceGate(governanceChecks) {
    const checks = [
        { key: 'typology_confirmed', label: 'Typology Attribution Confirmed', required: true },
        { key: 'evidence_linked', label: 'Evidence Linked to Reasons', required: true },
        { key: 'analyst_disposition', label: 'Analyst Disposition Recorded', required: true },
        { key: 'no_pending_interventions', label: 'No Unresolved Interventions', required: false }
    ];
    
    return `
        <div class="card full-width governance-gate-card">
            <h2>🔒 Submission Governance Gate</h2>
            <p class="governance-subtitle">All checks must pass before SAR submission to regulatory portal</p>
            
            <div class="governance-checks">
                ${checks.map(check => `
                    <div class="governance-check ${governanceChecks[check.key] ? 'check-pass' : 'check-fail'}">
                        <span class="check-icon">${governanceChecks[check.key] ? '✓' : '✗'}</span>
                        <span class="check-label">${check.label}</span>
                        ${check.required ? '<span class="check-required">REQUIRED</span>' : ''}
                    </div>
                `).join('')}
            </div>
            
            ${governanceChecks.can_submit ? 
                '<div class="success">✓ All governance checks passed. SAR submission enabled.</div>' :
                '<div class="error">✗ Governance checks incomplete. SAR submission blocked.</div>'
            }
        </div>
    `;
}
