---
name: ios-design-system-templates
description: Use when reference images, screenshots, moodboards, or iOS organism YAML should become a complete deterministic YAML inventory of iOS design-system templates. Invokes ios-design-system-organisms first, then extrapolates reusable screen, surface, flow, modal, state, and accessibility templates with strict no-null/no-empty/no-unknown validation.
compatibility: Requires access to the ios-design-system-organisms skill or an equivalent validated iOS organism YAML artifact. Optional validation uses Python 3.9+ with PyYAML or uv.
---

# iOS Design System Templates

## Goal

Generate every reusable iOS design-system template from reference images. The final artifact is always parser-valid YAML using the contract in `references/templates-yaml-contract.md`.

A template is a reusable screen-level, surface-level, or short flow blueprint composed from organisms: app shells, navigation stacks, tab roots, split views, list-detail structures, form flows, search/results layouts, feeds, dashboards, commerce surfaces, messaging surfaces, onboarding, authentication, settings, editors, empty/error states, modal sheets, permission flows, and system status surfaces. Templates are larger than organisms, but they are not complete applications, feature-specific user journeys, or business-specific screen copy.

## Non-Negotiables

- Start from reference images. If no reference images, screenshots, or moodboard is available, ask for input before generating templates.
- Invoke `ios-design-system-organisms` with the same reference images first. Use its validated YAML output as the organism source for template extrapolation.
- Final output must be YAML only unless the user explicitly asks for package maintenance, explanation, or files.
- Preserve the exact top-level order and required nested object shapes from `references/templates-yaml-contract.md`.
- Do not emit `null`, empty strings, empty lists, empty mappings, `undefined`, `unknown`, `missing`, `todo`, `tbd`, `n/a`, or placeholder values.
- Do not use wall-clock timestamps, random IDs, or run-dependent values. Derive IDs from stable source order, source filenames, visible evidence, organism YAML metadata, or a source fingerprint.
- If a template detail is not directly visible, derive it from the organism YAML and deterministic iOS platform defaults, then record the fallback in `provenance.decision_rule` with `confidence: low`.
- Every template object must include `anatomy`, `static`, `dynamic`, `organism_dependencies`, `composition`, `behavior`, `provenance`, `implementation`, and `qa` sections.
- Dynamic adaptations are required for every template: light/dark, accessibility, interaction state, device context, locale direction, motion context, data context, system material context, content variation context, navigation context, input modality context, and privacy or permission context.

## Workflow

Progress:
- [ ] Confirm reference input.
- [ ] Invoke iOS organism generation.
- [ ] Validate and normalize organism YAML.
- [ ] Extrapolate static templates.
- [ ] Extrapolate dynamic templates.
- [ ] Validate template YAML.

### 1. Confirm Reference Input

Proceed when the user supplies one of:

- attached reference images
- local image paths
- screenshots or moodboards
- validated YAML from `ios-design-system-organisms` plus the reference images used to create it

If multiple references are supplied, preserve their order. Assign deterministic source IDs as `ref_001`, `ref_002`, and so on.

### 2. Invoke iOS Organism Generation

Use `ios-design-system-organisms` with the same reference images. Ask for YAML only and require its native organism contract output.

The organism output becomes `dependency_bridge.ios_design_system_organisms.output_summary` and drives these template sections:

- `static_templates.app_shell_templates`, `navigation_stack_templates`, `tab_root_templates`, and `split_view_templates` from navigation scaffolds, tabbed surfaces, system chrome sections, list sections, detail sections, modal sheet sections, and accessibility organisms
- `static_templates.list_detail_templates`, `form_flow_templates`, `search_results_templates`, `settings_templates`, `authentication_templates`, and `permission_templates` from list sections, detail sections, form sections, search sections, settings sections, authentication sections, permission sections, feedback sections, and modal sheet sections
- `static_templates.feed_templates`, `content_collection_templates`, `media_gallery_templates`, `profile_templates`, and `dashboard_templates` from feed sections, content collection sections, media sections, profile sections, dashboard sections, empty state sections, feedback sections, and state organisms
- `static_templates.commerce_templates`, `messaging_templates`, `onboarding_templates`, `editor_templates`, `modal_sheet_templates`, `empty_state_templates`, `feedback_templates`, and `system_status_templates` from commerce sections, messaging sections, onboarding sections, editor sections, modal sheet sections, empty state sections, feedback sections, permission sections, and system chrome sections
- `dynamic_templates` from organism dynamic adaptations, state organisms, accessibility organisms, composition rules, and deterministic iOS platform behavior

