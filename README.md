# ChoreOps Dashboards

Dashboard template registry for ChoreOps.

This repository is the dedicated source for Lovelace dashboard templates used by the ChoreOps integration. It is designed to support a dual-repository model where:

- `ccpk1/choreops` provides integration/backend logic
- `ccpk1/choreops-dashboards` provides dashboard manifests and template YAML assets

## Purpose

- Publish dashboard template updates independently from integration releases
- Enable safe hotfixes for UI/template issues
- Provide a registry contract (`manifest.json`) for dynamic template discovery

## Planned repository layout

```text
.
├── manifest.json              # Dashboard registry contract
├── templates/                 # Dashboard YAML templates
│   ├── dashboard_full.yaml
│   ├── dashboard_minimal.yaml
│   ├── dashboard_compact.yaml
│   └── dashboard_admin.yaml
└── docs/                      # Optional docs for template authors
```

## Notes

- The ChoreOps integration will vendor a fallback copy of core templates for offline-safe generation.
- Remote registry content can override local fallback templates when available.

## License

This project is licensed under the GPL-3.0 license. See [LICENSE](LICENSE).
