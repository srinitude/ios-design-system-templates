# Agent Skills Compliance Reference

Source refresh date: 2026-05-19.

Use this reference only when editing, reviewing, packaging, or validating this skill. Do not load it during ordinary template-generation runs.

## Source Inventory

- Agent Skills URL map: https://agentskills.io/
- Canonical documentation index: https://agentskills.io/llms.txt
- Format specification: https://agentskills.io/specification
- Creator best practices: https://agentskills.io/skill-creation/best-practices
- Description optimization: https://agentskills.io/skill-creation/optimizing-descriptions
- Output evaluation: https://agentskills.io/skill-creation/evaluating-skills
- Script guidance: https://agentskills.io/skill-creation/using-scripts
- Reference implementation: https://github.com/agentskills/agentskills

## Compliance Rules For This Package

- The skill directory must contain `SKILL.md` exactly, with YAML frontmatter followed by Markdown.
- The frontmatter `name` must be `ios-design-system-templates` and must match the parent directory.
- The frontmatter `description` must stay under 1024 characters and must include both when to use the skill and what it produces.
- Use `compatibility` only for real runtime requirements. This skill uses it because deterministic validation depends on Python 3.9+ and PyYAML through `uv`, `requirements.txt`, or an installed environment.
- Keep support-file paths relative to the skill root: `references/templates-yaml-contract.md` and `scripts/validate-ios-templates-yaml.py`.
- Keep `SKILL.md` under 500 lines and roughly under 5000 tokens. Move schema detail and compliance research into `references/`.
- Additional files are allowed when they directly support the skill. The `agents/openai.yaml` file is client metadata and must stay aligned with the skill's frontmatter.

## Portable Best Practices Adopted

- Use progressive disclosure: frontmatter for triggering, `SKILL.md` for the runbook, `references/` for the long YAML contract, and `scripts/` for deterministic validation.
- Start from real use cases: reference-image analysis, organism-driven template extrapolation, valid YAML output, and implementation-ready iOS design-system contracts.
- Be prescriptive where the task is fragile. YAML validity, key order, duplicate-key rejection, required sections, banned placeholders, and confidence labels are enforced by script.
- Prefer defaults over menus. The default path is organism generation, template extrapolation, validator run, repair, and final raw YAML.
- Use procedures instead of generic quality claims. The skill states the exact sequence, files, commands, and validation gate.
- Keep the skill composable and platform-aware. The main instructions do not assume one host client except where local validation tools are explicitly required.
- Validate with concrete evidence before claiming success. Package validation should include frontmatter checks, script compile checks, CLI discovery checks, and positive YAML fixture checks.

## Determinism Checklist

- Every comprehensive template artifact preserves the contract's top-level order and nested key order.
- Every required static template category is present and populated.
- Every required dynamic template category has concrete variants.
- Every state and accessibility template uses the standard template object shape.
- Every template references organism IDs without copying organism, molecule, or atom values inline.
- Values that are not directly visible use deterministic fallbacks with `confidence: low` and a concrete `provenance.decision_rule`.
- The validator rejects markdown fences, tabs, duplicate keys, missing sections, wrong top-level order, empty values, banned placeholders, malformed confidence labels, and incomplete template objects.
