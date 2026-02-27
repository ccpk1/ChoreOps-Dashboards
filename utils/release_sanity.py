#!/usr/bin/env python3
"""Release sanity checks for ChoreOps dashboard registry repository.

This script validates registry and translation JSON structure, verifies referenced
files exist, and runs lightweight template policy heuristics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "dashboard_registry.json"
TEMPLATES_DIR = REPO_ROOT / "templates"
PREFERENCES_DIR = REPO_ROOT / "preferences"
TRANSLATIONS_DIR = REPO_ROOT / "translations"

REQUIRED_TEMPLATE_KEYS = {
    "template_id",
    "display_name",
    "description",
    "audience",
    "category",
    "lifecycle_state",
    "source",
    "preferences",
    "dependencies",
    "maintainer",
    "min_integration_version",
}

REQUIRED_SOURCE_KEYS = {"type", "path"}
REQUIRED_PREFERENCES_KEYS = {"doc_asset_path"}
REQUIRED_DEPENDENCY_SECTIONS = {"required", "recommended"}

VALID_AUDIENCE = {"user", "approver", "mixed"}
VALID_SOURCE_TYPES = {"vendored", "remote"}
VALID_LIFECYCLE = {"active", "deprecated", "archived"}

HARDCODED_EID_RE = re.compile(
    r"\b(?:sensor|binary_sensor|button|select|input_boolean|input_text|"
    r"input_number|switch|number|event)\.(?:kc_|choreops_)[a-z0-9_]+\b"
)
TRANSLATION_SENSOR_RE = re.compile(r"translation_sensor(_eid)?")
UI_LOOKUP_RE = re.compile(r"\bui\.(?:get|\w+)\(")
MARKDOWN_CONTENT_RE = re.compile(r"['\"]content['\"]\s*:")


@dataclass(slots=True)
class CheckResult:
    errors: list[str]
    warnings: list[str]

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)


def _load_json(path: Path, result: CheckResult) -> Any:
    """Load JSON file and emit a structured error on parse issues."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.add_error(f"Missing required file: {path.relative_to(REPO_ROOT)}")
    except json.JSONDecodeError as err:
        result.add_error(
            "Invalid JSON in "
            f"{path.relative_to(REPO_ROOT)}: line={err.lineno} col={err.colno}"
        )
    except OSError as err:
        result.add_error(f"Unable to read {path.relative_to(REPO_ROOT)}: {err}")
    return None


def _validate_registry(result: CheckResult) -> dict[str, Any] | None:
    """Validate top-level registry shape and template records."""
    payload = _load_json(REGISTRY_PATH, result)
    if payload is None:
        return None

    if not isinstance(payload, dict):
        result.add_error("dashboard_registry.json must be a JSON object")
        return None

    templates = payload.get("templates")
    if not isinstance(templates, list):
        result.add_error("dashboard_registry.json must contain templates as a list")
        return None

    seen_template_ids: set[str] = set()
    for index, template in enumerate(templates):
        context = f"dashboard_registry.json templates[{index}]"
        if not isinstance(template, dict):
            result.add_error(f"{context}: record must be an object")
            continue

        missing_keys = sorted(REQUIRED_TEMPLATE_KEYS - set(template))
        if missing_keys:
            result.add_error(f"{context}: missing keys {missing_keys}")

        template_id = template.get("template_id")
        if not isinstance(template_id, str) or not template_id.strip():
            result.add_error(f"{context}: template_id must be a non-empty string")
            continue
        template_id = template_id.strip()
        if template_id in seen_template_ids:
            result.add_error(f"{context}: duplicate template_id '{template_id}'")
        seen_template_ids.add(template_id)

        audience = template.get("audience")
        if audience not in VALID_AUDIENCE:
            result.add_error(
                f"{context}: invalid audience '{audience}' (allowed: {sorted(VALID_AUDIENCE)})"
            )

        lifecycle = template.get("lifecycle_state")
        if lifecycle not in VALID_LIFECYCLE:
            result.add_error(
                f"{context}: invalid lifecycle_state "
                f"'{lifecycle}' (allowed: {sorted(VALID_LIFECYCLE)})"
            )

        source = template.get("source")
        if not isinstance(source, dict):
            result.add_error(f"{context}: source must be an object")
        else:
            missing_source_keys = sorted(REQUIRED_SOURCE_KEYS - set(source))
            if missing_source_keys:
                result.add_error(
                    f"{context}: source missing keys {missing_source_keys}"
                )

            source_type = source.get("type")
            source_path = source.get("path")
            if source_type not in VALID_SOURCE_TYPES:
                result.add_error(
                    f"{context}: source.type must be one of {sorted(VALID_SOURCE_TYPES)}"
                )

            if not isinstance(source_path, str) or not source_path.strip():
                result.add_error(f"{context}: source.path must be a non-empty string")
            else:
                source_file = REPO_ROOT / source_path
                if not source_file.exists():
                    result.add_error(
                        f"{context}: missing source.path file {source_path}"
                    )
                if not source_path.startswith("templates/"):
                    result.add_warning(
                        f"{context}: source.path should normally be under templates/ ({source_path})"
                    )

        preferences = template.get("preferences")
        if not isinstance(preferences, dict):
            result.add_error(f"{context}: preferences must be an object")
        else:
            missing_preferences_keys = sorted(
                REQUIRED_PREFERENCES_KEYS - set(preferences)
            )
            if missing_preferences_keys:
                result.add_error(
                    f"{context}: preferences missing keys {missing_preferences_keys}"
                )
            doc_asset_path = preferences.get("doc_asset_path")
            if not isinstance(doc_asset_path, str) or not doc_asset_path.strip():
                result.add_error(
                    f"{context}: preferences.doc_asset_path must be non-empty string"
                )
            else:
                preferences_file = REPO_ROOT / doc_asset_path
                if not preferences_file.exists():
                    result.add_error(
                        f"{context}: missing preferences doc {doc_asset_path}"
                    )
                if not doc_asset_path.startswith("preferences/"):
                    result.add_warning(
                        f"{context}: preferences.doc_asset_path should normally be under preferences/ ({doc_asset_path})"
                    )

        dependencies = template.get("dependencies")
        if not isinstance(dependencies, dict):
            result.add_error(f"{context}: dependencies must be an object")
        else:
            missing_sections = sorted(REQUIRED_DEPENDENCY_SECTIONS - set(dependencies))
            if missing_sections:
                result.add_error(
                    f"{context}: dependencies missing sections {missing_sections}"
                )
            for section in ("required", "recommended"):
                dep_values = dependencies.get(section)
                if not isinstance(dep_values, list):
                    result.add_error(
                        f"{context}: dependencies.{section} must be a list"
                    )

    return payload


