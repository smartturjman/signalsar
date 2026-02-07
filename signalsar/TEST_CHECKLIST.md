# Regulator-Hardening Patch - Test Checklist

## Backend Tests

### 1. Typology Truncation Fix
- [ ] Investigate alert CUST-8821 (Rapid Movement)
- [ ] Verify typology in case detail shows full string (e.g., "RAPID_MOVEMENT")
- [ ] Check database: `SELECT typology FROM cases WHERE id=1`
- [ ] Expected: Full typology string, not truncated to 3 chars

### 2. NEW TYPOLOGY Mapping
- [ ] Investigate alert CUST-4455 (NEW TYPOLOGY)
- [ ] Verify typology is mapped to "MICRO_FRAGMENTATION"
- [ ] Check database: `SELECT typology FROM cases WHERE alert_id=2`
- [ ] Expected: "MICRO_FRAGMENTATION" (valid enum code)

### 3. Submission Validation - Evidence IDs
- [ ] Create a case without evidence
- [ ] Try to submit SAR
- [ ] Expected: Error "At least one reason must have non-empty evidence_ids"

### 4. Submission Validation - Narrative
- [ ] Edit SAR narrative to remove typology code
- [ ] Try to submit
- [ ] Expected: Error "SAR narrative must include typology code or description"

### 5. Database Foreign Keys
- [ ] Check schema: `sqlite3 signalsar.db ".schema cases"`
- [ ] Expected: `FOREIGN KEY (alert_id) REFERENCES alerts(id)`
- [ ] Try to insert case with invalid alert_id
- [ ] Expected: Foreign key constraint violation

### 6. Unique Indexes
- [ ] Check indexes: `sqlite3 signalsar.db "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='submissions'"`
- [ ] Expected: idx_submissions_submission_id, idx_submissions_checksum
- [ ] Try to insert duplicate submission_id
- [ ] Expected: Unique constraint violation

### 7. Append-Only Triggers
- [ ] Submit a SAR to create submission record
- [ ] Try: `UPDATE submissions SET checksum='test' WHERE id=1`
- [ ] Expected: Error "submissions is append-only: updates not allowed"
- [ ] Try: `DELETE FROM audit_log WHERE id=1`
- [ ] Expected: Error "audit_log is append-only: deletes not allowed"

## Frontend Tests

### 8. SAR.html - Rationale Modal (True Positive)
- [ ] Navigate to SAR draft page
- [ ] Click "Mark True Positive"
- [ ] Expected: Modal appears (not prompt)
- [ ] Modal has dropdown with 5 options
- [ ] Modal has optional detail textarea
- [ ] Select option and submit
- [ ] Expected: Feedback recorded, modal closes

### 9. SAR.html - Rationale Modal (False Positive)
- [ ] Click "Mark False Positive"
- [ ] Expected: Modal with different options
- [ ] Cancel button works
- [ ] Submit without selection shows error

### 10. Case.html - Typology Dropdown
- [ ] Navigate to case detail page
- [ ] Find "Typology Attribution" section
- [ ] Expected: Dropdown showing all TYPOLOGIES
- [ ] Machine-detected typology is pre-selected
- [ ] Select different typology
- [ ] Click "Confirm Typology"
- [ ] Expected: Typology updated, dropdown disabled

### 11. Case.html - Rationale Modals
- [ ] Click "Mark True Positive"
- [ ] Expected: Modal (not prompt)
- [ ] Click "Mark False Positive"
- [ ] Expected: Modal (not prompt)
- [ ] Click "Hold Withdrawal" (if available)
- [ ] Expected: Confirm dialog, then modal for rationale

### 12. Case.html - No Duplicate Blocks
- [ ] Navigate to case detail page
- [ ] Scroll through entire page
- [ ] Expected: Only ONE "Customer Profile" card
- [ ] Expected: Only ONE "Risk Analysis" card
- [ ] Expected: Risk analysis shows both evidence and reason codes

### 13. Audit.html - JSON Parsing
- [ ] Navigate to audit log page
- [ ] Find entry with action "case_created"
- [ ] Check Details column
- [ ] Expected: Readable format like "alert_id: 1" (not raw JSON)
- [ ] Find entry with action "sar_submitted"
- [ ] Expected: "submission_id: SAR-XXXXX, checksum: abc123..."

## Integration Tests

### 14. Full Workflow - Valid Submission
- [ ] Investigate alert
- [ ] Confirm typology via dropdown
- [ ] Mark true positive via modal
- [ ] Navigate to SAR draft
- [ ] Submit SAR
- [ ] Expected: Success, submission_id returned
- [ ] Check audit log shows all steps

### 15. Full Workflow - Blocked Submission
- [ ] Investigate alert
- [ ] Do NOT confirm typology
- [ ] Try to submit SAR
- [ ] Expected: Error "Typology must be confirmed"
- [ ] Confirm typology
- [ ] Try to submit without feedback
- [ ] Expected: Error "Analyst disposition must be recorded"

### 16. Database Integrity After Migration
- [ ] Check all existing cases still load
- [ ] Check all existing audit logs still visible
- [ ] Check all existing alerts still in queue
- [ ] No data loss from migration

## Browser Compatibility

### 17. Modal Display
- [ ] Test in Chrome/Edge
- [ ] Test in Firefox
- [ ] Test in Safari
- [ ] Modal centers properly
- [ ] Modal backdrop blocks interaction
- [ ] Modal closes on cancel

### 18. Dropdown Functionality
- [ ] Typology dropdown works in all browsers
- [ ] Options display correctly
- [ ] Selection updates properly

## Performance

### 19. Page Load Times
- [ ] Case detail page loads in <2 seconds
- [ ] SAR draft page loads in <2 seconds
- [ ] Audit log page loads in <2 seconds

### 20. Database Query Performance
- [ ] Foreign key checks don't slow down inserts
- [ ] Unique index checks are fast
- [ ] Trigger execution is fast

## Regression Tests

### 21. Existing Features Still Work
- [ ] Alert queue displays correctly
- [ ] Investigation creates case
- [ ] Evidence pack populates
- [ ] Transaction timeline displays
- [ ] Network analysis shows
- [ ] Adaptive thresholds work
- [ ] Interventions execute

## Security

### 22. SQL Injection Prevention
- [ ] Foreign keys prevent orphaned records
- [ ] Triggers prevent data tampering
- [ ] Unique indexes prevent duplicates

### 23. Audit Trail Integrity
- [ ] Cannot modify audit_log records
- [ ] Cannot delete audit_log records
- [ ] Cannot modify submissions
- [ ] Cannot delete submissions

## Documentation

### 24. Code Comments
- [ ] New validation logic is commented
- [ ] Migration script is documented
- [ ] Test script is documented

### 25. README Updates
- [ ] REGULATOR_HARDENING_PATCH.md is complete
- [ ] Deployment instructions are clear
- [ ] Migration steps are documented

## Sign-Off

- [ ] All backend tests pass
- [ ] All frontend tests pass
- [ ] All integration tests pass
- [ ] No regressions found
- [ ] Documentation complete
- [ ] Ready for deployment

---

## Test Results

Date: _______________
Tester: _______________

Backend Tests: _____ / 7 passed
Frontend Tests: _____ / 6 passed
Integration Tests: _____ / 3 passed
Browser Tests: _____ / 2 passed
Performance Tests: _____ / 2 passed
Regression Tests: _____ / 1 passed
Security Tests: _____ / 2 passed

Total: _____ / 23 passed

Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
