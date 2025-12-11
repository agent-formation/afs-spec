# Agent Formation Schema specification (draft)

This document defines the Agent Formation Schema at a high level. The canonical schemas in `/schemas` are the source of truth.

---

## 1. What is a Formation?

A **Formation** is a declarative description of an AI agent system. It specifies:

- Global system settings
- One or more agents
- Tool servers via MCP
- Agent-to-agent services via A2A
- Memory, knowledge, and secrets
- Optional runtime-specific extensions

A Formation is **portable by default** and should not assume a specific runtime.

Formation files use the `.afs` (Agent Formation Schema) or `.yaml` extension.

---

## 2. Core components

### 2.1 Formation root
Contains:
- `schema` (semantic version)
- `id`, `description`
- global defaults
- memory and knowledge configs
- auth / security if required
- component references

### 2.2 Agents
Agents are declared under `agents/` and referenced by the Formation.

Each agent includes:
- identity and role
- goals / responsibilities
- tool access
- memory bindings
- overrides

### 2.3 MCP tool servers
MCP servers provide tools to agents.

They may be:
- local command-based
- remote HTTP-based
- hosted elsewhere

### 2.4 A2A services
A2A services define agent-to-agent and external service communication.

They can represent:
- internal multi-agent pipelines
- external APIs
- background capabilities

---

## 3. Presence implies enablement

If a block is present in a Formation, it is considered enabled unless explicitly disabled.
This avoids redundant flags and keeps configs readable.

---

## 4. Overrides and precedence

Default precedence order:
1. Formation defaults
2. Component defaults (agents / services)
3. Agent-specific overrides

This enables concise top-level definitions with targeted specialization.

---

## 5. Secrets and environment variables

- Secrets are referenced as: `${{ secrets.NAME }}`
- Environment variables as: `${ENV_VAR}`

Concrete storage and resolution is runtime-defined, but the syntax is standard.

---

## 6. Extensions

Agent Formation includes a standard `extensions` surface:

```yaml
extensions:
  vendor.example.io/runtime:
    key: value
```

Rules:
- Core standard **must not** depend on extensions.
- Extension keys must be namespaced by domain.
- Runtimes should ignore unknown extensions safely.

---

## 7. Backward compatibility

- Patch/minor releases are backward compatible.
- Major releases may break compatibility and must include migration notes.

See `versioning.md`.
