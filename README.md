# Formation schemas

> **Open standard for declarative AI agents** - a portable, interoperable schema for defining agents, tools (MCP), and agent-to-agent services (A2A) across runtimes.

---

## Overview

**Formation schemas** define a **vendor-neutral, declarative configuration standard** for AI agents and multi-agent systems. The goal is simple:

- **Write agent systems once**
- **Run them anywhere**
- **Validate them consistently**

The schemas provide a clear separation between:

- **Definition (standard)** - how formations, agents, tools, and services are declared
- **Implementation (runtimes)** - how those declarations are executed by a specific platform

MUXI uses Formation as a reference implementation, but **any runtime or framework can adopt this standard**.

---

## Why a declarative agent standard?

Agent configurations today are fragmented across frameworks and often tightly coupled to a specific runtime. Formation schemas standardize the missing layer:

- **Portable agent definitions**
- **Composable multi-agent setups**
- **Consistent validation and backward compatibility**
- **Explicit extension points for vendors**

Think of Formation as *infrastructure-as-code for agents*.

---

## Repository structure

```
.
├── formation/                # Canonical Formation schemas and templates
│   ├── SCHEMA_GUIDE.md       # Authoritative field reference
│   ├── formation.yaml        # Core Formation template
│   ├── agents/               # Agent templates
│   │   ├── minimal.yaml
│   │   └── full.yaml
│   ├── mcp/                  # MCP tool server templates
│   │   ├── local_tools.yaml
│   │   └── web_tools.yaml
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

### Formation schemas (`/formation`)

Formation files describe **complete agent systems** with modular components:

- **Formation configuration** (`formation.yaml`)  
  Core system settings, LLM models, memory, MCP, A2A, auth, defaults.

- **Agent definitions** (`agents/*.yaml`)  
  Individual agents with roles, goals, tools, memory, and overrides.

- **MCP tool servers** (`mcp/*.yaml`)  
  Model Context Protocol servers providing tools/functions.

- **A2A services** (`a2a/*.yaml`)  
  Agent-to-agent services and external service adapters.

- **Knowledge and secrets** (`knowledge/`, `secrets.enc`)  
  Portable knowledge assets and encrypted config.

---

## Spec and documentation

### Start here

**`formation/SCHEMA_GUIDE.md`** is the authoritative field reference:

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
| Formation | `formation/formation.yaml` | SCHEMA_GUIDE |
| Agent | `formation/agents/*.yaml` | SCHEMA_GUIDE |
| MCP server | `formation/mcp/*.yaml` | SCHEMA_GUIDE |
| A2A service | `formation/a2a/*.yaml` | SCHEMA_GUIDE |

---

## Using the standard

### 1. Start a new Formation

```bash
cp -r formation my-formation
cd my-formation

nano formation.yaml

# secrets are optional, but recommended for production
# (commands below use MUXI CLI as reference implementation)
muxi secrets init
muxi secrets set OPENAI_API_KEY "your-key"

muxi deploy
```

### 2. Validate a Formation

```bash
muxi validate formation.yaml [--schema formation]
muxi validate agents/my-agent.yaml --schema agent
muxi validate mcp/my-tools.yaml --schema mcp
```

### 3. Add components

```bash
cp formation/agents/minimal.yaml agents/my-agent.yaml
cp formation/mcp/web_tools.yaml mcp/my-tools.yaml
cp formation/a2a/analytics_engine.yaml a2a/my-service.yaml
```

---

## Design principles

1. **Declarative first** - configuration describes intent, not execution.
2. **Portability** - configs are runtime-agnostic by default.
3. **Presence implies enablement** - sections activate features automatically.
4. **Sensible defaults** - reduce boilerplate for common setups.
5. **Backward compatibility** - no breaking changes within a major version.
6. **Explicit extensibility** - vendors add fields via namespaced extensions.

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

This repo defines the **Formation standard**. Contributions should include:

1. Schema updates
2. Guide updates
3. Template updates
4. Fixtures and validation coverage
5. Compatibility checks

See `CONTRIBUTING.md`.

---

## Origin

Formation was originally developed as part of the [MUXI Stack](https://github.com/muxi-ai/muxi) and contributed to the Agentic Spec project to establish a vendor-neutral standard for declarative AI agent systems. MUXI continues to serve as the reference implementation.

---

## License

Apache License 2.0. See `LICENSE`.

---

## Implementations

- [**MUXI Runtime**](https://github.com/muxi-ai/runtime) - reference implementation of Formation schemas.

Other implementations are welcome.
