# ChoreOps Dashboards release checklist

Use this checklist before publishing dashboard registry releases.

## 1) Version and tag policy

- [ ] Use SemVer release versions without `v` prefix (`X.Y.Z`).
- [ ] For prerelease testing, use SemVer prerelease versions (`X.Y.Z-beta.N`, `X.Y.Z-rc.N`).
- [ ] Confirm channel intent is explicit: `beta` for validation, `stable` for production.

## 2) Content readiness

- [ ] `dashboard_registry.json` is valid JSON and reflects intended template set.
- [ ] Referenced template files exist under `templates/`.
- [ ] Referenced preference docs exist under `preferences/`.
- [ ] Translation files under `translations/` are present and syntactically valid.

## 3) Quality gates

Run and pass:

```bash
python utils/release_sanity.py --strict
python -m pytest -q
```

Checklist:

- [ ] No failing tests.
- [ ] Release sanity checks pass with no warnings.
- [ ] No temporary debug edits.
- [ ] Working tree is clean before tagging.

## 4) Publish release (GitHub UI)

- [ ] Open GitHub → Releases → Draft a new release.
- [ ] Create/select tag (example: `0.0.1-beta.1`) targeting `main`.
- [ ] Mark **Set as a pre-release** when publishing beta/rc.
- [ ] Generate notes or add concise release notes with compatibility intent.
- [ ] Publish release.

## 5) Post-release verification (generator path)

- [ ] Confirm release appears in GitHub Releases list.
- [ ] Confirm tag is discoverable via Releases API.
- [ ] Confirm generator can resolve the selected release tag.
- [ ] Confirm template fetch works from tagged snapshot paths (`raw.githubusercontent.com/.../{tag}/...`).
- [ ] Confirm fallback behavior expectations are documented for this release.

## 6) Cross-repository compatibility note

- [ ] Record tested pair in release notes or PR:
  - ChoreOps integration tag
  - ChoreOps-Dashboards release tag
  - Channel (`beta`/`stable`)
  - Outcome (`verified`/`partial`/`blocked`)

## Rollback readiness

- [ ] If release is invalid, delete GitHub release and remove tag.
- [ ] Publish corrected prerelease/stable tag with clear notes.
