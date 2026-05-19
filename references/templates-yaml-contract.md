# iOS Templates YAML Contract

Use this contract exactly when generating iOS design-system templates. The final artifact must be parser-valid YAML and must preserve the top-level key order below.

## Top-Level Key Order

1. `schema_version`
2. `artifact_type`
3. `artifact_id`
4. `determinism`
5. `source_inputs`
6. `dependency_bridge`
7. `ios_context`
8. `template_taxonomy`
9. `organism_inputs`
10. `static_templates`
11. `dynamic_templates`
12. `state_templates`
13. `accessibility_templates`
14. `composition_rules`
15. `implementation`
16. `quality_gates`
17. `change_log`

## Deterministic Metadata

Required shape:

```yaml
schema_version: "1.0.0"
artifact_type: "ios_design_system_templates"
artifact_id: "ios_templates_<source_fingerprint>"
determinism:
  source_fingerprint: "<12_lowercase_hex_chars>"
  ordering_rule: "preserve_reference_order_then_organism_order_then_contract_order"
  id_rule: "template.<category>.<role>.<variant>"
  timestamp_policy: "wall_clock_timestamps_are_not_emitted"
  fallback_policy: "derive_from_ios_organism_yaml_then_ios_platform_defaults"
```

Do not emit current timestamps, random IDs, or session-specific values.

## Source And Dependency Bridge

Required shape:

```yaml
source_inputs:
  reference_set_id: "refset_<source_fingerprint>"
  references:
    - source_id: "ref_001"
      source_type: "image"
      stable_label: "ordered_reference_001"
      evidence_role: "primary_visual_reference"
      fingerprint_component: "sha256_or_stable_descriptor"
  source_ordering: "user_supplied_order"
  evidence_limitations:
    - "values_not_directly_visible_are_derived_by_contract_fallbacks"
dependency_bridge:
  ios_design_system_organisms:
    invocation_required: true
    skill_name: "ios-design-system-organisms"
    output_status: "validated_yaml_received"
    source_artifact_type: "ios_design_system_organisms"
    source_artifact_id: "ios_organisms_<source_fingerprint>"
    source_fingerprint: "<12_lowercase_hex_chars>"
    output_summary:
      strongest_organism_categories:
        - "navigation_scaffolds"
      weakest_organism_categories:
        - "commerce_sections"
      template_derivation_rule: "compose_templates_from_organism_ids_before_fallback_defaults"
    mapping_rules:
      - from_organism_category: "navigation_scaffolds"
        to_template_category: "navigation_stack_templates"
        rule: "map_navigation_stack_split_view_and_modal_scaffolds_to_reusable_screen_templates"
```

If a weak organism category is not visible, keep it in `weakest_organism_categories` and fill template values through the fallback policy.

## iOS Context

Required shape:

```yaml
ios_context:
  platform: "ios"
  minimum_target: "ios_17"
  implementation_surfaces:
    - "swiftui"
    - "uikit"
  device_classes:
    - "iphone_compact"
    - "iphone_regular"
    - "ipad_regular"
  color_schemes:
    - "light"
    - "dark"
  accessibility_contexts:
    - "dynamic_type"
    - "increase_contrast"
    - "reduce_motion"
    - "reduce_transparency"
    - "voiceover"
    - "switch_control"
    - "large_content_viewer"
  interaction_contexts:
    - "touch"
    - "pointer"
    - "keyboard"
  navigation_contexts:
    - "push_stack"
    - "tab_switch"
    - "sheet_presented"
    - "split_view"
  presentation_contexts:
    - "root_surface"
    - "pushed_destination"
    - "modal_sheet"
    - "popover"
```

These values are deterministic platform defaults unless the user specifies a narrower iOS target.

## Template Taxonomy

Required shape:

