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

Each server supports an optional `parameters` field: a flat key-value map of default values injected into every tool call. This is intended for infrastructure constants (org-level IDs, tenant keys) that should never be left to LLM inference. Values support `${{ secrets.X }}` interpolation. Caller-provided values always take precedence.

### 2.4 A2A services
A2A services define agent-to-agent and external service communication.

They can represent:
- internal multi-agent pipelines
- external APIs
- background capabilities

### 2.5 Skills
Skills are reusable agent capabilities following the [Agent Skills specification](https://agentskills.io/specification).

Each skill is a directory under `skills/` containing:
- `SKILL.md` (required): YAML frontmatter + instructions
- `scripts/` (optional): executable code
- `references/` (optional): additional documentation
- `assets/` (optional): templates, resources

Skills can be declared at:
- Formation level (public, available to all agents)
- Agent level (private, only that agent)

---

## 3. Explicit component declaration

Components (agents, MCP servers, A2A services) are declared explicitly in the formation file by ID.
Files in subdirectories (`agents/`, `mcp/`, `a2a/`) are pure definitions.
Only components listed in the formation manifest are loaded.

```yaml
agents:
  - support-agent       # Loads agents/support-agent.yaml by ID
  - research-agent      # Loads agents/research-agent.yaml by ID

mcp:
  servers:
    - github-mcp        # Loads mcp/github-mcp.yaml by ID
    - slack-mcp         # Loads mcp/slack-mcp.yaml by ID

skills:
  - pdf-processing      # Loads skills/pdf-processing/ by name
```

String entries reference files by ID. Dict entries are inline definitions.
An empty list or omitted field means nothing is loaded for that component type.

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
- Environment variables as: `${{ env.VAR }}`

Concrete storage and resolution are runtime-defined, but the syntax is standard.

---

## 6. Init hook

A Formation may include an `init` field containing a shell command that the runtime executes **before** any services are initialized. This is intended for one-time environment setup: creating directories, installing packages, seeding data, setting permissions, etc.

```yaml
init: "mkdir -p /tmp/workspace && cp seed.json /tmp/workspace/"
```

Rules:
- The command runs via the system shell (`sh -c`).
- Working directory is the formation directory.
- If the command exits with a non-zero status, the formation **must** fail to load.
- Runtimes **should** impose a reasonable timeout (recommended: 120 seconds).
- The field is optional. If omitted, no init command runs.

---

## 7. Extensions

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

## 8. Backward compatibility

- Patch/minor releases are backward compatible.
- Major releases may break compatibility and must include migration notes.

See `versioning.md`.
