# Contributing

## Before editing

- Keep the plugin name `jrs`; published Claude Code plugin names are permanent install identifiers.
- Put plugin components at the repository root. Only the manifest and marketplace catalog belong in `.claude-plugin/`.
- Keep skill names in kebab case and place each skill at `skills/<name>/SKILL.md`.
- `templates/department-runtime.md` and `templates/principal-escalation.md` generate the shared
  department sections. Edit the template, then run `python3 scripts/sync_department_contract.py --write`.
- `packages/standalone/*.skill` are generated distribution copies. Update the canonical skill first,
  then run `python3 scripts/build_standalone.py`.

## Validate a change

Run the official validator from the repository root:

```sh
claude plugin validate --strict .
python3 scripts/check_release.py
python3 scripts/check_usage_modes.py
python3 scripts/sync_department_contract.py
python3 scripts/check_prompt_budgets.py
python3 scripts/evaluate_results.py
python3 scripts/build_standalone.py
```

Then load the checkout and exercise the changed skill:

```sh
claude --plugin-dir .
```

For department changes, test both direct invocation (`/jrs:<department>`) and routing through
`/jrs:route`. Changes to execution, agents or models also run the cases in
`tests/usage-mode-prompts.md`.
For a release candidate, also capture the runtime cases in `tests/evals/cases.json` and validate the
result JSON with `python3 scripts/evaluate_results.py <results.json>`.

## Release a change

1. Update the version in `.claude-plugin/plugin.json`.
2. Update `CHANGELOG.md`.
3. Validate and test the plugin.
4. Commit and push the release.

Users can then update with:

```sh
claude plugin update jrs@jrs-labs919-plugins
```
