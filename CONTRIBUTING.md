# Contributing

## Before editing

- Keep the plugin name `jrs`; published Claude Code plugin names are permanent install identifiers.
- Put plugin components at the repository root. Only the manifest and marketplace catalog belong in `.claude-plugin/`.
- Keep skill names in kebab case and place each skill at `skills/<name>/SKILL.md`.
- Treat `packages/standalone/*.skill` as generated distribution artifacts. Update their source workflow first, then rebuild the package.

## Validate a change

Run the official validator from the repository root:

```sh
claude plugin validate --strict .
```

Then load the checkout and exercise the changed skill:

```sh
claude --plugin-dir .
```

For department changes, test both direct invocation (`/jrs:<department>`) and routing through `/jrs:route`.

## Release a change

1. Update the version in `.claude-plugin/plugin.json`.
2. Update `CHANGELOG.md`.
3. Validate and test the plugin.
4. Commit and push the release.

Users can then update with:

```sh
claude plugin update jrs@jrs-labs919-plugins
```
