# Commit Message Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/) and prefixes each commit title with an emoji to identify its type.

## Commit format

```text
<emoji> <type>(<scope>): <description>
```

Example:

```text
✨ feat(logger): add structured logging
```

### Formatting requirements

- Put the emoji at the beginning of the title to indicate the commit type.
- Use a `type` keyword from the table below.
- Use `scope` to identify the affected area, such as `logger`, `config`, `server`, or `bootstrap`. Omit it if no suitable scope applies.
- Write the `description` in English using the imperative mood, start with a lowercase letter, and omit the final period.
- Keep the title within 72 characters where possible.
- Separate the title and body with a blank line.
- Use the body to explain the reason for the change, its main contents, and its impact.
- Keep body lines within the team's agreed limit, commonly 72 or 100 characters.

## Commit types and emojis

| Type | Emoji | Purpose | Example |
| --- | --- | --- | --- |
| `feat` | ✨ | Add a feature | `✨ feat(config): support yaml configuration` |
| `fix` | 🐛 | Fix a bug or incorrect behavior | `🐛 fix(config): reject invalid timeout values` |
| `refactor` | ♻️ | Restructure code without changing external behavior | `♻️ refactor(bootstrap): simplify initialization` |
| `style` | 🎨 | Adjust formatting, layout, or style without changing logic | `🎨 style(server): format startup options` |
| `chore` | 🔧 | Maintain tools, configuration, or other non-business concerns | `🔧 chore(deps): update logging dependencies` |
| `docs` | 📝 | Add or update documentation | `📝 docs: add commit conventions` |
| `test` | ✅ | Add, modify, or organize tests | `✅ test(config): cover timeout validation` |
| `perf` | ⚡ | Improve performance | `⚡ perf(logging): reduce startup allocations` |
| `build` | 📦 | Change the build system or build dependencies | `📦 build: update go build settings` |
| `ci` | 👷 | Change CI/CD workflows or configuration | `👷 ci: add automated test workflow` |
| `revert` | ⏪ | Revert a previous commit | `⏪ revert: revert logger initialization` |

Conventional Commits uses `fix` for bug fixes; `bug` is not a standard type.

## Detailed commit template

```text
<emoji> <type>(<scope>): <description>

Why:
- Explain why the change is needed.

What:
- Describe the main implementation changes.
- Mention important behavior or configuration changes.

Impact:
- Describe affected modules, APIs, users, or compatibility.

BREAKING CHANGE: Describe the migration required by consumers.
```

Remove sections that do not apply. A small commit can contain only a title. Add a body for changes that affect multiple modules or behaviors.

## Writing examples

### Recommended

```text
✨ feat(logger): add structured logging

- add development and production logger initialization
- load logger environment from application configuration
- flush buffered log entries during shutdown
```

```text
🐛 fix(config): apply the default server address

The server now falls back to :8091 when no address is configured,
while preserving explicitly configured addresses.
```

### Avoid

```text
update code
fix bug
✨ feat (logger) : Add logger.
```

The last example contains extra spaces, an uppercase initial letter, and a final period, which do not follow this project's recommended format.

## Breaking changes

If a commit breaks an existing API, configuration format, or way of running the project, use `BREAKING CHANGE:` in the body to explain the migration:

```text
⚠️ refactor(config)!: rename application config fields

BREAKING CHANGE: rename `server.address` to `server.addr` in application.yaml.
```

You can also add `!` after the type or scope, for example `feat(api)!: change response format`.

## Pre-commit checklist

- [ ] Start the title with the agreed emoji.
- [ ] Use the correct Conventional Commits `type`.
- [ ] Keep `scope` accurate and concise.
- [ ] Use an English imperative description with a lowercase initial letter and no final period.
- [ ] Write the title in English and keep it within 72 characters.
- [ ] Add `BREAKING CHANGE:` when the change breaks compatibility.
- [ ] Explain the necessary reasons, implementation details, and impact in the body.
- [ ] Run the tests or checks relevant to the change.
