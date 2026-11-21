# Standalone skills

These `.skill` files are individual Claude skill packages for Claude.ai. Install `jrs-route.skill`
first, then add only the department and support packages you need. This is the modular alternative to
the complete plugin.

Do not install these packages in the same environment as the `jrs` Claude Code plugin. Their triggers overlap.

Each package contains its current workflow, deferred references and editable house standards when
applicable. Standalone skills do not include the plugin's shared agents, so they run stages in the
session and accurately report agent fallbacks.

The packages are generated from the same 1.3.0 source used by the plugin. Run
`python3 scripts/build_standalone.py` after changing a skill, then run the release checks.