```yaml
template_taxonomy:
  definition: "reusable_ios_screen_surface_or_short_flow_blueprint_composed_from_design_organisms"
  boundary_rule: "templates_are_larger_than_organisms_and_smaller_than_complete_apps_product_specific_journeys_or_business_workflows"
  required_static_categories:
    - "app_shell_templates"
    - "navigation_stack_templates"
    - "tab_root_templates"
    - "split_view_templates"
    - "list_detail_templates"
    - "form_flow_templates"
    - "search_results_templates"
    - "feed_templates"
    - "detail_templates"
    - "media_gallery_templates"
    - "profile_templates"
    - "dashboard_templates"
    - "commerce_templates"
    - "messaging_templates"
    - "onboarding_templates"
    - "authentication_templates"
    - "settings_templates"
    - "editor_templates"
    - "content_collection_templates"
    - "empty_state_templates"
    - "feedback_templates"
    - "modal_sheet_templates"
    - "permission_templates"
    - "system_status_templates"
  required_dynamic_categories:
    - "color_scheme_adaptations"
    - "accessibility_adaptations"
    - "interaction_state_adaptations"
    - "device_context_adaptations"
    - "locale_context_adaptations"
    - "motion_context_adaptations"
    - "data_context_adaptations"
    - "system_material_adaptations"
    - "content_variation_adaptations"
    - "navigation_context_adaptations"
    - "input_modality_adaptations"
    - "privacy_permission_adaptations"
  template_object_required_keys:
    - "id"
    - "name"
    - "category"
    - "role"
    - "anatomy"
    - "static"
    - "dynamic"
    - "organism_dependencies"
    - "composition"
    - "behavior"
    - "provenance"
    - "implementation"
    - "qa"
```

## Organism Inputs

Required shape:

```yaml
organism_inputs:
  organism_artifact_id: "ios_organisms_<source_fingerprint>"
  organism_source_fingerprint: "<12_lowercase_hex_chars>"
  required_organism_categories:
    - "navigation_scaffolds"
    - "tabbed_surfaces"
    - "system_chrome_sections"
    - "list_sections"
    - "form_sections"
    - "search_sections"
    - "feed_sections"
    - "detail_sections"
    - "media_sections"
    - "profile_sections"
    - "dashboard_sections"
    - "commerce_sections"
    - "messaging_sections"
    - "onboarding_sections"
    - "authentication_sections"
    - "settings_sections"
    - "editor_sections"
    - "content_collection_sections"
    - "empty_state_sections"
    - "feedback_sections"
    - "modal_sheet_sections"
    - "permission_sections"
  dependency_resolution:
    organism_id_rule: "reference_existing_organism_ids_without_redefining_organism_values"
    fallback_rule: "use_contract_defined_ios_defaults_when_organism_category_has_low_confidence"
```

## Static Template Categories

`static_templates` must contain every required static category. Each category must use this shape:

