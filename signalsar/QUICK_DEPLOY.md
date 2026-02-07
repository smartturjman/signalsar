# Quick Deploy - Regulator-Hardening Patch

## 30-Second Deploy

```bash
# Backup, migrate, verify, start
cp signalsar.db signalsar.db.backup && \
python3 migrate_db.py && \
python3 test_fixes.py && \
python3 app.py
```

## What Changed?

### Backend ✓
- Full typology strings (not truncated)
- NEW TYPOLOGY → MICRO_FRAGMENTATION
- Submission validation (evidence + narrative)

### Database ✓
- Foreign keys enabled
- Unique indexes on submissions
- Append-only audit_log & submissions

### Frontend ✓
- Rationale modals (not prompts)
- Typology dropdown selection
- No duplicate UI blocks
- Readable audit log

## Quick Test

```bash
# 1. Verify backend
python3 test_fixes.py

# 2. Test triggers
sqlite3 signalsar.db "UPDATE audit_log SET analyst='test' WHERE id=1"
# Expected: Error (append-only)

# 3. Start app
python3 app.py

# 4. Open browser
# http://localhost:5000
```

## Rollback

```bash
cp signalsar.db.backup signalsar.db
python3 app.py
```

## Files

- `migrate_db.py` - Run once to upgrade DB
- `test_fixes.py` - Verify changes
- `DEPLOYMENT_GUIDE.md` - Full instructions
- `TEST_CHECKLIST.md` - Complete tests

## Success Criteria

- ✓ test_fixes.py passes all 6 tests
- ✓ App starts without errors
- ✓ Modals appear (not prompts)
- ✓ Typology dropdown works
- ✓ Audit log is readable

## Support

See DEPLOYMENT_GUIDE.md for troubleshooting.
