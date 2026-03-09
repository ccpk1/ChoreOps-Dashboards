# admin-shared-v1 preferences

`admin-shared-v1` is the shared admin approval board. It shows every user who currently has pending chore or reward approvals, with each user rendered as a compact lane of actionable approval rows.

## Quick overview

- Shared board layout: all users with pending approvals are shown together in one admin view.
- Lane-based review flow: each user gets a summary header plus stacked approval rows.
- Portable row structure: approval rows are fully self-contained button-card definitions rather than depending on a separate shared row template.
- Collapsible Approval Center: the top summary header supports persisted collapse state.
- This document covers the supported template-level `pref_*` surface only.

## Card: Approval Center

- `pref_ui_control_key_root` (default: `admin-shared/approval-center`)
  - Sets the `ui_control` branch used by the shared Approval Center header.
  - Override this only when you intentionally want another shared-admin instance to store its collapse state separately.
  - Example custom values: `admin-shared/approval-center`, `admin-shared/approval-center-compact`, `dashboards/admin/main/approval-center`.
  - Use slash-delimited segments without relying on a leading slash.

- `pref_default_header_collapsed` (default: `false`)
  - Sets the default Approval Center header state when no persisted UI override exists.
  - `false` means expanded by default.
  - `true` means collapsed by default.
  - If pending approvals exist, the template currently prefers opening the header unless a stored override is already present.
  - Allowed: `true`, `false`.

- `pref_primary_tint_mix_pct` (default: `14`)
  - Controls the percent of `var(--primary-color)` mixed into the collapsed Approval Center header background and border treatment.
  - Higher values create a stronger collapsed-state tint.
  - Allowed: integer from `0` to `100`.

- `pref_show_header_background` (default: `true`)
  - Controls whether the collapsed Approval Center header uses a tinted background fill.
  - Expanded state continues to use the template's admin-specific surfaced styling.
  - Allowed: `true`, `false`.

- `pref_show_header_thin_border` (default: `true`)
  - Controls whether the collapsed Approval Center header shows the thin full border treatment.
  - Expanded state continues to use the template's admin-specific surfaced styling.
  - Allowed: `true`, `false`.

Recommended ranges:

- `0` = no primary tint in collapsed state
- `10` to `18` = subtle themed tint
- `25+` = much stronger collapsed-state emphasis

- Approval Center header collapse state
  - The shared Approval Center header supports a persisted collapse toggle.
  - The template uses the branch from `pref_ui_control_key_root` and stores the state at `header-collapse` under that root.
  - Expanding from a stored collapsed state removes the saved override so the card falls back to the template default behavior.
  - This state is stored through `choreops.manage_ui_control` using the shared helper context.
