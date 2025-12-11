<p align="center">
<img src="https://avatars.githubusercontent.com/u/249095986?v=1" width="112" height="112">
</p>

# Agent Formation

> **Open standard for declarative AI agents** — a portable, interoperable schema for defining agents, tools (MCP), and agent-to-agent services (A2A) across runtimes.

---

## Overview

**Agent Formation** defines a **vendor-neutral, declarative configuration standard** for AI agents and multi-agent systems. The goal is simple:

- **Write agent systems once**
- **Run them anywhere**
- **Validate them consistently**

The standard provides a clear separation between:

- **Definition (standard)** — how formations, agents, tools, and services are declared
- **Implementation (runtimes)** — how those declarations are executed by a specific platform

[MUXI](https://muxi.org) uses Agent Formation as a reference implementation, but **any runtime or framework can adopt this standard**.

---

## Why a declarative agent standard?

Agent configurations today are fragmented across frameworks and often tightly coupled to a specific runtime. Agent Formation standardizes the missing layer:

- **Portable agent definitions**
- **Composable multi-agent setups**
- **Consistent validation and backward compatibility**
- **Explicit extension points for vendors**

Think of Agent Formation as *infrastructure-as-code for agents*.

---

## File extensions

Agent Formation supports two file extensions:

- **`.afs`** — Agent Formation Schema (recommended)
- **`.yaml`** — Standard YAML extension

Both are fully supported and functionally identical. Use `.afs` for clarity in projects with multiple YAML files.

---

## Repository structure

```
.
├── schemas/                  # Canonical Formation schemas and templates
│   ├── SCHEMA_GUIDE.md       # Authoritative field reference
│   ├── formation.afs         # Core Formation template
│   ├── agents/               # Agent templates
│   │   ├── minimal.afs
│   │   └── full.afs
│   ├── mcp/                  # MCP tool server templates
│   │   ├── local_tools.afs
│   │   └── web_tools.afs
│   ├── a2a/                  # Agent-to-agent service templates
│   ├── knowledge/            # Knowledge base files directory
│   ├── secrets.enc           # Encrypted secrets storage (example)
│   └── secrets.example       # Example secrets template
├── specs/                    # Specification documents
│   ├── formation.md          # Core standard
│   ├── versioning.md         # Versioning policy
│   └── secrets.md            # Secrets specification
├── CHARTER.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── MAINTAINERS.md
├── ROADMAP.md
└── SECURITY.md
```

---

## Schema families

### Formation schemas (`/schemas`)

Formation files describe **complete agent systems** with modular components:

- **Formation configuration** (`formation.afs` or `formation.yaml`)  
  Core system settings, LLM models, memory, MCP, A2A, auth, defaults.

- **Agent definitions** (`agents/*.afs`)  
  Individual agents with roles, goals, tools, memory, and overrides.

- **MCP tool servers** (`mcp/*.afs`)  
  Model Context Protocol servers providing tools/functions.

- **A2A services** (`a2a/*.afs`)  
  Agent-to-agent services and external service adapters.

- **Knowledge and secrets** (`knowledge/`, `secrets`, `secrets.enc`, `.key`)  
  Portable knowledge assets and encrypted config.

---

## Spec and documentation

### Start here

**`schemas/SCHEMA_GUIDE.md`** is the authoritative field reference:

- Field-by-field reference
- Override rules and precedence
- Validation rules and examples
- Best practices

### Specifications

| Document | Description |
|----------|-------------|
| `specs/formation.md` | High-level Formation standard overview |
| `specs/versioning.md` | Semantic versioning policy |
| `specs/secrets.md` | Secrets encryption and interpolation |

### Quick reference

| Schema type | Templates | Spec section |
|-------------|-----------|--------------|
| Formation | `schemas/formation.afs` | [SCHEMA_GUIDE.md](schemas/SCHEMA_GUIDE.md) |
| Agent | `schemas/agents/*.afs` | [SCHEMA_GUIDE.md](schemas/SCHEMA_GUIDE.md) |
| MCP server | `schemas/mcp/*.afs` | [SCHEMA_GUIDE.md](schemas/SCHEMA_GUIDE.md) |
| A2A service | `schemas/a2a/*.afs` | [SCHEMA_GUIDE.md](schemas/SCHEMA_GUIDE.md) |

---

## Using the standard

### 1. Start a new Formation

```bash
cp -r schemas my-formation
cd my-formation

nano formation.afs

# secrets are optional, but recommended for production
# (commands below use MUXI CLI as reference implementation)
muxi secrets init
muxi secrets set OPENAI_API_KEY "your-key"

muxi deploy
```

### 2. Validate a Formation

```bash
muxi validate formation.afs [--schema formation]
muxi validate agents/my-agent.afs --schema agent
muxi validate mcp/my-tools.afs --schema mcp
```

### 3. Add components

```bash
cp schemas/agents/minimal.afs agents/my-agent.afs
cp schemas/mcp/web_tools.afs mcp/my-tools.afs
cp schemas/a2a/analytics_engine.afs a2a/my-service.afs
```

---

## Design principles

1. **Declarative first** — configuration describes intent, not execution.
2. **Portability** — configs are runtime-agnostic by default.
3. **Presence implies enablement** — sections activate features automatically.
4. **Sensible defaults** — reduce boilerplate for common setups.
5. **Backward compatibility** — no breaking changes within a major version.
6. **Explicit extensibility** — vendors add fields via namespaced extensions.

---

## Versioning and compatibility

All files include semantic schema versions:

```yaml
schema: "1.0.0"
```

- **Patch**: bugfixes or clarifications
- **Minor**: backward-compatible additions
- **Major**: breaking changes with migration tooling

See `specs/versioning.md`.

---

## Contributing

This repo defines the **Agent Formation Standard**. Contributions should include:

1. Schema updates
2. Guide updates
3. Template updates
4. Fixtures and validation coverage
5. Compatibility checks

See `CONTRIBUTING.md`.

---

## Origin

Agent Formation was originally developed as part of the [MUXI Stack](https://github.com/muxi-ai/muxi) and contributed to establish a vendor-neutral standard for declarative AI agent systems. MUXI continues to serve as the reference implementation.

---

## License

Apache License 2.0. See `LICENSE`.

---

## Implementations

- [**MUXI Runtime**](https://github.com/muxi-ai/muxi) — reference implementation of Agent Formation.

Other implementations are welcome.
