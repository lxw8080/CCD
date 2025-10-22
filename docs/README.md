# Documentation Hub

Welcome to the consolidated documentation portal for the Customer Content Delivery (CCD) project.

## Getting Started
- `README.md` — quick project overview
- `QUICK_START.md` — spin up the stack locally
- `WINDOWS_SETUP_CN.md` — Windows-specific setup tips
- `docs/PROJECT_CHANGELOG.md` — fine-grained change log
- `CHANGELOG.md` — release level summary

## Audience Guide
- **End users** → `docs/guides/USER_GUIDE.md`
- **Developers** → `backend/README.md`, `frontend/README.md`
- **QA** → `docs/guides/custom-fields-testing.md`
- **Operations** → `deployment/README.md`, `docs/guides/database-migration-guide.md`
- **Stakeholders** → `PROJECT_SUMMARY.md`, `PROJECT_STRUCTURE.md`

## Guides Directory
```
docs/guides/
├── USER_GUIDE.md                # Feature-by-feature walkthrough
├── custom-fields-testing.md     # Manual QA scenarios and smoke tests
└── database-migration-guide.md  # Checked procedure for external PostgreSQL
```

## History Archive
```
docs/history/
└── dynamic-custom-fields-2025-10-21.md  # Dynamic custom fields rollout report
```

When you add new reference material:
1. Place audience-facing docs under `docs/guides/`.
2. Archive project retrospectives under `docs/history/` with `YYYY-MM-DD` date prefixes.
3. Update this hub together with `DOCS_INDEX.md` and the root `项目导航.md`.

For questions or missing entries, document the answer and add a link here so future contributors can find it quickly.
