# Standalone skills

These `.skill` files are individual Claude skill packages for Claude.ai. Install `jrs-route.skill` first, then add only the department packages you need.

Do not install these packages in the same environment as the `jrs` Claude Code plugin. Their triggers overlap.

The standalone packages contain self-contained workflows. They do not include the plugin's shared agents or editable `house-standards.md` files.

**Version note.** These packages were built from plugin version 1.0.3. They do not yet contain the
1.1.x changes (risk trigger at every size, drafts-not-approvals rule, handoff block, deterministic
routing and review-contract fixes) or the 1.2.0 adaptive usage modes. Use the plugin for those until
the packages are rebuilt.
