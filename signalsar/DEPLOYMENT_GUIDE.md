# Regulator-Hardening Patch - Deployment Guide

## Quick Start

```bash
# 1. Backup database
cp signalsar.db signalsar.db.backup.$(date +%Y%m%d_%H%M%S)

# 2. Run migration
python3 migrate_db.py

# 3. Verify changes
python3 test_fixes.py

# 4. Start application
python3 app.py
```

## Pre-Deployment Checklist

- [ ] Backup current database
- [ ] Review REGULATOR_HARDENING_PATCH.md
- [ ] Ensure Python 3.x is installed
- [ ] Ensure all dependencies are installed (`pip install -r requirements.txt`)
- [ ] Stop any running instances of the application

## Deployment Steps

### Step 1: Backup Database

```bash
# Create timestamped backup
cp signalsar.db signalsar.db.backup.$(date +%Y%m%d_%H%M%S)

# Verify backup
ls -lh signalsar.db*
```

### Step 2: Run Migration

```bash
python3 migrate_db.py
```

**Expected Output:**
```
Migrating database schema to add foreign keys and constraints...
Migration complete!
- Added foreign key constraints
- Added unique indexes on submissions
- Added append-only triggers on audit_log and submissions
```

**If you see "Database already has foreign keys. No migration needed.":**
- This is normal if you've already run the migration
- Skip to Step 3

### Step 3: Verify Changes

```bash
python3 test_fixes.py
```

**Expected Output:**
```
============================================================
REGULATOR-HARDENING PATCH VERIFICATION
============================================================

1. Testing typology truncation fix...
   ✓ PASS: Full typology string returned (not truncated)

2. Testing NEW TYPOLOGY mapping...
   ✓ PASS: Typology 'MICRO_FRAGMENTATION' is valid enum code

3. Testing database foreign keys...
   ✓ PASS: Foreign keys present in cases table

4. Testing unique indexes on submissions...
   ✓ PASS: Unique indexes on submission_id and checksum

5. Testing append-only triggers...
   ✓ PASS: All append-only triggers present

6. Testing evidence_ids validation...
   ✓ PASS: Evidence IDs are non-empty

============================================================
VERIFICATION COMPLETE
============================================================
```

**All tests must pass before proceeding.**

### Step 4: Test Trigger Functionality

```bash
# Test audit_log immutability
sqlite3 signalsar.db "UPDATE audit_log SET analyst='test' WHERE id=1" 2>&1

# Expected: Error: audit_log is append-only: updates not allowed

# Test submissions immutability
sqlite3 signalsar.db "DELETE FROM submissions WHERE id=1" 2>&1

# Expected: Error: submissions is append-only: deletes not allowed
```

### Step 5: Start Application

```bash
python3 app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 6: Smoke Test

Open browser to `http://localhost:5000` and verify:

1. **Alert Queue Loads**
   - Navigate to home page
   - Verify alerts display

2. **Case Investigation Works**
   - Click "Investigate" on any alert
   - Verify case detail page loads
   - Check typology dropdown appears

3. **Typology Confirmation**
   - Select typology from dropdown
   - Click "Confirm Typology"
   - Verify confirmation succeeds

4. **Rationale Modal**
   - Click "Mark True Positive"
   - Verify modal appears (not prompt)
   - Select rationale and submit
   - Verify feedback recorded

5. **SAR Submission**
   - Navigate to SAR draft
   - Verify governance checks
   - Submit SAR (if all checks pass)
   - Verify submission succeeds

6. **Audit Log**
   - Navigate to audit log
   - Verify details are readable (not raw JSON)

## Rollback Procedure

If issues occur:

```bash
# 1. Stop application
# Press Ctrl+C or kill process

# 2. Restore backup
cp signalsar.db.backup.YYYYMMDD_HHMMSS signalsar.db

# 3. Restart application
python3 app.py
```

## Troubleshooting

### Migration Fails

