# Dynamic Custom Fields Rollout (2025-10-21)

## Summary
- completed a full dynamic custom field system for customers, covering backend models, REST APIs, and admin UX
- deployed schema migration `0003_customfield_remove_customer_remarks_customfieldvalue` to the external PostgreSQL database (`ccd_dev` on `115.190.29.10:5433`)
- added client-side form rendering on both Element Plus (PC) and Vant (mobile) with per-field validation rules
- introduced a dynamic default value flag (`TODAY`) for the date field “申请日期” (application date) and verified it end-to-end
- resolved an edit-mode regression that previously overwrote saved dates with the current day

## Backend Implementation Highlights
- Added `CustomField` and `CustomFieldValue` models to `backend/apps/customers/models.py`; the former stores configuration, the latter stores values with a `(customer_id, custom_field_id)` uniqueness constraint.
- Extended serializers, viewsets, and URLs to expose CRUD endpoints for custom fields plus read/write support inside customer APIs.
- Registered the models inside Django Admin with grouped fieldsets, search, and filters so operations staff can manage configuration without code changes.
- Included helper scripts (`test_custom_fields.py`, `verify_default_value.py`) for seeding and verifying custom field data.

### Available Field Types
`text`, `textarea`, `number`, `date`, `select`, `email`, `phone`, `url` (all validated on the server and rendered with dedicated widgets on the clients).

## Frontend Updates
- `frontend/src/views/pc/CustomerForm.vue` renders fields dynamically with Element Plus controls, generates validation rules, and persists values alongside the main form.
- `frontend/src/views/mobile/CustomerForm.vue` mirrors the same behaviour with Vant components, including mobile date pickers and select pickers.
- `frontend/src/api/customer.js` encapsulates the REST calls for listing configuration and submitting customer payloads that embed `custom_fields`.

## Deployment & Database Checklist
- Local SQLite database (`backend/db.sqlite3`) removed; the app now targets the external PostgreSQL database exclusively.
- External DB verified via `check_external_db.py`; tables `custom_fields` (17 columns) and `custom_field_values` (6 columns) exist with foreign keys, unique constraints, and indexes.
- `python manage.py showmigrations customers` confirms migrations 0001–0003 applied.
- Recommended deployment commands:
  ```bash
  python manage.py migrate
  python manage.py showmigrations customers
  python check_external_db.py
  python test_api_access.py
  ```
- Optional backup prior to production rollout:
  ```bash
  pg_dump -h 115.190.29.10 -p 5433 -U flask_user -d ccd_dev -F c -f backup-2025-10-21.dump
  ```

## Dynamic Default Value (“申请日期”)
- Requirement: auto-fill the application date when creating a customer while preserving existing data during edits.
- Solution: store the literal `"TODAY"` in `CustomField.default_value`; translate it to `YYYY-MM-DD` on the client.
- Script `backend/update_application_date_default.py` updates the configuration, while `verify_default_value.py` confirms the state.
- Frontend logic formats the current date and sets it only when `!isEdit` and the form value is empty.

## Edit Mode Bug Fix
- Issue: editing a customer replaced the saved date with the current day because the default initialisation always ran.
- Fix: guard the default initialisation with `if (!isEdit.value)` in both PC and mobile form components so existing values stay intact.
- Regression tests cover creating, editing, and cross-device flows to confirm the original date persists.

## Validation & Testing
- See `docs/guides/custom-fields-testing.md` for the consolidated manual test plan (quick smoke tests plus full scenario coverage).
- Key checkpoints:
  - new customer forms auto-fill today’s date but allow overrides
  - existing customer edits retain stored dates
  - Admin CRUD operations in Django reflect instantly on both clients
  - API payloads include the `custom_fields` object, matching validation expectations

## Follow-up Recommendations
- Consider caching field definitions if load grows.
- Extend the dynamic default pattern to support values such as `TOMORROW` when needed.
- Layer role-based visibility or grouping to improve large forms.
- Monitor database performance and add targeted indexes if custom field volume increases significantly.
- Reference `docs/guides/database-migration-guide.md` before running future schema work.
