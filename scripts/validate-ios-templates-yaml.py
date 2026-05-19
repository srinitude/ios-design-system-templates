#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0,<7"
# ]
# ///
"""Validate an iOS design-system template YAML artifact.

Usage:
  python3 scripts/validate-ios-templates-yaml.py path/to/templates.yaml
  uv run scripts/validate-ios-templates-yaml.py path/to/templates.yaml --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:  # pragma: no cover - environment dependent
    print(
        "Error: PyYAML is required. Try: uv run scripts/validate-ios-templates-yaml.py <file>",
        file=sys.stderr,
    )
    sys.exit(2)


TOP_LEVEL_KEYS = [
    "schema_version",
    "artifact_type",
    "artifact_id",
    "determinism",
    "source_inputs",
    "dependency_bridge",
    "ios_context",
    "template_taxonomy",
    "organism_inputs",
    "static_templates",
    "dynamic_templates",
    "state_templates",
    "accessibility_templates",
    "composition_rules",
    "implementation",
    "quality_gates",
    "change_log",
]

STATIC_CATEGORIES = [
    "app_shell_templates",
    "navigation_stack_templates",
    "tab_root_templates",
    "split_view_templates",
    "list_detail_templates",
    "form_flow_templates",
    "search_results_templates",
    "feed_templates",
    "detail_templates",
    "media_gallery_templates",
    "profile_templates",
    "dashboard_templates",
    "commerce_templates",
    "messaging_templates",
    "onboarding_templates",
    "authentication_templates",
    "settings_templates",
    "editor_templates",
    "content_collection_templates",
    "empty_state_templates",
    "feedback_templates",
    "modal_sheet_templates",
    "permission_templates",
    "system_status_templates",
]

DYNAMIC_CATEGORIES = [
    "color_scheme_adaptations",
    "accessibility_adaptations",
    "interaction_state_adaptations",
    "device_context_adaptations",
    "locale_context_adaptations",
    "motion_context_adaptations",
    "data_context_adaptations",
    "system_material_adaptations",
    "content_variation_adaptations",
    "navigation_context_adaptations",
    "input_modality_adaptations",
    "privacy_permission_adaptations",
]

TEMPLATE_REQUIRED_KEYS = [
    "id",
    "name",
    "category",
    "role",
    "anatomy",
    "static",
    "dynamic",
    "organism_dependencies",
    "composition",
    "behavior",
    "provenance",
    "implementation",
    "qa",
]

ANATOMY_REQUIRED_KEYS = [
    "organism_regions",
    "required_organisms",
    "optional_organisms",
    "organism_slots",
    "content_regions",
    "navigation_regions",
    "state_regions",
    "presentation_regions",
]

STATIC_REQUIRED_KEYS = [
    "layout",
    "sizing",
    "spacing",
    "typography",
    "color",
    "shape",
    "stroke",
    "elevation",
    "material",
    "iconography",
    "imagery",
    "copy",
    "motion",
    "haptics",
    "sound",
    "z_index",
    "content_rules",
    "constraints",
]

DYNAMIC_REQUIRED_KEYS = [
    "color_scheme",
    "accessibility",
    "interaction_state",
    "device_context",
    "locale_context",
    "motion_context",
    "data_context",
    "system_material_context",
    "content_variation_context",
    "navigation_context",
    "input_modality_context",
    "privacy_permission_context",
]

ORGANISM_DEPENDENCIES_REQUIRED_KEYS = ["required", "conditional", "fallback"]
COMPOSITION_REQUIRED_KEYS = [
    "organism_mapping",
    "layout_formula",
    "state_binding",
    "variant_strategy",
    "reuse_boundary",
    "containment_rule",
    "template_boundary",
]
BEHAVIOR_REQUIRED_KEYS = [
    "entry_actions",
    "exit_actions",
    "transitions",
    "data_requirements",
    "error_recovery",
    "persistence_policy",
]
PROVENANCE_REQUIRED_KEYS = [
    "organism_source",
    "molecule_trace",
    "atom_trace",
    "visual_evidence",
    "confidence",
    "decision_rule",
]
IMPLEMENTATION_REQUIRED_KEYS = ["swiftui", "uikit", "token_name", "file_targets", "handoff_notes"]
QA_REQUIRED_KEYS = ["assertions", "snapshot_states", "interaction_tests", "failure_mode"]

SOURCE_INPUTS_REQUIRED_KEYS = ["reference_set_id", "references", "source_ordering", "evidence_limitations"]
REFERENCE_REQUIRED_KEYS = ["source_id", "source_type", "stable_label", "evidence_role", "fingerprint_component"]
IOS_CONTEXT_REQUIRED_KEYS = [
    "platform",
    "minimum_target",
    "implementation_surfaces",
    "device_classes",
    "color_schemes",
    "accessibility_contexts",
    "interaction_contexts",
    "navigation_contexts",
    "presentation_contexts",
]
TEMPLATE_TAXONOMY_REQUIRED_KEYS = [
    "definition",
    "boundary_rule",
    "required_static_categories",
    "required_dynamic_categories",
    "template_object_required_keys",
]
DEPENDENCY_RESOLUTION_REQUIRED_KEYS = ["organism_id_rule", "fallback_rule"]
COMPOSITION_RULES_REQUIRED_KEYS = [
    "organism_reference_policy",
    "template_boundary_policy",
    "variant_generation_policy",
    "accessibility_policy",
    "layout_policy",
    "state_policy",
]
TOKEN_NAMING_REQUIRED_KEYS = ["swiftui_type_prefix", "swift_identifier_style", "yaml_identifier_style"]
EXPORT_TARGET_REQUIRED_KEYS = ["target", "format", "naming_rule"]
FILE_PLAN_REQUIRED_KEYS = ["path", "purpose"]
QUALITY_GATES_REQUIRED_KEYS = ["validation_checks", "completeness_claim", "residual_risks"]
CHANGE_LOG_ENTRY_REQUIRED_KEYS = ["change_id", "description", "source_fingerprint", "deterministic"]

STATE_TEMPLATE_KEYS = [
    "enabled",
    "loading",
    "empty",
    "error",
    "success",
    "editing",
    "refreshing",
    "paginating",
    "filtering",
    "selecting",
    "expanded",
    "collapsed",
    "offline",
    "permission_denied",
    "unauthenticated",
]

ACCESSIBILITY_TEMPLATE_KEYS = [
    "dynamic_type",
    "increase_contrast",
    "reduce_motion",
    "reduce_transparency",
    "voiceover",
    "switch_control",
    "large_content_viewer",
    "bold_text",
    "keyboard_navigation",
    "differentiate_without_color",
    "voice_control",
    "display_zoom",
    "assistive_access",
]

CONFIDENCE_VALUES = {"low", "medium", "high"}
BANNED_STRINGS = {
    "",
    "null",
    "none",
    "undefined",
    "unknown",
    "missing",
    "todo",
    "tbd",
    "n/a",
    "na",
    "not_applicable",
    "not applicable",
    "not-available",
    "placeholder",
}
FINGERPRINT_RE = re.compile(r"^[0-9a-f]{12}$")


class UniqueKeyLoader(yaml.SafeLoader):
    """YAML loader that rejects duplicate keys."""


def construct_mapping(loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping,
)


def dotted(path: Iterable[Any]) -> str:
    rendered = "$"
    for part in path:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered


def require_mapping(value: Any, path: list[Any], errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{dotted(path)} must be a mapping")
        return False
    return True


def require_keys(mapping: dict[str, Any], keys: list[str], path: list[Any], errors: list[str], exact: bool = False) -> None:
    actual = list(mapping.keys())
    missing = [key for key in keys if key not in mapping]
    if missing:
        errors.append(f"{dotted(path)} missing required keys: {', '.join(missing)}")
    if exact and actual != keys:
        errors.append(f"{dotted(path)} key order mismatch: expected {keys}, got {actual}")


def walk_no_placeholders(value: Any, path: list[Any], errors: list[str]) -> None:
    if value is None:
        errors.append(f"{dotted(path)} must not be null")
        return
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in BANNED_STRINGS:
            errors.append(f"{dotted(path)} has banned placeholder value {value!r}")
        if value.strip() != value:
            errors.append(f"{dotted(path)} has leading or trailing whitespace")
        return
    if isinstance(value, list):
        if not value:
            errors.append(f"{dotted(path)} must not be an empty list")
        for index, item in enumerate(value):
            walk_no_placeholders(item, [*path, index], errors)
        return
    if isinstance(value, dict):
        if not value:
            errors.append(f"{dotted(path)} must not be an empty mapping")
        for key, item in value.items():
            if not isinstance(key, str):
                errors.append(f"{dotted(path)} contains non-string key {key!r}")
            elif not key or key.strip().lower() in BANNED_STRINGS:
                errors.append(f"{dotted(path)} contains banned key {key!r}")
            walk_no_placeholders(item, [*path, key], errors)


def validate_template(template: Any, path: list[Any], expected_category: str, errors: list[str]) -> None:
    if not require_mapping(template, path, errors):
        return
    require_keys(template, TEMPLATE_REQUIRED_KEYS, path, errors)
    if template.get("category") != expected_category:
        errors.append(f"{dotted(path)} category must be {expected_category!r}")
    template_id = template.get("id")
    if isinstance(template_id, str) and not template_id.startswith(f"template.{expected_category}."):
        errors.append(f"{dotted([*path, 'id'])} must start with 'template.{expected_category}.'")

    anatomy = template.get("anatomy")
    if require_mapping(anatomy, [*path, "anatomy"], errors):
        require_keys(anatomy, ANATOMY_REQUIRED_KEYS, [*path, "anatomy"], errors)

    static = template.get("static")
    if require_mapping(static, [*path, "static"], errors):
        require_keys(static, STATIC_REQUIRED_KEYS, [*path, "static"], errors)

    dynamic = template.get("dynamic")
    if require_mapping(dynamic, [*path, "dynamic"], errors):
        require_keys(dynamic, DYNAMIC_REQUIRED_KEYS, [*path, "dynamic"], errors)

    organism_dependencies = template.get("organism_dependencies")
    if require_mapping(organism_dependencies, [*path, "organism_dependencies"], errors):
        require_keys(
            organism_dependencies,
            ORGANISM_DEPENDENCIES_REQUIRED_KEYS,
            [*path, "organism_dependencies"],
            errors,
        )

    composition = template.get("composition")
    if require_mapping(composition, [*path, "composition"], errors):
        require_keys(composition, COMPOSITION_REQUIRED_KEYS, [*path, "composition"], errors)

    behavior = template.get("behavior")
    if require_mapping(behavior, [*path, "behavior"], errors):
        require_keys(behavior, BEHAVIOR_REQUIRED_KEYS, [*path, "behavior"], errors)

    provenance = template.get("provenance")
    if require_mapping(provenance, [*path, "provenance"], errors):
        require_keys(provenance, PROVENANCE_REQUIRED_KEYS, [*path, "provenance"], errors)
        confidence = provenance.get("confidence")
        if confidence not in CONFIDENCE_VALUES:
            errors.append(f"{dotted([*path, 'provenance', 'confidence'])} must be one of {sorted(CONFIDENCE_VALUES)}")

    implementation = template.get("implementation")
    if require_mapping(implementation, [*path, "implementation"], errors):
        require_keys(implementation, IMPLEMENTATION_REQUIRED_KEYS, [*path, "implementation"], errors)

    qa = template.get("qa")
    if require_mapping(qa, [*path, "qa"], errors):
        require_keys(qa, QA_REQUIRED_KEYS, [*path, "qa"], errors)


def validate_static_templates(root: dict[str, Any], errors: list[str]) -> None:
    static_templates = root.get("static_templates")
    if not require_mapping(static_templates, ["static_templates"], errors):
        return
    require_keys(static_templates, STATIC_CATEGORIES, ["static_templates"], errors)
    for category in STATIC_CATEGORIES:
        section = static_templates.get(category)
        path = ["static_templates", category]
        if not require_mapping(section, path, errors):
            continue
        require_keys(section, ["summary", "templates"], path, errors)
        templates = section.get("templates")
        if not isinstance(templates, list):
            errors.append(f"{dotted([*path, 'templates'])} must be a list")
            continue
        if not templates:
            errors.append(f"{dotted([*path, 'templates'])} must not be empty")
            continue
        for index, template in enumerate(templates):
            validate_template(template, [*path, "templates", index], category, errors)


def validate_dynamic_templates(root: dict[str, Any], errors: list[str]) -> None:
    dynamic_templates = root.get("dynamic_templates")
    if not require_mapping(dynamic_templates, ["dynamic_templates"], errors):
        return
    require_keys(dynamic_templates, DYNAMIC_CATEGORIES, ["dynamic_templates"], errors)
    for category in DYNAMIC_CATEGORIES:
        section = dynamic_templates.get(category)
        path = ["dynamic_templates", category]
        if not require_mapping(section, path, errors):
            continue
        require_keys(
            section,
            [
                "rule_id",
                "affected_template_categories",
                "affected_organism_categories",
                "default_behavior",
                "variants",
                "implementation_notes",
            ],
            path,
            errors,
        )
        variants = section.get("variants")
        if not isinstance(variants, list) or not variants:
            errors.append(f"{dotted([*path, 'variants'])} must be a non-empty list")
            continue
        for index, variant in enumerate(variants):
            if not require_mapping(variant, [*path, "variants", index], errors):
                continue
            require_keys(
                variant,
                ["variant_id", "condition", "template_adjustments", "organism_adjustments", "qa_assertions"],
                [*path, "variants", index],
                errors,
            )


def validate_named_template_map(root: dict[str, Any], key: str, required_keys: list[str], errors: list[str]) -> None:
    section = root.get(key)
    if not require_mapping(section, [key], errors):
        return
    require_keys(section, required_keys, [key], errors)
    expected_category = "state" if key == "state_templates" else "accessibility"
    for template_key in required_keys:
        validate_template(section.get(template_key), [key, template_key], expected_category, errors)


def validate_source_inputs(root: dict[str, Any], errors: list[str]) -> None:
    source_inputs = root.get("source_inputs")
    if not require_mapping(source_inputs, ["source_inputs"], errors):
        return
    require_keys(source_inputs, SOURCE_INPUTS_REQUIRED_KEYS, ["source_inputs"], errors)
    references = source_inputs.get("references")
    if not isinstance(references, list) or not references:
        errors.append("$.source_inputs.references must be a non-empty list")
        return
    for index, reference in enumerate(references):
        path = ["source_inputs", "references", index]
        if require_mapping(reference, path, errors):
            require_keys(reference, REFERENCE_REQUIRED_KEYS, path, errors)


def validate_ios_context(root: dict[str, Any], errors: list[str]) -> None:
    ios_context = root.get("ios_context")
    if not require_mapping(ios_context, ["ios_context"], errors):
        return
    require_keys(ios_context, IOS_CONTEXT_REQUIRED_KEYS, ["ios_context"], errors)


def validate_template_taxonomy(root: dict[str, Any], errors: list[str]) -> None:
    taxonomy = root.get("template_taxonomy")
    if not require_mapping(taxonomy, ["template_taxonomy"], errors):
        return
    require_keys(taxonomy, TEMPLATE_TAXONOMY_REQUIRED_KEYS, ["template_taxonomy"], errors)
    if taxonomy.get("required_static_categories") != STATIC_CATEGORIES:
        errors.append("$.template_taxonomy.required_static_categories must match the contract static category order")
    if taxonomy.get("required_dynamic_categories") != DYNAMIC_CATEGORIES:
        errors.append("$.template_taxonomy.required_dynamic_categories must match the contract dynamic category order")
    if taxonomy.get("template_object_required_keys") != TEMPLATE_REQUIRED_KEYS:
        errors.append("$.template_taxonomy.template_object_required_keys must match the contract template object key order")


def validate_composition_rules(root: dict[str, Any], errors: list[str]) -> None:
    composition_rules = root.get("composition_rules")
    if require_mapping(composition_rules, ["composition_rules"], errors):
        require_keys(composition_rules, COMPOSITION_RULES_REQUIRED_KEYS, ["composition_rules"], errors)


def validate_implementation(root: dict[str, Any], errors: list[str]) -> None:
    implementation = root.get("implementation")
    if not require_mapping(implementation, ["implementation"], errors):
        return
    require_keys(implementation, ["token_naming", "export_targets", "file_plan", "dependency_order"], ["implementation"], errors)

    token_naming = implementation.get("token_naming")
    if require_mapping(token_naming, ["implementation", "token_naming"], errors):
        require_keys(token_naming, TOKEN_NAMING_REQUIRED_KEYS, ["implementation", "token_naming"], errors)

    export_targets = implementation.get("export_targets")
    if not isinstance(export_targets, list) or not export_targets:
        errors.append("$.implementation.export_targets must be a non-empty list")
    else:
        for index, export_target in enumerate(export_targets):
            path = ["implementation", "export_targets", index]
            if require_mapping(export_target, path, errors):
                require_keys(export_target, EXPORT_TARGET_REQUIRED_KEYS, path, errors)

    file_plan = implementation.get("file_plan")
    if not isinstance(file_plan, list) or not file_plan:
        errors.append("$.implementation.file_plan must be a non-empty list")
    else:
        for index, file_entry in enumerate(file_plan):
            path = ["implementation", "file_plan", index]
            if require_mapping(file_entry, path, errors):
                require_keys(file_entry, FILE_PLAN_REQUIRED_KEYS, path, errors)


def validate_quality_gates(root: dict[str, Any], errors: list[str]) -> None:
    quality_gates = root.get("quality_gates")
    if require_mapping(quality_gates, ["quality_gates"], errors):
        require_keys(quality_gates, QUALITY_GATES_REQUIRED_KEYS, ["quality_gates"], errors)


def validate_change_log(root: dict[str, Any], errors: list[str]) -> None:
    change_log = root.get("change_log")
    if not require_mapping(change_log, ["change_log"], errors):
        return
    require_keys(change_log, ["entries"], ["change_log"], errors)
    entries = change_log.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("$.change_log.entries must be a non-empty list")
        return
    for index, entry in enumerate(entries):
        path = ["change_log", "entries", index]
        if require_mapping(entry, path, errors):
            require_keys(entry, CHANGE_LOG_ENTRY_REQUIRED_KEYS, path, errors)
            fingerprint = entry.get("source_fingerprint")
            if not isinstance(fingerprint, str) or not FINGERPRINT_RE.match(fingerprint):
                errors.append(f"{dotted([*path, 'source_fingerprint'])} must be 12 lowercase hex characters")


def validate_metadata(root: dict[str, Any], errors: list[str]) -> None:
    if root.get("schema_version") != "1.0.0":
        errors.append("$.schema_version must be '1.0.0'")
    if root.get("artifact_type") != "ios_design_system_templates":
        errors.append("$.artifact_type must be 'ios_design_system_templates'")

    determinism = root.get("determinism")
    if require_mapping(determinism, ["determinism"], errors):
        require_keys(
            determinism,
            ["source_fingerprint", "ordering_rule", "id_rule", "timestamp_policy", "fallback_policy"],
            ["determinism"],
            errors,
        )
        fingerprint = determinism.get("source_fingerprint")
        if not isinstance(fingerprint, str) or not FINGERPRINT_RE.match(fingerprint):
            errors.append("$.determinism.source_fingerprint must be 12 lowercase hex characters")
        expected_artifact_id = f"ios_templates_{fingerprint}" if isinstance(fingerprint, str) else None
        if root.get("artifact_id") != expected_artifact_id:
            errors.append("$.artifact_id must be ios_templates_<source_fingerprint>")

    dependency_bridge = root.get("dependency_bridge")
    if require_mapping(dependency_bridge, ["dependency_bridge"], errors):
        bridge = dependency_bridge.get("ios_design_system_organisms")
        if require_mapping(bridge, ["dependency_bridge", "ios_design_system_organisms"], errors):
            require_keys(
                bridge,
                [
                    "invocation_required",
                    "skill_name",
                    "output_status",
                    "source_artifact_type",
                    "source_artifact_id",
                    "source_fingerprint",
                    "output_summary",
                    "mapping_rules",
                ],
                ["dependency_bridge", "ios_design_system_organisms"],
                errors,
            )
            if bridge.get("skill_name") != "ios-design-system-organisms":
                errors.append("$.dependency_bridge.ios_design_system_organisms.skill_name must be 'ios-design-system-organisms'")
            bridge_fingerprint = bridge.get("source_fingerprint")
            if not isinstance(bridge_fingerprint, str) or not FINGERPRINT_RE.match(bridge_fingerprint):
                errors.append("$.dependency_bridge.ios_design_system_organisms.source_fingerprint must be 12 lowercase hex characters")
            output_summary = bridge.get("output_summary")
            if require_mapping(output_summary, ["dependency_bridge", "ios_design_system_organisms", "output_summary"], errors):
                require_keys(
                    output_summary,
                    ["strongest_organism_categories", "weakest_organism_categories", "template_derivation_rule"],
                    ["dependency_bridge", "ios_design_system_organisms", "output_summary"],
                    errors,
                )
            mapping_rules = bridge.get("mapping_rules")
            if not isinstance(mapping_rules, list) or not mapping_rules:
                errors.append("$.dependency_bridge.ios_design_system_organisms.mapping_rules must be a non-empty list")
            else:
                for index, mapping_rule in enumerate(mapping_rules):
                    path = ["dependency_bridge", "ios_design_system_organisms", "mapping_rules", index]
                    if require_mapping(mapping_rule, path, errors):
                        require_keys(mapping_rule, ["from_organism_category", "to_template_category", "rule"], path, errors)

    organism_inputs = root.get("organism_inputs")
    if require_mapping(organism_inputs, ["organism_inputs"], errors):
        require_keys(
            organism_inputs,
            [
                "organism_artifact_id",
                "organism_source_fingerprint",
                "required_organism_categories",
                "dependency_resolution",
            ],
            ["organism_inputs"],
            errors,
        )
        organism_fingerprint = organism_inputs.get("organism_source_fingerprint")
        if not isinstance(organism_fingerprint, str) or not FINGERPRINT_RE.match(organism_fingerprint):
            errors.append("$.organism_inputs.organism_source_fingerprint must be 12 lowercase hex characters")
        if organism_inputs.get("required_organism_categories") is not None:
            required_organisms = organism_inputs.get("required_organism_categories")
            if not isinstance(required_organisms, list) or not required_organisms:
                errors.append("$.organism_inputs.required_organism_categories must be a non-empty list")
        dependency_resolution = organism_inputs.get("dependency_resolution")
        if require_mapping(dependency_resolution, ["organism_inputs", "dependency_resolution"], errors):
            require_keys(dependency_resolution, DEPENDENCY_RESOLUTION_REQUIRED_KEYS, ["organism_inputs", "dependency_resolution"], errors)


def validate(data: bytes) -> list[str]:
    text = data.decode("utf-8")
    errors: list[str] = []
    if "\t" in text:
        errors.append("YAML must use spaces only; tabs found")
    if text.lstrip().startswith("```") or text.rstrip().endswith("```"):
        errors.append("YAML must not be wrapped in markdown fences")

    try:
        root = yaml.load(text, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        return [f"YAML parse error: {exc}"]

    if not isinstance(root, dict):
        return ["YAML root must be a mapping"]

    require_keys(root, TOP_LEVEL_KEYS, [], errors, exact=True)
    walk_no_placeholders(root, [], errors)
    validate_metadata(root, errors)
    validate_source_inputs(root, errors)
    validate_ios_context(root, errors)
    validate_template_taxonomy(root, errors)
    validate_static_templates(root, errors)
    validate_dynamic_templates(root, errors)
    validate_named_template_map(root, "state_templates", STATE_TEMPLATE_KEYS, errors)
    validate_named_template_map(root, "accessibility_templates", ACCESSIBILITY_TEMPLATE_KEYS, errors)
    validate_composition_rules(root, errors)
    validate_implementation(root, errors)
    validate_quality_gates(root, errors)
    validate_change_log(root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("yaml_file", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable validation output")
    args = parser.parse_args()

    errors = validate(args.yaml_file.read_bytes())
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    elif errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Validation passed")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