**Error: "database is locked"**
- Stop all running instances of the application
- Close any SQLite browser connections
- Retry migration

**Error: "no such table"**
- Verify you're in the correct directory
- Check signalsar.db exists
- Verify database is not corrupted

### Tests Fail

**Test 1 or 2 fails (typology issues)**
- Check app.py was updated correctly
- Verify no syntax errors: `python3 -m py_compile app.py`

**Test 3, 4, or 5 fails (database issues)**
- Re-run migration: `python3 migrate_db.py`
- Check database schema: `sqlite3 signalsar.db ".schema"`

**Test 6 fails (evidence issues)**
- This may be normal if no cases exist yet
- Investigate an alert to create a case
- Re-run test

### Application Won't Start

**Error: "Address already in use"**
- Another instance is running on port 5000
- Kill process: `lsof -ti:5000 | xargs kill -9`
- Or change port in app.py

**Error: "No module named 'flask'"**
- Install dependencies: `pip install -r requirements.txt`
- Or activate virtual environment: `source venv/bin/activate`

### Frontend Issues

**Modal doesn't appear**
- Check browser console for JavaScript errors
- Verify governance.js is loaded
- Clear browser cache

**Typology dropdown missing**
- Check case.html was updated correctly
- Verify API returns typologies dict
- Check browser console for errors

## Post-Deployment Verification

Use TEST_CHECKLIST.md to perform comprehensive testing:

```bash
# Review checklist
cat TEST_CHECKLIST.md

# Run through each test
# Document results
```

## Monitoring

After deployment, monitor:

1. **Application Logs**
   - Check app.log for errors
   - Monitor for foreign key violations

2. **Database Integrity**
   - Verify no orphaned records
   - Check audit_log is append-only
   - Verify submissions are immutable

3. **User Feedback**
   - Confirm analysts can use new UI
   - Verify rationale modals work
   - Check typology dropdown functions

## Support

If issues persist:

1. Check REGULATOR_HARDENING_PATCH.md for implementation details
2. Review TEST_CHECKLIST.md for specific test cases
3. Examine test_fixes.py for verification logic
4. Check app.log for error messages

## Files Modified

- `app.py` - Backend logic
- `init_db.py` - Schema for new databases
- `static/sar.html` - Rationale modals
- `static/case.html` - Typology dropdown, rationale modals
- `static/audit.html` - JSON parsing
- `static/styles.css` - Modal styles

## Files Created

- `migrate_db.py` - Migration script
- `test_fixes.py` - Verification script
- `REGULATOR_HARDENING_PATCH.md` - Implementation summary
- `TEST_CHECKLIST.md` - Test checklist
- `DEPLOYMENT_GUIDE.md` - This guide

## Success Criteria

Deployment is successful when:

- ✓ All tests in test_fixes.py pass
- ✓ Application starts without errors
- ✓ Alert queue displays correctly
- ✓ Case investigation works
- ✓ Typology dropdown functions
- ✓ Rationale modals appear
- ✓ SAR submission succeeds
- ✓ Audit log is readable
- ✓ No duplicate UI blocks
- ✓ Database triggers block updates/deletes

## Timeline

Estimated deployment time: **15-30 minutes**

- Backup: 1 minute
- Migration: 2-5 minutes
- Verification: 5-10 minutes
- Testing: 10-15 minutes

## Maintenance

### Regular Checks

- Weekly: Verify audit_log integrity
- Weekly: Check for orphaned records
- Monthly: Review submission checksums
- Monthly: Validate foreign key constraints

### Database Maintenance

```bash
# Check database integrity
sqlite3 signalsar.db "PRAGMA integrity_check"

# Vacuum database (reclaim space)
sqlite3 signalsar.db "VACUUM"

# Analyze query performance
sqlite3 signalsar.db "ANALYZE"
```

## Contact

For questions or issues with this deployment:
- Review documentation in this repository
- Check application logs
- Verify database schema
