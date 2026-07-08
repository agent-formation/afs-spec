# SOPs (standard operating procedures)

SOPs are reusable, named procedures defined as markdown files with YAML frontmatter.

- **Auto-discovered** — `sops/` is scanned recursively; every `*.md` file whose frontmatter declares `type: sop` is loaded (content/policy tier, see `specs/formation.md` §3). Other files in `sops/` are loadable resources for `[file:path]` references.
- **Id from filename** — `sops/weekly-report.md` becomes SOP `weekly-report`.
- **Activation** — SOPs execute via semantic matching against user requests, via slash commands (a formation SOP shadows a built-in command of the same name), or by explicit reference (e.g. `proactive.heartbeat.sop`).

## Frontmatter

| Key | Required | Default | Meaning |
|-----|----------|---------|---------|
| `type` | yes | — | Literal `sop` |
| `name` | no | file stem | Display name |
| `description` | no | — | One-line description (shown by `/help`) |
| `mode` | no | `template` | `template` (deterministic step parsing) or `guide` (LLM-interpreted) |
| `tags` | no | — | Comma-separated string or list, for semantic matching |
| `model` | no | — | Default model for all steps: alias or `provider/model` |
| `bypass_approval` | no | `true` | Skip workflow plan approval |
| `synthesis` | no | `true` | Run a synthesis pass after execution |

## Step directives

In `template` mode the body's numbered steps (under `## Steps`) may carry inline directives:

| Directive | Meaning |
|-----------|---------|
| `[agent:name]` | Route the step to the named agent |
| `[skill:name]` / `[skill:name/script]` | Activate a skill (optionally a specific script) |
| `[mcp:server]` / `[mcp:server/action]` | Declare an MCP capability requirement |
| `[model:x]` | Step-level model override (wins over frontmatter `model:`) |
| `[parallel]` | Remove the sequential dependency on the previous step |
| `[file:path]` | Reference a resource file |

See `weekly-report.md` in this directory for a complete annotated example, and `specs/formation.md` §2.6 for the normative text.
