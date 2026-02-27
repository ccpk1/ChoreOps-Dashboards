## Summary

Describe what this PR changes.

## Standards reference

- Canonical authoring/process standards: [Dashboard Template Guide](https://github.com/ccpk1/choreops/blob/main/docs/DASHBOARD_TEMPLATE_GUIDE.md)

## Change type

- [ ] New dashboard template
- [ ] Template update/fix
- [ ] Registry metadata update
- [ ] Translation sync
- [ ] Documentation only

## Template submission checklist

If this PR adds a new dashboard template, confirm all required assets are included:

- [ ] Added a new versioned template file in `templates/`
- [ ] Added/updated matching `dashboard_registry.json` entry
- [ ] Added matching preference documentation in `preferences/`
- [ ] Verified `source.path` and `preferences.doc_asset_path` values are correct

## Required development standards

- [ ] Uses dynamic, integration-instance-aware lookup patterns for helper/sensor references
- [ ] Does not manually construct or hardcode entity IDs
- [ ] Follows replacement field patterns without custom token formats
- [ ] Uses `ui.get()` translation lookups for all user-facing strings, and format fallback as `err-<key>` for easy troubleshooting. i.e. `ui.get('done', 'err-done')`
- [ ] Reused existing translation keys where possible; added missing keys to `translations/en_dashboard.json` when required.
- [ ] Handles missing required entities gracefully with fallback messaging and skip-render guard behavior

## Compatibility notes

- [ ] No compatibility impact
- [ ] Compatibility impact documented below

Compatibility details:

<!-- Describe target ChoreOps versions and any known constraints. -->

## Validation

- [ ] YAML/JSON structure reviewed
- [ ] Paths and IDs reviewed for consistency
- [ ] Release notes included for user-visible changes