```yaml
static_templates:
  app_shell_templates:
    summary: "reusable_root_level_application_surfaces_that_coordinate_navigation_tabs_chrome_and_safe_areas"
    templates:
      - id: "template.app_shell_templates.primary.tabbed"
        name: "primary_tabbed_app_shell"
        category: "app_shell_templates"
        role: "primary_tabbed_app_shell"
        anatomy:
          organism_regions:
            - region_id: "root_navigation"
              required: true
              organism_refs:
                - "organism.navigation_scaffolds.stack.primary"
                - "organism.tabbed_surfaces.tab_bar.primary"
          required_organisms:
            - "organism.navigation_scaffolds.stack.primary"
            - "organism.system_chrome_sections.safe_area.primary"
          optional_organisms:
            - "organism.search_sections.scoped_search.standard"
          organism_slots:
            - slot_id: "primary_content_template_region"
              accepts:
                - "feed_sections"
                - "list_sections"
                - "dashboard_sections"
              required: true
          content_regions:
            - region_id: "selected_tab_content"
              content_type: "template_owned_content_surface"
              required: true
          navigation_regions:
            - region_id: "root_route_stack"
              transition_style: "push_or_tab_switch"
              required: true
          state_regions:
            - region_id: "global_status_feedback"
              state_source: "state_templates.loading"
              required: true
          presentation_regions:
            - region_id: "modal_presentation_surface"
              presentation_style: "sheet_or_full_screen_cover"
              required: true
        static:
          layout:
            axis: "vertical"
            alignment: "fill"
            distribution: "system_chrome_then_navigation_then_selected_content"
          sizing:
            minimum_touch_target: "44x44pt"
            safe_area_rule: "respect_top_bottom_keyboard_and_dynamic_island_safe_areas"
            width_rule: "fills_available_window_width"
          spacing:
            section_gap_token: "organism.system_chrome_sections.safe_area.primary"
            content_inset_rule: "derive_from_root_navigation_and_selected_content_organisms"
          typography:
            title_source: "organism.navigation_scaffolds.stack.primary"
            scaling_rule: "dynamic_type_uses_accessibility_template_rules"
          color:
            background_source: "organism.system_chrome_sections.safe_area.primary"
            foreground_rule: "inherit_foreground_from_visible_child_organisms"
          shape:
            container_shape_rule: "root_surface_uses_platform_window_shape"
            clipping_rule: "clip_only_modal_popover_and_overlay_presentation_regions"
          stroke:
            separator_source: "organism.tabbed_surfaces.tab_bar.primary"
            focus_ring_rule: "defer_focus_ring_to_focused_child_organism"
          elevation:
            chrome_elevation_rule: "use_navigation_tab_and_modal_organism_elevation"
            scroll_edge_rule: "raise_visible_chrome_when_content_scrolls_under_it"
          material:
            material_source: "organism.system_chrome_sections.safe_area.primary"
            vibrancy_rule: "allow_system_vibrancy_only_for_platform_chrome_material"
          iconography:
            icon_source_rule: "icons_are_supplied_by_navigation_tab_and_toolbar_organisms"
            icon_alignment: "align_to_platform_tab_and_navigation_baselines"
          imagery:
            image_policy: "selected_content_templates_control_imagery_through_child_organisms"
            fallback_image_policy: "use_media_gallery_template_fallbacks_for_delayed_images"
          copy:
            title_copy_rule: "titles_use_navigation_organism_copy_rules"
            localization_expansion: "allow_root_titles_to_wrap_only_at_accessibility_sizes"
          motion:
            transition_source: "organism.navigation_scaffolds.stack.primary"
            navigation_motion_rule: "preserve_platform_push_tab_and_sheet_transitions"
          haptics:
            feedback_source: "organism.feedback_sections.confirmation.inline"
            feedback_rule: "use_haptics_only_for_explicit_navigation_tab_or_primary_actions"
          sound:
            activation_sound_rule: "respect_child_organism_sound_tokens_and_system_silent_mode"
            template_sound_token: "organism.feedback_sections.confirmation.inline"
          z_index:
            layer_rule: "modal_feedback_and_permission_regions_above_root_navigation_and_content"
            overlay_policy: "global_toast_and_permission_layers_remain_above_selected_tab_content"
          content_rules:
            minimum_visible_regions: 3
            maximum_primary_regions: 5
            localization_expansion: "allow_30_percent_tab_label_growth_before_compaction"
          constraints:
            - "must_preserve_44pt_minimum_tap_target_for_all_interactive_child_organisms"
        dynamic:
          color_scheme:
            light: "use_light_values_from_organism_color_scheme_dependencies"
            dark: "use_dark_values_from_organism_color_scheme_dependencies"
            high_contrast_light: "use_high_contrast_light_organism_variants"
            high_contrast_dark: "use_high_contrast_dark_organism_variants"
          accessibility:
            dynamic_type: "collapse_secondary_global_actions_into_overflow_at_accessibility_sizes"
            increase_contrast: "strengthen_separator_and_focus_organism_dependencies"
            reduce_transparency: "replace_chrome_material_with_opaque_system_chrome_organisms"
            voiceover: "announce_current_template_region_selected_tab_and_available_actions"
            switch_control: "preserve_linear_focus_order_from_chrome_to_navigation_to_content"
            large_content_viewer: "expose_large_previews_for_tab_and_toolbar_icons"
          interaction_state:
            enabled: "all_required_child_organisms_accept_interaction"
            loading: "show_global_loading_state_region_without_displacing_navigation_chrome"
            refreshing: "attach_refresh_feedback_to_selected_content_region"
            error: "show_error_feedback_region_and_keep_root_navigation_available"
          device_context:
            iphone_compact: "single_column_navigation_with_bottom_tab_bar"
            iphone_regular: "single_column_navigation_with_expanded_toolbar_capacity"
            ipad_regular: "prefer_split_view_or_sidebar_when_organism_inputs_support_it"
          locale_context:
            left_to_right: "leading_navigation_appears_on_left"
            right_to_left: "mirror_navigation_and_tab_slots_while_preserving_symbol_semantics"
          motion_context:
            standard_motion: "use_platform_push_tab_and_sheet_transitions"
            reduce_motion: "replace_depth_and_tab_transition_motion_with_crossfade"
          data_context:
            empty: "show_empty_state_template_in_selected_content_region"
            populated: "render_selected_content_regions_in_defined_order"
            error: "show_feedback_template_above_recoverable_content"
            success: "allow_confirmation_feedback_without_navigation_reset"
          system_material_context:
            standard: "use_declared_system_chrome_and_navigation_material_organisms"
            reduce_transparency: "use_opaque_system_chrome_organism"
          content_variation_context:
            sparse: "use_primary_navigation_plus_empty_state_or_detail_template"
            dense: "enable_list_detail_or_dashboard_template_with_grouped_regions"
            action_heavy: "group_secondary_actions_into_system_chrome_or_modal_sheet_template"
          navigation_context:
            root: "show_root_tab_or_navigation_chrome"
            pushed: "show_back_control_and_destination_template_title"
            modal: "show_close_control_and_modal_sheet_template_title"
          input_modality_context:
            touch: "use_standard_touch_targets"
            pointer: "enable_hover_affordances_for_chrome_toolbar_and_disclosure_organisms"
            keyboard: "expose_template_focus_order_and_command_shortcuts"
          privacy_permission_context:
            unrestricted: "render_all_available_template_regions"
            permission_limited: "hide_disable_or_replace_regions_without_entitlement"
        organism_dependencies:
          required:
            - "organism.navigation_scaffolds.stack.primary"
            - "organism.system_chrome_sections.safe_area.primary"
          conditional:
            - condition: "tabbed_shell_variant"
              organism_refs:
                - "organism.tabbed_surfaces.tab_bar.primary"
          fallback:
            - "organism.feedback_sections.inline_error.default"
        composition:
          organism_mapping:
            root_navigation: "organism.navigation_scaffolds.stack.primary"
            root_chrome: "organism.system_chrome_sections.safe_area.primary"
            global_feedback: "organism.feedback_sections.inline_error.default"
          layout_formula: "height=safe_area_top+navigation_chrome_height+selected_content_height+safe_area_bottom"
          state_binding: "bind_loading_empty_error_success_permission_and_refreshing_to_state_regions"
          variant_strategy: "derive_compact_regular_ipad_modal_and_tabbed_variants_from_shared_anatomy"
          reuse_boundary: "reusable_root_template_not_complete_application_or_product_journey"
          containment_rule: "template_contains_organisms_and_state_regions_but_does_not_own_business_data_models"
          template_boundary: "template_may_span_one_screen_or_short_modal_flow_but_not_multi_feature_workflows"
        behavior:
          entry_actions:
            - "resolve_root_navigation_tab_selection_and_primary_content_template"
          exit_actions:
            - "persist_selected_tab_and_scroll_position_when_host_application_requests_restoration"
          transitions:
            - from_state: "root"
              to_state: "pushed"
              trigger: "destination_activation"
              animation: "platform_push_or_reduce_motion_crossfade"
          data_requirements:
            - "root_title_text"
            - "selected_content_items"
          error_recovery:
            - "keep_root_navigation_or_close_action_available_during_content_error"
          persistence_policy: "restore_navigation_path_selected_tab_and_scroll_state_only_when_host_application_supplies_stable_route_ids"
        provenance:
          organism_source: "ios_design_system_organisms.static_organisms"
          molecule_trace:
            - "organism_dependencies_preserve_molecule_refs_from_source_organism_yaml"
          atom_trace:
            - "molecule_dependencies_preserve_atom_refs_from_source_molecule_yaml"
          visual_evidence:
            - "root_surface_navigation_density_and_content_priority_derived_from_ref_001"
          confidence: "medium"
          decision_rule: "compose_from_high_confidence_navigation_system_chrome_tab_feedback_and_content_organisms"
        implementation:
          swiftui: "NavigationStack(path:) { TabView(selection:) { selectedContent }.toolbar { toolbarItems } }.sheet(item:) { modalContent }"
          uikit: "UITabBarController with UINavigationController children, child content controllers, and modal presentation coordinator"
          token_name: "primaryTabbedAppShell"
          file_targets:
            - "DesignSystemTemplates.swift"
            - "DSPrimaryTabbedAppShell.swift"
          handoff_notes:
            - "implement_as_root_container_when_navigation_and_chrome_behavior_is_shared_across_features"
        qa:
          assertions:
            - "all_interactive_child_organisms_preserve_44pt_minimum_tap_targets"
            - "root_chrome_does_not_overlap_content_at_any_safe_area"
          snapshot_states:
            - "light_root_populated"
            - "dark_modal_presented"
            - "accessibility_xxl_loading"
          interaction_tests:
            - "tab_switch_preserves_each_tab_navigation_stack_when_enabled"
            - "modal_close_remains_reachable_with_keyboard_focus"
          failure_mode: "fallback_to_platform_navigation_stack_with_valid_organism_dependencies"
```

