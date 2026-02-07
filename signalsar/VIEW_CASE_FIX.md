# View Case Navigation Fix - Test Results

## ✅ Issue Fixed

**Problem:** Clicking "View Case" from Alert Queue showed "No case ID provided" error.

**Root Cause:** Alert Queue passed `alert_id` in URL, but Case page expected `case_id`.

**Solution:** Added case resolution endpoint and fallback logic.

---

## 📁 Files Changed

### 1. app.py (Backend)
**Added endpoint:**
```python
GET /api/alerts/<alert_id>/case
```
- Returns latest case_id for the alert
- Returns 404 with message if no case exists

### 2. static/index.html (Alert Queue)
**Updated `viewCase()` function:**
- Calls `/api/alerts/{alertId}/case` to resolve case_id
- Navigates to `/case.html?id={case_id}` (not alert_id)
- Shows user-friendly error if no case exists

### 3. static/case.html (Case Detail)
**Added fallback logic:**
- Checks for `alert_id` parameter if `id` is missing
- Calls resolution endpoint to get case_id
- Updates URL without reload using `history.replaceState()`
- Shows clear error message if no case found

---

## 🔌 New API Endpoint

### GET /api/alerts/{alert_id}/case

**Success Response (200):**
```json
{
  "case_id": 4
}
```

**Error Response (404):**
```json
{
  "error": "No case found for this alert. Click Investigate first."
}
```

---

## ✅ Test Results

### API Tests

**1. Create case for alert:**
```bash
curl -X POST http://127.0.0.1:5000/api/alerts/1/investigate
# Returns: {"case_id": 4, "compliance_score": 100}
```

**2. Resolve case_id from alert_id:**
```bash
curl http://127.0.0.1:5000/api/alerts/1/case
# Returns: {"case_id": 4}
```

**3. Non-existent case:**
```bash
curl http://127.0.0.1:5000/api/alerts/99/case
# Returns: {"error": "No case found for this alert. Click Investigate first."}
```

---

## 🧪 End-to-End Test Steps

### Test Flow 1: Investigate → View Case

1. **Start Application:**
   ```bash
   cd signalsar
   source venv/bin/activate
   python3 app.py
   ```

2. **Open Browser:** http://127.0.0.1:5000

3. **Investigate Alert:**
   - Click "Investigate" on Alert #1
   - ✅ Case Detail page loads with case_id in URL
   - ✅ All evidence and data displayed

4. **Return to Queue:**
   - Click "← Back to Queue" or navigate to home
   - ✅ Alert #1 status now shows "investigating"

5. **View Case:**
   - Click "View Case" button on Alert #1
   - ✅ Case Detail page loads correctly
   - ✅ Same case data displayed
   - ✅ No "No case ID provided" error

### Test Flow 2: View Case Without Investigation

1. **Open Alert Queue**

2. **Try View Case on Uninvestigated Alert:**
   - Find an alert with status "open" (not investigated)
   - Click "View Case" (if button exists)
   - ✅ Alert shows: "No case found for this alert. Click Investigate first."

### Test Flow 3: Direct URL Access

1. **Access with case_id:**
   ```
   http://127.0.0.1:5000/case.html?id=4
   ```
   - ✅ Case loads correctly

2. **Access with alert_id (fallback):**
   ```
   http://127.0.0.1:5000/case.html?alert_id=1
   ```
   - ✅ Case resolves and loads
   - ✅ URL updates to `?id=4` automatically

3. **Access with no parameters:**
   ```
   http://127.0.0.1:5000/case.html
   ```
   - ✅ Shows: "No case ID provided"

---

## 🔄 Navigation Flow Diagram

```
Alert Queue
    │
    ├─ [Investigate] ──> POST /api/alerts/{id}/investigate
    │                    └─> Returns case_id
    │                        └─> Navigate to /case.html?id={case_id}
    │
    └─ [View Case] ──> GET /api/alerts/{id}/case
                       └─> Returns case_id
                           └─> Navigate to /case.html?id={case_id}

Case Detail Page
    │
    ├─ URL: ?id={case_id}
    │   └─> Load case directly
    │
    └─ URL: ?alert_id={alert_id} (fallback)
        └─> GET /api/alerts/{alert_id}/case
            └─> Resolve case_id
                └─> Update URL to ?id={case_id}
                    └─> Load case
```

---

## ✅ Verification Checklist

- [x] New endpoint `/api/alerts/{alert_id}/case` returns case_id
- [x] Endpoint returns 404 with message if no case exists
- [x] "View Case" button resolves case_id before navigation
- [x] "View Case" shows error if no case found
- [x] Case page supports both `id` and `alert_id` parameters
- [x] Case page auto-resolves alert_id to case_id
- [x] URL updates without page reload when using fallback
- [x] "Investigate" button behavior unchanged
- [x] Error messages are user-friendly
- [x] No console errors in browser

---

## 🎯 User Experience Improvements

### Before:
- Click "View Case" → ❌ "No case ID provided" error
- Confusing for users
- Required manual URL editing

### After:
- Click "View Case" → ✅ Case loads correctly
- Clear error if no case exists: "No case found for this alert. Click Investigate first."
- Seamless navigation between Alert Queue and Case Detail

---

## 🔍 Edge Cases Handled

1. **Alert with no case:**
   - Shows: "No case found for this alert. Click Investigate first."

2. **Alert with multiple cases:**
   - Returns latest case (ORDER BY created_at DESC LIMIT 1)

3. **Direct URL access with alert_id:**
   - Automatically resolves to case_id
   - Updates URL for consistency

4. **Invalid alert_id:**
   - Returns 404 with clear error message

5. **Network errors:**
   - Caught and displayed to user

---

## 📊 Test Summary

**API Endpoint:** ✅ Working
**Alert Queue Navigation:** ✅ Fixed
**Case Page Fallback:** ✅ Implemented
**Error Handling:** ✅ User-friendly
**Existing Flows:** ✅ Unchanged

**Total Files Changed:** 3
- app.py (1 new endpoint)
- index.html (updated viewCase function)
- case.html (added fallback logic)

---

## 🚀 Deployment Notes

No database changes required. Changes are backward compatible:
- Old URLs with `?id={case_id}` still work
- New URLs with `?alert_id={alert_id}` now work
- API endpoint is additive (no breaking changes)
