# Formation schemas

This directory contains the canonical Formation schema templates and the authoritative specification guide.

## Contents

| Path | Description |
|------|-------------|
| `SCHEMA_GUIDE.md` | **Authoritative schema reference** - field definitions, override rules, validation, examples |
| `formation.yaml` | Core formation configuration template |
| `agents/` | Agent definition templates (`minimal.yaml`, `full.yaml`) |
| `mcp/` | MCP tool server templates (`local_tools.yaml`, `web_tools.yaml`) |
| `a2a/` | Agent-to-agent service templates |
| `knowledge/` | Knowledge base files directory |
| `secrets.enc` | Encrypted secrets storage |
| `secrets.example` | Example secrets template |

## Quick start

```bash
# Copy this directory as a starting point
cp -r schemas my-formation
cd my-formation

# Edit the core configuration
nano formation.yaml

# Add agents, MCP servers, A2A services as needed
```

## Documentation

For complete field reference, override hierarchies, secrets syntax, and validation rules, see **[SCHEMA_GUIDE.md](SCHEMA_GUIDE.md)**.
