# ChoreOps Dashboards

Dashboard template registry for ChoreOps.

This repository is the dedicated source for Lovelace dashboard templates used by the ChoreOps integration. It is designed to support a dual-repository model where:

- `ccpk1/choreops` provides integration/backend logic
- `ccpk1/choreops-dashboards` provides dashboard manifests and template YAML assets

## Purpose

- Publish dashboard template updates independently from integration releases
- Enable safe hotfixes for UI/template issues
- Provide a registry contract (`dashboard_registry.json`) for dynamic template discovery

## Repository layout

```text
.
├── dashboard_registry.json    # Dashboard registry contract
├── templates/                 # Dashboard template YAML assets
│   ├── *.yaml
├── preferences/               # Per-template preference docs
│   ├── *.md
└── translations/              # Dashboard UI translation assets
		├── {lang}_dashboard.json
```

## Current template IDs

The current manifest uses versioned, immutable template IDs:

- `user-gamification-v1` → `templates/user-gamification-v1.yaml`
- `user-minimal-v1` → `templates/user-minimal-v1.yaml`
- `admin-shared-v1` → `templates/admin-shared-v1.yaml`
- `admin-peruser-v1` → `templates/admin-peruser-v1.yaml`

Matching preference docs:

- `preferences/user-gamification-v1.md`
- `preferences/user-minimal-v1.md`
- `preferences/admin-shared-v1.md`
- `preferences/admin-peruser-v1.md`

Template IDs are immutable once published; new behavior variants should ship as new IDs.

## Manifest contract (schema v1)

Current required template fields in `dashboard_registry.json`:

- `template_id`
- `display_name`
- `description`
- `audience`
- `category`
- `lifecycle_state`
- `source.path`
- `preferences.doc_asset_path`

Optional metadata (not currently populated in the checked-in manifest):

- compatibility metadata
- dependency declarations

## Translation assets

- Dashboard translation assets are stored in `translations/`.
- File naming convention is `{lang}_dashboard.json` (for example `en_dashboard.json`, `fr_dashboard.json`).
- Translation bundles should stay schema-compatible and preserve key fallback behavior expected by integration runtime.

## Preference documentation

- Template preference guidance is stored in `preferences/`.
- Each template should have a corresponding preference document referenced by manifest preference metadata.
- Preference docs are user-facing and should document:
  - supported `pref_*` keys,
  - default values,
  - valid values/ranges,
  - card-level behavior notes when multiple cards consume preferences,
  - rebuild/overwrite caveats.

## Notes

- The ChoreOps integration will vendor a fallback copy of core templates for offline-safe generation.
- Remote registry content can override local fallback templates when available.

## Release versioning policy

This repository uses `v`-prefixed SemVer tags.

- Stable: `vX.Y.Z`
- Beta: `vX.Y.Z-beta.N`
- Release candidate: `vX.Y.Z-rc.N`
- Optional dev snapshot format: `vX.Y.Z-dev.YYYYMMDD+<shortsha>`

Published tags are immutable.

The dashboard registry and integration have independent version streams. Numeric version equality is not required.
Compatibility is tracked through release notes and the compatibility matrix, and verified through cross-repository testing.

## Compatibility matrix template

Record compatibility for each dashboard release in release notes or PR description.

| Integration release | Dashboard registry release | Channel | Compatibility status | Notes                               |
| ------------------- | -------------------------- | ------- | -------------------- | ----------------------------------- |
| `v0.5.0-beta.5`     | `v0.1.0-beta.1`            | beta    | verified             | Initial dashboard registry baseline |

Compatibility status values:

- `verified`: validated and supported
- `partial`: works with limitations documented
- `blocked`: incompatible pending fix

## Custom card policy

- This repository is for dashboard templates and registry metadata.
- It does not host custom card source code.
- Template dependencies can reference third-party cards and future ChoreOps-specific cards.
- If ChoreOps-specific cards are created, they should live in dedicated frontend card repositories with their own release lifecycle (for HACS/frontend distribution compatibility).

## Template submission workflow

1. Add or update template YAML assets under `templates/`.
2. Add or update matching records in `dashboard_registry.json`.
3. Confirm metadata is complete:

- required schema v1 fields (`template_id`, `display_name`, `description`, `audience`, `category`, `lifecycle_state`, `source.path`, `preferences.doc_asset_path`)
- optional compatibility/dependency metadata when needed for that release

4. Include concise release notes in the PR for user-visible behavior changes.

Minimum acceptance bar:

- Manifest and template assets validate cleanly.
- Naming and dependency identifier policies pass.
- Compatibility notes are provided when release impact exists.

## Contributing new dashboard templates

Pull requests for new dashboard templates are welcome.

For a new template PR, include all of the following:

1. A new template file in `templates/` with a versioned, immutable `template_id` (for example `user-badges-overview-v1`).
2. A matching entry in `dashboard_registry.json` with all required schema fields.
3. A matching preference guide in `preferences/` referenced by `preferences.doc_asset_path`.
4. Notes in the PR description covering audience, lifecycle state, and compatibility impact.

If you are unsure about scope or naming, open a discussion in the main repository (`ccpk1/ChoreOps`) and then submit a draft PR here.

## Dashboard development standards (required)

All dashboard template PRs must follow these standards:

- Canonical standards reference: [Dashboard Template Guide](https://github.com/ccpk1/choreops/blob/main/docs/DASHBOARD_TEMPLATE_GUIDE.md)

- **Dynamic, instance-aware lookup patterns only**
  - Always use dynamic lookup patterns for dashboard helper entities and related sensors.
  - Lookups must be integration-instance aware.
  - Do not manually construct or hardcode entity IDs.

- **Replacement field patterns are strict**
  - Follow established replacement field patterns exactly.
  - Do not introduce ad-hoc replacement token formats.

- **User-facing strings must use the translation sensor**
  - Obtain user-facing text via `ui()` translation lookups.
  - Reuse an existing translation key whenever possible.
  - If no suitable key exists, add it to dashboard English source translations (`translations/en_dashboard.json`) so the translation workflow can propagate additional languages.

- **Graceful error handling is required**
  - Validate required entities before building card content (for example dashboard helper, translation sensor, and core sensor references).
  - If required entities are missing, `unknown`, or `unavailable`, render a clear fallback guidance card and set a guard flag (for example `skip_render = true`).
  - Skip normal card rendering when guard validation fails.
  - Do not hard-fail the template renderer due to missing required entities.

## Review gates and approvals

- Template-only changes: maintainer approval.
- Schema/contract changes: architecture-owner sign-off required.
- PR gates must validate schema, naming, dependencies, and YAML parsing.

## Lifecycle policy

- `active`: selectable by default.
- `deprecated`: selectable with migration guidance.
- `archived`: not for new selections; retained for compatibility/migration context.

Deprecation requires a communication window and a documented replacement path.

## Release operations and branch policy

- Default contribution branch: `main`.
- Optional short-lived stabilization branches: `release/X.Y`.
- Dev artifacts are produced from `main` snapshots.
- Beta/stable artifacts are published from tagged commits.

Promotion flow:

1. Merge to `main`.
2. Publish dev snapshot for validation.
3. Publish beta tag when stabilization is needed.
4. Promote validated commit to stable tag.

## License

This project is licensed under the GPL-3.0 license. See [LICENSE](LICENSE).
