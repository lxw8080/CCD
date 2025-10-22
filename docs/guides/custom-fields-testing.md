# Dynamic Custom Fields – Testing Guide

## Scope
- validate backend + frontend support for configurable customer fields
- confirm the `"申请日期"` (application date) field uses the dynamic `TODAY` default safely
- ensure admin changes flow through to both PC and mobile clients without deployments

## Test Environment
- Backend: `python manage.py runserver` (Django 4.2, PostgreSQL `ccd_dev`)
- Frontend: `npm run dev` (Vite, Vue 3)
- Admin URL: `http://127.0.0.1:8000/admin/` (default account `admin / admin123`)
- External DB already contains nine sample fields (product, amount, date, etc.)

## Quick Smoke Checklist
1. **Create customer** → open “New Customer”, confirm “申请日期” pre-fills with today, submit successfully.
2. **Edit customer** → reopen the saved record, ensure “申请日期” shows the stored value (not today), edit other data, re-save.
3. **Mobile view** → repeat create + edit flows in mobile simulator (F12 device mode) to verify parity.
4. **Admin update** → toggle a field in Django Admin (e.g., change label), refresh the form and confirm it updates instantly.
5. **API payload** → inspect network request; payload should include `custom_fields` with field IDs as keys.

Record pass/fail for each step; investigate immediately if any expectation fails.

## Detailed Scenarios

### 1. Admin CRUD
- Visit *Customers → Custom fields* in Django Admin.
- Create a new field (e.g., “客户来源” select field) and check it appears on the clients after a refresh.
- Disable (`is_active = False`) an existing field and verify it disappears from forms while past submissions remain intact.

### 2. PC Form Validation
- Leave required custom fields empty → expect validation errors.
- Enter out-of-range values (e.g., amount `100000000`) → expect rule violation.
- Provide malformed email/phone → expect pattern errors.
- Submit with valid data → expect success and persisted values.

### 3. Mobile Form Validation
- Switch to mobile device emulation; repeat PC tests.
- Confirm Vant components (pickers, date pickers, inputs) render correctly and show validation feedback.

### 4. Edit Flow Regression
- Create a record with “申请日期” set to a past value (e.g., `2025-10-15`).
- Reopen in edit mode on both clients; ensure the original value is displayed and saved.
- Confirm the default initialisation no longer runs when `isEdit` is true (watch console logs if instrumented).

### 5. API Verification
- Use browser dev tools or `curl` with an auth token to inspect requests:
  ```bash
  curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/customers/custom-fields/
  ```
- Confirm the `POST /api/customers/` payload carries a `custom_fields` object, and responses echo the same structure.

## Troubleshooting
- **Default not applied** → run `python backend/verify_default_value.py` to confirm the database holds `"TODAY"`.
- **Edit still overwrites date** → ensure both PC and mobile forms wrap default initialisation with `if (!isEdit.value)`.
- **Client missing new fields** → check network request to `/custom-fields/` and confirm no caching; restart frontend dev server if Vite cache is stale.
- **Validation mismatch** → review serializer constraints vs. generated front-end rules to keep parity.

## Test Data Reference
```json
{
  "name": "测试客户",
  "id_card": "110101199001011234",
  "phone": "13800138000",
  "address": "北京市朝阳区",
  "status": "pending",
  "custom_fields": {
    "1": "个人贷款",
    "2": "50",
    "3": "2025-10-21"
  }
}
```

## Post-Test Actions
- Capture outcomes in QA notes; highlight any fields that need additional validation rules.
- Re-enable any fields disabled for testing.
- If deploying, rerun `python check_external_db.py` and `python test_api_access.py` for extra assurance.

## Related Docs
- `docs/history/dynamic-custom-fields-2025-10-21.md` – rollout summary
- `backend/update_application_date_default.py` – updates the default flag
- `backend/test_custom_fields.py` – seeds sample configuration