Use the same template object shape for every category. Category-specific values should change, but required nested keys must stay present.

## Required Static Category Intent

- `app_shell_templates`: root app surfaces, primary navigation containers, global safe-area coordination, and reusable application shell structures.
- `navigation_stack_templates`: push navigation flows, destination templates, route title structures, toolbar capacity rules, and back or close affordance patterns.
- `tab_root_templates`: tabbed root surfaces, segmented root surfaces, tab overflow handling, tab-specific badges, and selected content regions.
- `split_view_templates`: sidebar/detail structures, two-column and three-column layouts, collapsed compact behavior, and iPad adaptive navigation.
- `list_detail_templates`: grouped list plus detail surfaces, selectable lists, drill-in layouts, swipe action patterns, and reorderable list-detail structures.
- `form_flow_templates`: editable field flows, validation templates, picker-heavy forms, submit/cancel regions, and multi-step form blocks.
- `search_results_templates`: search landing states, scoped search, suggestions, filter regions, zero-result structures, and results grouping.
- `feed_templates`: card feeds, timelines, activity streams, paginated surfaces, refreshable lists, and mixed media feeds.
- `detail_templates`: object detail pages, metadata groups, related content, primary action groups, and expandable detail structures.
- `media_gallery_templates`: galleries, preview grids, carousel detail surfaces, attachment pickers, playback surfaces, and upload review structures.
- `profile_templates`: account/profile pages, identity summaries, member profiles, presence surfaces, and profile action structures.
- `dashboard_templates`: KPI dashboards, chart summaries, operational status surfaces, metric grids, and trend panels.
- `commerce_templates`: product detail, pricing, cart, checkout, entitlement, purchase confirmation, and subscription management surfaces.
- `messaging_templates`: conversation lists, message threads, composer surfaces, attachment flows, typing states, and empty conversation surfaces.
- `onboarding_templates`: intro flows, step panels, choice flows, permission education, progress structures, and completion surfaces.
- `authentication_templates`: sign-in, sign-up, verification, biometric, recovery, session-expired, and account-switching structures.
- `settings_templates`: preferences, account settings, integrations, destructive actions, legal/support, and nested preference detail structures.
- `editor_templates`: creation canvases, inspector layouts, formatting surfaces, asset pickers, preview panels, and publish/review structures.
- `content_collection_templates`: browsable collections, shelves, grids, sorting/filtering, selection mode, and batch action structures.
- `empty_state_templates`: first-run, no-content, no-results, no-permission, offline, and blocked-state reusable surfaces.
- `feedback_templates`: inline success, warning, error, progress, toast stack, confirmation, remediation, and blocking feedback surfaces.
- `modal_sheet_templates`: detented sheets, action sheets, destructive confirmations, modal forms, modal detail, and picker sheets.
- `permission_templates`: notification, location, camera, photo-library, contacts, calendar, tracking, limited-access, and denied-permission structures.
- `system_status_templates`: global status bars, network/offline banners, sync status, background task progress, maintenance, and entitlement status surfaces.