def _validate_translation_files(result: CheckResult) -> None:
    """Validate translation JSON files are parseable objects."""
    if not TRANSLATIONS_DIR.exists():
        result.add_error("translations/ directory is missing")
        return

    translation_files = sorted(TRANSLATIONS_DIR.glob("*_dashboard.json"))
    if not translation_files:
        result.add_error("No translation files found in translations/")
        return

    for translation_file in translation_files:
        payload = _load_json(translation_file, result)
        if payload is None:
            continue
        if not isinstance(payload, dict):
            result.add_error(
                f"{translation_file.relative_to(REPO_ROOT)} must contain a JSON object"
            )


def _validate_template_policy(result: CheckResult) -> None:
    """Run lightweight template heuristics for common release regressions."""
    if not TEMPLATES_DIR.exists():
        result.add_error("templates/ directory is missing")
        return

    template_files = sorted(TEMPLATES_DIR.glob("*.yaml"))
    if not template_files:
        result.add_error("No template files found in templates/")
        return

    for template_file in template_files:
        relative_path = template_file.relative_to(REPO_ROOT)
        try:
            text = template_file.read_text(encoding="utf-8")
        except OSError as err:
            result.add_error(f"Unable to read {relative_path}: {err}")
            continue

        hardcoded_matches = HARDCODED_EID_RE.findall(text)
        if hardcoded_matches:
            filtered = sorted(
                {match for match in hardcoded_matches if not match.endswith("_")}
            )
            if filtered:
                result.add_warning(
                    f"{relative_path}: potential hardcoded entity IDs detected ({', '.join(filtered[:5])})"
                )

        has_markdown_content = MARKDOWN_CONTENT_RE.search(text) is not None
        has_translation_sensor = TRANSLATION_SENSOR_RE.search(text) is not None
        has_ui_lookup = UI_LOOKUP_RE.search(text) is not None

        if has_markdown_content and not (has_translation_sensor and has_ui_lookup):
            result.add_warning(
                f"{relative_path}: markdown content present without clear translation sensor/ui lookup pattern"
            )


def run_checks(strict: bool) -> int:
    """Run all release sanity checks and return process exit code."""
    result = CheckResult(errors=[], warnings=[])

    _validate_registry(result)
    _validate_translation_files(result)
    _validate_template_policy(result)

    if result.errors:
        print("❌ Errors")
        for error in result.errors:
            print(f"- {error}")

    if result.warnings:
        print("⚠️ Warnings")
        for warning in result.warnings:
            print(f"- {warning}")

    if not result.errors and not result.warnings:
        print("✅ release_sanity: all checks passed")
        return 0

    if result.errors:
        return 1

    return 1 if strict else 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run release sanity checks for ChoreOps dashboards"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures",
    )
    return parser.parse_args(argv)


def main() -> int:
    """Script entry point."""
    args = parse_args(sys.argv[1:])
    return run_checks(strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
