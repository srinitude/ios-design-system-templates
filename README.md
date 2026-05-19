# iOS Design System Templates

[![skills.sh compatible](https://img.shields.io/badge/skills.sh-compatible-111111?style=flat-square)](https://skills.sh/s/srinitude/ios-design-system-templates)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Validate](https://github.com/srinitude/ios-design-system-templates/actions/workflows/validate.yml/badge.svg)](https://github.com/srinitude/ios-design-system-templates/actions/workflows/validate.yml)

A portable Agent Skills package for generating complete deterministic iOS design-system template inventories from reference images.

The skill invokes `ios-design-system-organisms` with the same references, uses the validated organism YAML as its dependency source, and extrapolates reusable screen, surface, flow, modal, state, and accessibility templates into parser-valid YAML with strict no-null/no-empty/no-unknown validation.

## Install

```bash
npx skills add srinitude/ios-design-system-templates
```

To preview the skills exposed by this repository:

```bash
npx skills add srinitude/ios-design-system-templates --list
```

## Use Cases

- Convert iOS reference images into a deterministic YAML inventory of reusable templates.
- Compose template-level surfaces from validated organism IDs instead of duplicating organism, molecule, or atom values.
- Preserve schema order, static and dynamic template fields, confidence labels, fallback rules, and evidence boundaries across runs.
- Validate generated template YAML before returning it to downstream design-system or engineering tools.

## Package Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── agent-skills-compliance.md
│   └── templates-yaml-contract.md
├── requirements.txt
└── scripts/
    └── validate-ios-templates-yaml.py
```

## Validation

Validate the skill package:

```bash
skills-ref validate "$PWD"
```

If `skills-ref` is not installed, run the official reference implementation:

```bash
git clone --depth 1 https://github.com/agentskills/agentskills /tmp/agentskills
uv run --project /tmp/agentskills/skills-ref skills-ref validate "$PWD"
```

Validate the bundled script:

```bash
python3 -m py_compile scripts/validate-ios-templates-yaml.py
uv run --with-requirements requirements.txt python scripts/validate-ios-templates-yaml.py --help
```

Validate a generated template artifact:

```bash
python3 scripts/validate-ios-templates-yaml.py path/to/templates.yaml
```

When `uv` is available, the same template validator can be run through the local environment:

```bash
uv run --with-requirements requirements.txt python scripts/validate-ios-templates-yaml.py path/to/templates.yaml
```

The same checks run in GitHub Actions for pushes and pull requests.

## Requirements

- Python 3.9 or newer.
- PyYAML for YAML validation, installed from `requirements.txt`, through `uv`, or through an existing Python environment.
- Access to `ios-design-system-organisms` or an equivalent validated iOS organism YAML artifact when generating template inventories.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

Please keep changes focused on the portable skill package: update `SKILL.md` for runbook behavior, `references/` for long-form schema or compliance material, and `scripts/` for deterministic validation logic.

## Security

Report security concerns using the guidance in [SECURITY.md](SECURITY.md). Do not include secrets, private screenshots, credentials, or proprietary reference material in public issues.

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