## Dynamic Template Categories

`dynamic_templates` must contain every required dynamic category. Each dynamic category must use this shape:

```yaml
dynamic_templates:
  color_scheme_adaptations:
    rule_id: "dynamic_template.color_scheme"
    affected_template_categories:
      - "app_shell_templates"
    affected_organism_categories:
      - "navigation_scaffolds"
      - "system_chrome_sections"
    default_behavior: "resolve_template_colors_through_organism_color_scheme_variants"
    variants:
      - variant_id: "light"
        condition: "system_color_scheme_is_light"
        template_adjustments:
          - "use_light_organism_values_for_all_color_dependencies"
        organism_adjustments:
          - "read_organism.dynamic.color_scheme.light"
        qa_assertions:
          - "template_regions_keep_visible_hierarchy"
      - variant_id: "dark"
        condition: "system_color_scheme_is_dark"
        template_adjustments:
          - "use_dark_organism_values_for_all_color_dependencies"
        organism_adjustments:
          - "read_organism.dynamic.color_scheme.dark"
        qa_assertions:
          - "text_contrast_remains_at_least_wcag_aa_for_template_content"
    implementation_notes:
      - "prefer_runtime_color_resolution_from_organism_tokens"
```

## State And Accessibility Templates

`state_templates` must include reusable templates for at least:

- `enabled`
- `loading`
- `empty`
- `error`
- `success`
- `editing`
- `refreshing`
- `paginating`
- `filtering`
- `selecting`
- `expanded`
- `collapsed`
- `offline`
- `permission_denied`
- `unauthenticated`

`accessibility_templates` must include reusable templates for at least:

- `dynamic_type`
- `increase_contrast`
- `reduce_motion`
- `reduce_transparency`
- `voiceover`
- `switch_control`
- `large_content_viewer`
- `bold_text`
- `keyboard_navigation`
- `differentiate_without_color`
- `voice_control`
- `display_zoom`
- `assistive_access`

Use the standard template object shape for each state and accessibility template. State template objects must use `category: "state"` and IDs beginning with `template.state.`. Accessibility template objects must use `category: "accessibility"` and IDs beginning with `template.accessibility.`.

## Composition Rules

Required shape:

```yaml
composition_rules:
  organism_reference_policy: "reference_organism_ids_instead_of_copying_organism_values"
  template_boundary_policy: "templates_stop_before_complete_apps_long_product_journeys_or_business_workflows"
  variant_generation_policy: "derive_variants_from_shared_anatomy_and_explicit_dynamic_rules"
  accessibility_policy: "state_and_accessibility_templates_must_be_composable_with_all_static_template_categories"
  layout_policy: "all_templates_preserve_safe_areas_intrinsic_child_organism_sizing_and_44pt_minimum_interactive_targets"
  state_policy: "templates_coordinate_child_organism_states_without_overwriting_organism_contracts"
```

## Implementation

Required shape:

```yaml
implementation:
  token_naming:
    swiftui_type_prefix: "DS"
    swift_identifier_style: "lower_camel_case"
    yaml_identifier_style: "lower_snake_case"
  export_targets:
    - target: "swiftui"
      format: "swift_source"
      naming_rule: "DesignSystemTemplates.<category>.<template>"
    - target: "uikit"
      format: "swift_source"
      naming_rule: "DSTemplates.<category>.<template>"
  file_plan:
    - path: "DesignSystemTemplates.swift"
      purpose: "shared_template_surfaces_and_short_flow_compositions"
  dependency_order:
    - "organism_inputs"
    - "composition_rules"
    - "static_templates"
    - "dynamic_templates"
```

## Quality Gates

Required shape:

```yaml
quality_gates:
  validation_checks:
    - "yaml_parses_without_markdown_fences"
    - "top_level_key_order_matches_contract"
    - "no_null_empty_unknown_undefined_missing_or_placeholder_values"
    - "every_required_static_category_has_templates"
    - "every_required_dynamic_category_has_variants"
    - "every_template_has_anatomy_static_dynamic_organism_dependencies_composition_behavior_provenance_implementation_and_qa"
    - "every_template_references_organism_ids_without_redefining_organism_values"
  completeness_claim: "all_required_ios_template_categories_are_populated"
  residual_risks:
    - "weak_organism_evidence_sections_use_low_confidence_deterministic_fallbacks"
```

## Change Log

Required shape:

```yaml
change_log:
  entries:
    - change_id: "change.initial_contract"
      description: "initial_template_inventory_generated_from_reference_set_and_organism_yaml"
      source_fingerprint: "<12_lowercase_hex_chars>"
      deterministic: true
```

## Value Rules

- Never use `null`, `~`, empty strings, empty lists, empty mappings, `undefined`, `unknown`, `missing`, `todo`, `tbd`, `n/a`, or placeholders.
- Do not omit a required key.
- Use lowercase snake_case for YAML keys and template names.
- Use confidence values only from `low`, `medium`, or `high`.
- Quote hex colors and strings containing `: `, `%`, leading zeroes, or punctuation that YAML may misread.
- Lists must contain at least one concrete string or mapping.
- Mappings must contain at least one required concrete key-value pair.
- Weak evidence must become a concrete deterministic fallback with `confidence: low`, not a placeholder.
