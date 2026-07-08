# Agent Formation schemas

This directory contains the canonical Agent Formation schema templates and the authoritative specification guide.

## Contents

| Path | Description |
|------|-------------|
| `SCHEMA_GUIDE.md` | **Authoritative schema reference** — field definitions, override rules, validation, examples |
| `formation.afs` | Core formation configuration template |
| `agents/` | Agent definition templates (`minimal.afs`, `full.afs`) |
| `skills/` | Agent skills directory (SKILL.md files with scripts, references, assets) |
| `mcp/` | MCP tool server templates (`local_tools.afs`, `web_tools.afs`) |
| `a2a/` | Agent-to-agent service templates |
| `sops/` | SOP templates (markdown + frontmatter; auto-discovered) |
| `triggers/` | Trigger templates (markdown + frontmatter; auto-discovered) |
| `transformers/` | Outbound payload transformer templates (auto-discovered) |
| `groups/` | Access-control group templates (auto-discovered; requires `server.auth: required`) |
| `knowledge/` | Knowledge base files directory |

## File extensions

Agent Formation supports two file extensions:

- **`.afs`** — Agent Formation Schema (recommended)
- **`.yaml`** — Standard YAML extension

Both are fully supported and functionally identical.

## Quick start

```bash
# Copy this directory as a starting point
cp -r schemas my-formation
cd my-formation

# Edit the core configuration
nano formation.afs

# Add agents, MCP servers, A2A services as needed
```

## Documentation

For complete field reference, override hierarchies, secrets syntax, and validation rules, see **[SCHEMA_GUIDE.md](SCHEMA_GUIDE.md)**.
