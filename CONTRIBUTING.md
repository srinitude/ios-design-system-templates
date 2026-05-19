# Contributing

Thanks for helping improve iOS Design System Templates.

## Development Setup

Clone the repository, then validate the skill package from the repository root:

```bash
skills-ref validate "$PWD"
python3 -m py_compile scripts/validate-ios-templates-yaml.py
uv run --with-requirements requirements.txt python scripts/validate-ios-templates-yaml.py --help
npx skills add "$PWD" --list
```

If `skills-ref` is not installed, run the official reference implementation:

```bash
git clone --depth 1 https://github.com/agentskills/agentskills /tmp/agentskills
uv run --project /tmp/agentskills/skills-ref skills-ref validate "$PWD"
```

## Contribution Guidelines

- Keep the repository installable with `npx skills add srinitude/ios-design-system-templates`.
- Keep `SKILL.md` focused on the core workflow and non-obvious gotchas.
- Put long schemas, compliance notes, and field-level detail in `references/`.
- Put deterministic repeated logic in `scripts/`.
- Preserve parser-valid YAML behavior and the validator contract for template outputs.
- Avoid committing private screenshots, credentials, API keys, generated caches, or proprietary reference material.

## Pull Requests

Before opening a pull request:

1. Run the validation commands above.
2. Update README or reference docs when behavior changes.
3. Keep commits focused and use clear commit messages.
4. Explain what changed, why it changed, and how it was validated.