If the organism skill cannot run and no validated organism YAML was supplied with matching references, stop and explain the blocked dependency. Do not invent organism evidence.

### 3. Normalize Organism Evidence

Before writing templates, create a stable source fingerprint:

1. Prefer the organism YAML `determinism.source_fingerprint`.
2. Otherwise prefer SHA-256 of ordered reference image bytes when local files are available.
3. Otherwise hash ordered source IDs, filenames, dimensions if known, and organism YAML metadata.
4. Use the first 12 lowercase hex characters in `determinism.source_fingerprint`.

Separate direct visual evidence, organism-derived evidence, molecule-trace evidence, atom-trace evidence, deterministic iOS defaults, and extrapolated values in each template's `provenance` object.

### 4. Generate Template Inventory

Read `references/templates-yaml-contract.md` before producing final YAML.

Create all required static template categories:

- `app_shell_templates`
- `navigation_stack_templates`
- `tab_root_templates`
- `split_view_templates`
- `list_detail_templates`
- `form_flow_templates`
- `search_results_templates`
- `feed_templates`
- `detail_templates`
- `media_gallery_templates`
- `profile_templates`
- `dashboard_templates`
- `commerce_templates`
- `messaging_templates`
- `onboarding_templates`
- `authentication_templates`
- `settings_templates`
- `editor_templates`
- `content_collection_templates`
- `empty_state_templates`
- `feedback_templates`
- `modal_sheet_templates`
- `permission_templates`
- `system_status_templates`

Use deterministic template IDs:

```text
template.<category>.<role>.<variant>
```

Examples:

```text
template.app_shell_templates.primary.tabbed
template.form_flow_templates.settings.editable
template.search_results_templates.scoped.results
```

Every template must include direct organism dependencies by ID, composition rules, SwiftUI and UIKit implementation mappings, state behavior, accessibility behavior, QA assertions, and fallback behavior.

### 5. Generate Dynamic Adaptations

Create every required dynamic template section:

- `color_scheme_adaptations`
- `accessibility_adaptations`
- `interaction_state_adaptations`
- `device_context_adaptations`
- `locale_context_adaptations`
- `motion_context_adaptations`
- `data_context_adaptations`
- `system_material_adaptations`
- `content_variation_adaptations`
- `navigation_context_adaptations`
- `input_modality_adaptations`
- `privacy_permission_adaptations`

Each dynamic section must specify:

- `rule_id`
- `affected_template_categories`
- `affected_organism_categories`
- `default_behavior`
- `variants`
- `implementation_notes`

Variants must be concrete and non-empty. If the references do not show a variant, derive it from the organism YAML and record that derivation.

### 6. Validate

When shell tools are available, draft the YAML to a temporary file and run:

```bash
python3 scripts/validate-ios-templates-yaml.py /tmp/ios-design-system-templates.yaml
```

If PyYAML is unavailable, run:

```bash
uv run scripts/validate-ios-templates-yaml.py /tmp/ios-design-system-templates.yaml
```

Fix all reported errors before returning or saving the artifact. If validation cannot run, manually check every item in `quality_gates.validation_checks` and report the limitation.

## Gotchas

- Do not treat template generation as a business-specific screen inventory. Templates are reusable screen, surface, or short-flow blueprints that can appear across products.
- Do not duplicate organism, molecule, or atom values inline when organism IDs can be referenced. Template YAML should compose organisms, not replace them.
- Do not use `"unknown"` for weak evidence. Choose a deterministic fallback, lower the confidence, and explain the rule.
- Do not emit empty optional-looking structures. If a section is required, it must contain at least one concrete value.
- Do not include complete apps, long user journeys across many product states, implementation-only services, analytics plans, or business-specific page copy as templates.
- Do not add top-level sections for convenience. Put additions under the nearest existing mapping using snake_case keys.

## Support Files

- `references/templates-yaml-contract.md`: canonical YAML schema, key order, template object shape, category requirements, and deterministic fallback rules.
- `scripts/validate-ios-templates-yaml.py`: mechanical YAML validation for top-level order, required nested fields, template object shape, confidence values, and banned placeholder values.
