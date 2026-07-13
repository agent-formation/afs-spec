# Agent Formation Schema Guide

## 📋 Overview

This guide documents the complete schema structure for Agent Formation, including all configuration files, override hierarchies, and validation requirements.

> [!TIP]
> **Secrets Management**: Throughout all configuration files, you can reference secrets using the `${{ secrets.NAME }}` syntax. Any secrets added to your formation's secrets store can be accessed this way, providing secure handling of API keys, passwords, and other sensitive configuration values.

> [!NOTE]
> **File Extensions**: Agent Formation supports both `.afs` (Agent Formation Schema) and `.yaml` extensions. Both are fully supported and functionally identical. Examples in this guide use `.afs` but `.yaml` works the same way.

> [!NOTE]
> When pushing agents, formations, or MCPs to the registry, your username is automatically prepended to the component id, forming a globally unique identifier like `username/agent-id`.

## 📚 Table of Contents

- [📋 Overview](#-overview)
- [🏗️ Schema Version](#️-schema-version)
- [📁 Formation Schema (`formation.afs`)](#-formation-schema-formationafs)
  - [Basic Formation Information](#basic-formation-information)
  - [Server Configuration](#server-configuration)
  - [Access Control (`rbac` + `middleware` + `groups/`)](#access-control-rbac--middleware--groups)
    - [The Middleware Tool Contract](#the-middleware-tool-contract)
    - [Group Definition Format](#group-definition-format)
    - [Permission Resolution Rules](#permission-resolution-rules)
    - [The Tool Override Cascade](#the-tool-override-cascade)
  - [Input Limits Configuration](#input-limits-configuration)
  - [LLM Model Aliases](#llm-model-aliases)
  - [Overlord Soul Configuration](#overlord-soul-configuration)
  - [Workflow Replanning Configuration (`overlord.workflow.replanning`)](#workflow-replanning-configuration-overlordworkflowreplanning)
  - [Memory Configuration](#memory-configuration)
    - [Working Memory Configuration](#working-memory-configuration)
    - [Buffer Memory Configuration](#buffer-memory-configuration)
    - [Persistent Memory Configuration](#persistent-memory-configuration)
    - [Memory Ingestion Configuration (`memory.ingestion`)](#memory-ingestion-configuration-memoryingestion)
  - [Knowledge Configuration (`knowledge:`)](#knowledge-configuration-knowledge)
  - [Proactive Configuration](#proactive-configuration)
  - [Commands Configuration](#commands-configuration)
  - [Artifacts Configuration](#artifacts-configuration)
  - [Links Configuration (`links:`)](#links-configuration-links)
  - [Coding Delegation Configuration (`coding:`)](#coding-delegation-configuration-coding)
    - [The Adapter Schema](#the-adapter-schema)
  - [Watch Configuration (`mcp.watch`)](#watch-configuration-mcpwatch)
    - [The `watch_job` Tool Contract](#the-watch_job-tool-contract)
    - [Group Watch Quota Override](#group-watch-quota-override)
  - [Skills Configuration](#skills-configuration)
  - [Agent-Specific Skills](#agent-specific-skills)
- [📋 SOP Schema (`sops/*.md`)](#-sop-schema-sopsmd)
  - [Steps](#steps)
- [⚡ Trigger Schema (`triggers/*.md`)](#-trigger-schema-triggersmd)
- [📤 Transformer Schema (`transformers/*.afs`)](#-transformer-schema-transformersafs)
- [🔄 Override Hierarchy](#-override-hierarchy)
  - [LLM Configuration Precedence (Highest to Lowest)](#llm-configuration-precedence-highest-to-lowest)
  - [Model Selection Hierarchy (model references)](#model-selection-hierarchy-model-references)
  - [Overlord LLM stages: `base` and `synthesis`](#overlord-llm-stages-base-and-synthesis)
  - [Resolution lattice](#resolution-lattice)
  - [BREAKING: flat `overlord.llm` shape removed](#breaking-flat-overlordllm-shape-removed)
  - [Example Override Flow](#example-override-flow)
  - [MCP Server Access Rules](#mcp-server-access-rules)
  - [API Key Resolution Order](#api-key-resolution-order)
- [📝 Secrets and User Credentials Interpolation](#-secrets-and-user-credentials-interpolation)
  - [Secrets Syntax](#secrets-syntax)
  - [User Credentials Syntax](#user-credentials-syntax)
  - [Examples](#examples)
- [✅ Validation Requirements](#-validation-requirements)
  - [Formation Validation](#formation-validation)
  - [Agent Validation](#agent-validation)
  - [MCP Validation](#mcp-validation)
  - [MCP Default Parameters](#mcp-default-parameters)
  - [MCP Tool Filtering](#mcp-tool-filtering)
  - [A2A Validation](#a2a-validation)
  - [SOP Validation](#sop-validation)
  - [Trigger Validation](#trigger-validation)
  - [Transformer Validation](#transformer-validation)
  - [Coding Delegation Validation](#coding-delegation-validation)
  - [Watch Validation](#watch-validation)
  - [Links Validation](#links-validation)
  - [Memory Ingestion Validation](#memory-ingestion-validation)
  - [Replanning Validation](#replanning-validation)
  - [Knowledge Source Validation](#knowledge-source-validation)
  - [Group Validation](#group-validation)
- [🎯 Best Practices](#-best-practices)
  - [Schema Compliance](#schema-compliance)
  - [Secret Management](#secret-management)
  - [Component Organization](#component-organization)
  - [Override Strategy](#override-strategy)
- [🔍 Common Validation Errors](#-common-validation-errors)
  - [Missing Required Fields](#missing-required-fields)
  - [Invalid Secret References](#invalid-secret-references)
  - [Capability Mismatches](#capability-mismatches)

> [!NOTE]
> **Field-level reference**: Complete, per-field documentation for every configuration
> block (LLM, overlord, A2A, MCP, agents, scheduler, logging, credentials, component
> declaration, and more) lives as inline annotations in the schema files themselves:
> [`formation.afs`](formation.afs), [`agents/`](agents/), [`mcp/`](mcp/),
> [`a2a/`](a2a/), plus the normative prose in [`specs/formation.md`](../specs/formation.md).
> This guide covers structure, override hierarchy, and validation rules.

## 🏗️ Schema Version

All configuration files **MUST** include:
```yaml
schema: "1.0.0"  # Semantic versioning
```

## 📁 Formation Schema (`formation.afs`)

### Basic Formation Information
*Core metadata and identification for the formation*

```yaml
schema: "1.0.0"
id: "formation-1"
description: "Example formation"

# Optional metadata fields
author: "Author Name <email@domain.com>"
url: "https://example.com"
license: "MIT"
version: "1.0.0"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `schema` | ✅ Yes | string | None | Formation schema version using semantic versioning |
| `id` | ✅ Yes | string | None | Unique identifier for this formation |
| `description` | ✅ Yes | string | None | Human-readable description of the formation's purpose |
| `author` | ❌ No | string | None | Author information with optional email |
| `url` | ❌ No | string | None | URL for formation documentation or repository |
| `license` | ❌ No | string | Unlicense | License type (e.g., MIT, Apache-2.0) |
| `version` | ❌ No | string | None | Formation version using semantic versioning |


### Server Configuration
*HTTP API server configuration for formation access*

```yaml
server:
  # Server binding configuration
  host: "0.0.0.0"   # Default: 0.0.0.0
  port: 3000        # Default: 3000
  access_log: false # Default: false - Enable detailed access logging

  # API Keys (auto-generated if not provided)
  api_keys:
    admin_key: "${{ secrets.FORMATION_ADMIN_API_KEY }}"
    client_key: "${{ secrets.FORMATION_CLIENT_API_KEY }}"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `server.host` | ❌ No | string | "0.0.0.0" | Host/IP to bind the API server to |
| `server.port` | ❌ No | integer | 3000 | Port number for the API server |
| `server.access_log` | ❌ No | boolean | false | Enable detailed HTTP access logging |
| `server.api_keys.admin_key` | ❌ No | string | Auto-generated | API key for formation management operations |
| `server.api_keys.client_key` | ❌ No | string | Auto-generated | API key for user interactions |

> [!NOTE]
> API key header names and user identification headers are implementation-defined. See your runtime documentation for details.

### Access Control (`rbac` + `middleware` + `groups/`)
*Group-based access control: how memberships reach the formation, and which resources each group can use*

The runtime stores **no group memberships**. Groups reach a formation in exactly one way: a formation-declared **request middleware** — a standard MCP server the runtime calls with every request payload after client-key auth and before any processing. The middleware matches `user_id` to groups against whatever the organization uses (its DB, WorkOS, LDAP, a static map); how it does so is outside this standard.

Both blocks are **top-level** — not under `server:`, because the pipeline applies equally to HTTP traffic and to embedded `overlord.chat(...)` use:

```yaml
# formation.afs
rbac:
  active: auto            # auto (default) | true | false
  fallback: false         # false | <group_name>

middleware:
  # An actual MCP server declaration. Exactly one transport:
  url: "${{ secrets.RESOLVER_URL }}"     # http
  headers:
    Authorization: "Bearer ${{ secrets.RESOLVER_TOKEN }}"
  # command: "./middleware.py"           # stdio (alternative)
  # args: ["--map", "groups.json"]
  timeout: 2s                            # the only runtime knob
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `rbac.active` | ❌ No | string/bool | `auto` | `auto`: RBAC is on iff `groups/` contains group files. `true`: explicit intent — no group files fails the load. `false`: kill switch — filtering disabled even if `groups/` exists (logged loudly at load) |
| `rbac.fallback` | ❌ No | `false`/string | `false` | Applies to a request that ends up with **no groups** (no middleware, or the middleware cleanly returned none): `false` rejects it; `<group_name>` proceeds with that group's permissions (`public` is the idiomatic open tier). The named group must exist in `groups/` (validated at load). Never applies to middleware errors |
| `middleware.url` | ❌ Conditional | string | None | HTTP transport endpoint (exactly one transport: `url` or `command`) |
| `middleware.headers` | ❌ No | map | None | HTTP headers (auth etc.); only with `url` |
| `middleware.command` | ❌ Conditional | string | None | Stdio transport command, e.g. `./middleware.py` (exactly one transport) |
| `middleware.args` | ❌ No | list | None | Stdio command arguments; only with `command` |
| `middleware.timeout` | ❌ No | duration | 10s | Per-call timeout — the only runtime-side knob (no runtime caching) |

**Dead-config rule:** RBAC active + `fallback: false` + no `middleware` block would reject every request — the formation fails to load. (With `fallback: <group>` the combination is legal: every request gets the fallback tier.)

**Pipeline** (identical for external requests and the internal origins — heartbeat and scheduler synthesize the same payload and traverse the same steps):

```
client-key auth (external) / internal origin
   └─ middleware (if declared)         request payload -> request payload (+ groups)
        └─ rbac (if active)
             groups attached? -> resolve permissions from groups/
             no groups?       -> fallback group | reject
                  └─ process request (filtered context)
```

#### The Middleware Tool Contract

The middleware **must** be an actual MCP server (stdio or http) exposing exactly one tool named `middleware` whose input and output schemas are defined by the spec. At formation load the runtime connects, lists tools, and **fails fast** if the tool is absent or its declared schema does not match the contract.

- **Input:** the full request payload — `user_id`, `message`, `attachments`, `metadata`, `route_class` — as the tool arguments. `groups` is **never** part of the inbound payload; an input schema declaring it fails formation load. Groups can only be attached on the way out, so they can never arrive as a caller's claim.
- **Output:** the same-shaped payload, possibly modified, plus an optional `groups` list of group ids — the **only** channel through which memberships enter the runtime. Identity mapping (rewriting `user_id`) and payload policy are permitted; `route_class` must be echoed unchanged. Every response is validated against the request schema before the runtime continues with it.
- **`route_class`** identifies the origin: external routes (`chat`, `audiochat`, `trigger`, `api`) and the internal origins `heartbeat`, `scheduler`, and `delegation` (coding-delegation completion re-entry) — internal requests traverse the middleware identically, no special cases.

**Fail-closed:** a middleware error, timeout, or malformed/schema-invalid response rejects the request. `rbac.fallback` does not apply to errors — a fallback on error would let an identity-provider outage silently reassign users to the fallback group. **No runtime-side caching:** the middleware is called on every request; respond fast, cache internally if needed.

> [!NOTE]
> **Removed surface.** Earlier revisions specified `server.auth: required|open` gated by a runtime-side user/membership database. Both are removed; a formation still carrying `server.auth` fails to load with a migration error. The client key authenticates the calling application; user-level gating is `rbac.fallback: false` (grouped users only) plus a middleware that returns no groups for unknown users.

See `schemas/middleware/` for the full tool payload schema and a template walkthrough.

Group permission files live in a `groups/` directory and are **auto-discovered** (content/policy tier — no manifest entry, unlike agents/MCP/A2A/skills). A group file grants nothing until the middleware attaches its id to a request (or `rbac.fallback` names it), so discovery-on-presence is safe. An empty `groups/` directory is inert (warning only).

#### Group Definition Format

```yaml
# groups/analyst.afs -- id derives from the filename stem
name: "Business Analyst"                # optional
description: "Analysis and reporting"   # optional
inherits: base-user                     # optional; string or list

# Plain lists are allow-lists. Use the long form {allow: ..., deny: ...}
# when subtracting from wildcards or overriding inherited allows.
agents:
  - researcher                          # plain grant -- inherits the agent's own config
  - report-writer
  - db-assistant:                       # grant + agent-scoped tool override
      database-mcp:
        tools:
          allow: [get_financials, list_orders]

# Group-wide tool overrides per MCP server -- applies to every granted
# agent that attaches the server.
mcp_servers:
  database-mcp:
    tools:
      deny: ["update_*", "delete_*"]

triggers:
  - invoice-processor
  - "report-*"

sops: "*"

# Native runtime apps visible to this group.
native_apps:
  - memory-visualizer

# Shared-memory write grants.
memory:
  write: ["group:analyst"]

# Watch quota override (only watch.max_concurrent is supported here) --
# mirrors the formation's mcp.watch shape. Highest value across a user's
# groups wins; no group value = formation default.
mcp:
  watch:
    max_concurrent: 25
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `name` | ❌ No | string | None | Human-readable group name |
| `description` | ❌ No | string | None | Optional description |
| `inherits` | ❌ No | string/list | None | Parent group id(s); resolved depth-first, cycles are a load error |
| `agents` | ❌ No | list/`"*"`/map | None | Allowed agents; entries are strings or single-key dicts with per-agent tool overrides |
| `mcp_servers` | ❌ No | map | None | Per-server `tools:` override blocks (`allow`/`deny`) |
| `triggers` | ❌ No | list/`"*"`/map | None | Allowed triggers |
| `sops` | ❌ No | list/`"*"`/map | None | Allowed SOPs |
| `native_apps` | ❌ No | list/`"*"`/map | None | Allowed native apps (no section = all non-privileged apps) |
| `memory.write` | ❌ No | list | None | Shared-memory write scopes |
| `mcp.watch.max_concurrent` | ❌ No | integer ≥ 1 | None | Per-user watch quota override (see [Watch Configuration](#watch-configuration-mcpwatch)); highest of a user's groups wins |

#### Permission Resolution Rules

1. **Deny takes precedence over allow.** If any of a user's groups denies a resource, it is denied.
2. **Union of allows** across all of a user's groups.
3. **Wildcards** — patterns are POSIX `fnmatch` globs (`*`, `?`, `[...]`) in both allow and deny lists.
4. **Inheritance** — parent permissions resolve first; list sections merge additively; a child's tool-override block **replaces** the parent's block for the same (agent, server) key; deny in the child overrides allow in the parent.
5. **No `groups/` directory** = RBAC is inactive under `active: auto`; no resource filtering.
6. **A request that ends up with no groups** (no middleware, or the middleware cleanly returned none) is rejected — unless `rbac.fallback` names a group, in which case it proceeds with that group's permissions.

#### The Tool Override Cascade

Tool control is one concern appearing at four levels; the most specific level wins:

| Level | Keys | Role |
|-------|------|------|
| Formation `mcp.servers[].tools` | `allow` / `deny` (either or both) | Hard catalog bound — pruned at registration; nothing below can resurrect a pruned tool |
| Agent `mcp_servers` attachment `tools` | `allow` / `deny` (either or both) | The agent's default tool surface for that server — on an inline (agent-private) definition or on a `{id, tools}` reference to a formation-declared server; applied after the registry bound |
| Group `mcp_servers.<id>.tools` | `allow` / `deny` (either or both) | Group-wide override for that server, across all granted agents |
| Group `agents.<agent>.<id>.tools` | `allow` / `deny` (either or both) | Most specific: this group, this agent, this server |

An agent's `mcp_servers` entry may be a plain string (attach the formation-declared server as-is), a `{id, tools}` mapping (attach it with a narrowing override), or a full inline definition (agent-private server, optionally with its own `tools` block). Attachment-level `tools` blocks chain **after** the registry bound: they select from the already-pruned catalog, so an attachment can narrow the agent's view but never resurrect a registry-pruned tool.

**Group override semantics:** if a group provides a `tools:` block, it **supersedes** the inherited block; otherwise the inherited config applies unchanged. Within a block: `allow` alone = exactly this set (expanded against the post-registry catalog, so a group override may supersede — not merely intersect — the agent's inherited view); `deny` alone = inherited minus these; both = allow-then-subtract. `tools: {deny: "*"}` hides a server from a group entirely. Cross-group merge: union of allows, any group's deny wins (deny is global, allow is per-group).

> [!NOTE]
> **Uniform vocabulary.** All four levels use `allow`/`deny`, either or both, with deny applied after allow (deny wins on overlap). A single string pattern is accepted wherever a list is (the `deny: "*"` idiom). At the registry and attachment levels, `whitelist`/`blacklist` are accepted as aliases of `allow`/`deny`; declaring a canonical key together with its own alias in one block (`allow` + `whitelist`, or `deny` + `blacklist`) is a load-time error. Group blocks accept the canonical keys only.

> [!NOTE]
> **Registry is not grant.** The formation-level `mcp.servers` list defines connections and prunes tool catalogs; capability flows to an agent only via that agent's `mcp_servers` attachment.

**Design principle:** tool granularity is the permission granularity. Ship semantic tools (`get_financials`, `update_order`), not generic ones (`query`); the cascade composes well-designed tools and does not attempt data-level enforcement inside badly-designed ones.

### Input Limits Configuration
*Input validation limits to prevent denial-of-service attacks and enforce reasonable boundaries*

```yaml
input_limits:
  max_message_length: 100000        # 100KB for chat messages
  max_file_size_bytes: 52428800     # 50MB for file uploads
  max_memory_entry_size: 10000      # 10KB for memory entries
  max_tool_output_size: 1048576     # 1MB for tool outputs
  max_batch_items: 100              # Maximum batch size
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `input_limits.max_message_length` | ❌ No | integer | 100000 | Maximum chat message length in characters (100KB) |
| `input_limits.max_file_size_bytes` | ❌ No | integer | 52428800 | Maximum file upload size in bytes (50MB) |
| `input_limits.max_memory_entry_size` | ❌ No | integer | 10000 | Maximum memory entry size in characters (10KB) |
| `input_limits.max_tool_output_size` | ❌ No | integer | 1048576 | Maximum tool output size in bytes (1MB) |
| `input_limits.max_batch_items` | ❌ No | integer | 100 | Maximum number of items in batch operations |

> [!NOTE]
> These limits protect against denial-of-service attacks and enforce reasonable input boundaries. When limits are exceeded, users receive clear error messages with suggestions on how to proceed.

> [!TIP]
> **Default values are suitable for most formations.** Only adjust these if you have specific requirements:
> - **Large documents**: Increase `max_file_size_bytes` for document processing use cases
> - **Streaming data**: Increase `max_tool_output_size` for tools that return large datasets
> - **Batch operations**: Increase `max_batch_items` for bulk processing scenarios

---

### LLM Model Aliases
*Semantic model names usable anywhere a `model:` reference is accepted*

```yaml
llm:
  aliases:
    fast: "openai/gpt-4o-mini"
    premium: "anthropic/claude-sonnet-4-5"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `llm.aliases` | ❌ No | map | None | Alias name → fully qualified `provider/model` string |

Rules:
- Alias names must match `[a-zA-Z0-9_-]+`.
- Alias values must be fully qualified `provider/model` strings.
- Alias names must **not** collide with capability names (`text`, `vision`, `audio`, `video`, `documents`, `embedding`, `streaming`).
- Aliases are accepted anywhere a `model:` reference is: SOP frontmatter, trigger frontmatter, skill frontmatter, and SOP step `[model:x]` directives. Every `model:` reference is validated at load time against `llm.aliases` or the `provider/model` form. See [Model Selection Hierarchy](#model-selection-hierarchy-model-references).

---

### Overlord Soul Configuration
*The orchestrator's persona (identity, tone, values)*

```yaml
# formation.afs — inline fallback; a SOUL.md file next to this file wins
overlord:
  soul: |
    You are Fynn, a helpful assistant for Company XYZ.
```

The soul is auto-discovered by fixed filename next to the formation file. Resolution precedence (first match wins):

1. `SOUL.md` next to the formation file
2. `soul.md` next to the formation file
3. inline `overlord.soul`
4. runtime built-in default persona

Rules:
- The soul document content is used verbatim (no templating).
- Soul is **overlord-only**. Agents are single-file contained — an agent's character lives in its `system_message`; there is no per-agent `soul` field.

---

### Workflow Replanning Configuration (`overlord.workflow.replanning`)
*A fundamentally different plan when task-level recovery is exhausted — OFF by default*

When a workflow fails after task-level recovery (retries, fallbacks) is exhausted, replanning asks the task decomposer for a fundamentally different plan that avoids the observed failure modes. Disabled by default so existing formations keep byte-identical behavior.

```yaml
overlord:
  workflow:
    replanning:
      enabled: true
      max_attempts: 3
      plan_similarity_threshold: 0.7
      preserve_successful_outputs: true
      replan_timeout_seconds: 30
      non_replannable_error_patterns: ["auth", "permission", "invalid api key"]
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `replanning.enabled` | ❌ No | boolean | false | Enable workflow-level replanning |
| `replanning.max_attempts` | ❌ No | integer 1-10 | 3 | Maximum replanning attempts per original workflow |
| `replanning.plan_similarity_threshold` | ❌ No | number 0-1 | 0.7 | Replanned workflows with task-signature similarity at or above this are rejected as duplicates of the failed plan |
| `replanning.preserve_successful_outputs` | ❌ No | boolean | true | Include successful task results in the replan context so completed work is not redone |
| `replanning.replan_timeout_seconds` | ❌ No | number ≥ 1 | 30 | Timeout for generating a replacement plan |
| `replanning.non_replannable_error_patterns` | ❌ No | list of strings | auth/permission/credential/config/corruption set | Case-insensitive substrings identifying task errors a different plan cannot fix; entries must be non-empty (a blank substring matches everything) |

Unknown keys in the block fail the load. Replanned workflows re-enter the decomposer through the normal pipeline, so permission and access rules apply unchanged.

---

### Memory Configuration
*Memory systems for context retention and long-term storage*

Agent Formation supports three memory tiers:
- **Working Memory**: Shared vector storage backend (always enabled)
- **Buffer Memory**: Recent conversation context (always enabled)
- **Persistent Memory**: Long-term storage in SQLite or PostgreSQL

#### Working Memory Configuration

```yaml
memory:
  working:
    max_memory_mb: auto      # Auto-calculate based on system memory (10% of RAM, 64MB-1GB)
    fifo_interval_min: 5     # FIFO cleanup interval in minutes
    vector_dimension: 1536   # Dimension for embedding vectors
    mode: "local"            # "local" or "remote"
    remote:                  # Only if mode is "remote"
      url: "tcp://localhost:8000"
      api_key: "${{ secrets.FAISSX_API_KEY }}"
      tenant: "${{ secrets.FAISSX_TENANT_ID }}"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `memory.working.max_memory_mb` | ❌ No | int/string | "auto" | Memory limit (auto = 10% RAM, capped 64MB-1GB) |
| `memory.working.fifo_interval_min` | ❌ No | integer | 5 | FIFO cleanup interval in minutes |
| `memory.working.vector_dimension` | ❌ No | integer | 1536 | Embedding vector dimension |
| `memory.working.mode` | ❌ No | string | "local" | Storage mode: "local" or "remote" |

#### Buffer Memory Configuration

```yaml
memory:
  buffer:
    size: 10              # Context window size
    multiplier: 10        # Buffer multiplier (total = size * multiplier)
    vector_search: true   # Enable vector similarity search
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `memory.buffer.size` | ❌ No | integer | 10 | Number of recent messages in context |
| `memory.buffer.multiplier` | ❌ No | integer | 10 | Buffer multiplier for total storage |
| `memory.buffer.vector_search` | ❌ No | boolean | true | Enable semantic search in buffer |

#### Persistent Memory Configuration

Persistent memory provides long-term storage across sessions using SQLite or PostgreSQL.

**Default Behavior**: When `memory.persistent` is omitted, SQLite is automatically enabled with a database file created in the formation directory (`memory.db`). This means formations have persistent memory out of the box with zero configuration.

```yaml
# Example 1: Default SQLite (recommended for single-user/development)
# Just omit the persistent key entirely - SQLite db created automatically
memory:
  buffer: { size: 20 }
  # persistent not specified = auto SQLite in formation directory

# Example 2: Explicitly disable persistent memory
memory:
  persistent: false

# Example 3: Disable but preserve config (useful during development)
memory:
  persistent:
    enabled: false
    connection_string: "postgresql://user:pass@localhost:5432/db"
    embedding_model: "text-embedding-ada-002"

# Example 4: PostgreSQL for multi-user/production
memory:
  persistent:
    connection_string: "postgresql://user:password@localhost:5432/dbname"
    embedding_model: "text-embedding-ada-002"
    query_timeout_seconds: 30
    user_synopsis:
      enabled: true
      cache_ttl: 3600
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `memory.persistent` | ❌ No | object/false | auto SQLite | Persistent memory config, or `false` to disable |
| `memory.persistent.enabled` | ❌ No | boolean | true | Enable/disable (useful to preserve config while disabled) |
| `memory.persistent.connection_string` | ❌ No | string | SQLite in formation dir | Database connection string |
| `memory.persistent.embedding_model` | ❌ No | string | From llm.models | Model for generating embeddings |
| `memory.persistent.query_timeout_seconds` | ❌ No | integer | 30 | Maximum time for SQL queries |
| `memory.persistent.user_synopsis.enabled` | ❌ No | boolean | true | Add user context to system message |
| `memory.persistent.user_synopsis.cache_ttl` | ❌ No | integer | 3600 | Synopsis cache TTL in seconds |

**Connection String Formats**:
- PostgreSQL: `postgresql://user:password@host:port/dbname`
- SQLite (explicit): `sqlite:///path/to/memory.db` or just `memory.db`
- Default (omit): SQLite file created as `memory.db` in formation directory

> [!NOTE]
> **Single-user vs Multi-user Mode**: SQLite backends automatically run in single-user mode (all requests use user_id "0"). For multi-user isolation with per-user memory partitions, use PostgreSQL.

> [!TIP]
> **Development Workflow**: Use `enabled: false` to temporarily disable persistent memory while preserving your PostgreSQL configuration. This is useful for debugging or testing without persistence.

#### Memory Ingestion Configuration (`memory.ingestion`)
*Tiered extraction, entity resolution, and synthesis cadences for ingested memory*

Controls how raw ingested items (e.g. connected sources like email) become structured memory: a tier-escalation pipeline (T1 local classify/store → T2 default-model LLM extraction → T3 frontier extraction for high-signal items), periodic entity resolution, and scheduled synthesis passes. Everything defaults ON with the values below; the block is optional.

```yaml
memory:
  ingestion:
    max_in_flight_per_user: 4        # concurrent processing bound (lenient fallback)
    sources:
      gmail:
        filter: strict               # strict | lenient | off (per-source noise gate)
        tier: 2                      # optional per-source tier pin (1 | 2 | 3)
    tiers:                           # escalation heuristics (T1 -> T2 -> T3)
      enabled: true
      ambiguity_margin: 0.05         # classify margin below this -> escalate to T2
      t3_signal_score: 5             # signal score at/above -> T3
      models:
        t2: "openai/gpt-4o-mini"     # optional; default extraction model
        t3: "anthropic/claude-..."   # optional; falls back to the t2 model
      budget:
        t2_items_per_job: 100        # LLM-extraction cap per processing job
        t3_items_per_job: 10         # frontier cap per processing job
    entity_resolution:
      enabled: true
      auto_merge_threshold: 0.85     # score at/above -> auto-merge
      flag_threshold: 0.5            # score at/above (below merge) -> flag for review
      entity_types: [person]
      max_entities: 200              # per-user scan bound per pass
    synthesis:                       # cadence table; each individually disableable
      enabled: true
      hot:       { enabled: true, interval_seconds: 300 }
      warm:      { enabled: true, interval_seconds: 3600 }
      cold:      { enabled: true, interval_seconds: 86400 }
      cold_cold: { enabled: true, interval_seconds: 604800 }
      patterns:
        enabled: true
        min_events: 20               # a schedule pattern needs this many events
        top_k: 3                     # items per rendered pattern fact
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `ingestion.max_in_flight_per_user` | ❌ No | integer | 4 | Concurrent processing bound per user (lenient fallback on bad values) |
| `ingestion.sources.<name>.filter` | ❌ No | string | — | Per-source noise gate: `strict` \| `lenient` \| `off` (lenient fallback) |
| `ingestion.sources.<name>.tier` | ❌ No | 1 \| 2 \| 3 | — | Pin a source to one processing tier (strict; anything else fails load) |
| `ingestion.tiers.enabled` | ❌ No | boolean | true | Enable tier escalation heuristics |
| `ingestion.tiers.ambiguity_margin` | ❌ No | number 0-1 | 0.05 | Classification margin below this escalates the item to T2 |
| `ingestion.tiers.t3_signal_score` | ❌ No | positive integer | 5 | Signal score at/above this escalates to T3 |
| `ingestion.tiers.models.t2` / `.t3` | ❌ No | model string | text model / t2 model | Optional extraction model overrides; `t3` falls back to `t2` |
| `ingestion.tiers.budget.t2_items_per_job` | ❌ No | positive integer | 100 | LLM-extraction cap per processing job |
| `ingestion.tiers.budget.t3_items_per_job` | ❌ No | positive integer | 10 | Frontier-extraction cap per processing job |
| `ingestion.entity_resolution.enabled` | ❌ No | boolean | true | Enable periodic entity resolution |
| `ingestion.entity_resolution.auto_merge_threshold` | ❌ No | number 0-1 | 0.85 | Match score at/above auto-merges entities |
| `ingestion.entity_resolution.flag_threshold` | ❌ No | number 0-1 | 0.5 | Score at/above (below merge) flags for review; must not exceed `auto_merge_threshold` |
| `ingestion.entity_resolution.entity_types` | ❌ No | non-empty list | `[person]` | Entity types to resolve (normalized lowercase) |
| `ingestion.entity_resolution.max_entities` | ❌ No | positive integer | 200 | Per-user scan bound per pass |
| `ingestion.synthesis.enabled` | ❌ No | boolean | true | Master switch for synthesis cadences |
| `ingestion.synthesis.<cadence>.enabled` | ❌ No | boolean | true | Per-cadence switch (`hot`/`warm`/`cold`/`cold_cold`) |
| `ingestion.synthesis.<cadence>.interval_seconds` | ❌ No | positive number | 300 / 3600 / 86400 / 604800 | Cadence intervals: 5m / hourly / nightly / weekly |
| `ingestion.synthesis.patterns.enabled` | ❌ No | boolean | true | Enable schedule-pattern synthesis |
| `ingestion.synthesis.patterns.min_events` | ❌ No | positive integer | 20 | Minimum events before a pattern is synthesized |
| `ingestion.synthesis.patterns.top_k` | ❌ No | positive integer | 3 | Items per rendered pattern fact |

Validation is fail-fast at load with the full config path in every error; booleans are rejected wherever numbers are expected. (The two pre-existing keys, `max_in_flight_per_user` and `sources.<name>.filter`, keep their shipped lenient-fallback semantics.)

---

### Knowledge Configuration (`knowledge:`)
*Local and remote knowledge sources, plus reasoning-RAG retrieval settings*

Knowledge sources give agents reference material for context-aware responses. A source is either **local** (a `path` relative to the formation directory) or **remote** (a `url` synced into a local mirror before ingestion). Declared at the agent level (and, where the runtime supports it, formation-wide) as a `sources` list:

```yaml
knowledge:
  enabled: true
  sources:
    - path: "knowledge/faq/"
      description: "Frequently asked questions"
    - url: "s3://my-bucket/docs/*.pdf"
      description: "Product documentation"
      id: product-docs                 # optional; derived from the URL when absent
      auth:
        type: aws                      # omit keys to use the ambient credential chain
        access_key: "${{ secrets.AWS_ACCESS_KEY }}"
        secret_key: "${{ secrets.AWS_SECRET_KEY }}"
      include: ["*.pdf"]
      exclude: ["drafts/*"]
      schedule: "@daily"               # cron expression or alias; needs the scheduler
```

**Local sources**: `path` must be relative to the formation root; absolute paths and `..` traversal are rejected (formations stay self-contained and portable).

**Remote sources** (`url`): supported schemes are `http://`, `https://`, `s3://`, `gs://`, `az://`, `rsync://`, `rsync+ssh://`, `ftp://`, `sftp://`, and `file://` (bind mounts; absolute local paths only). Remote content is **mirrored, then ingested**: each source syncs into a runtime-owned local cache (never into the formation directory, which may be read-only) and the ordinary local ingestion pipeline runs on the mirror. A failing sync never blocks formation startup or chat — per-file failures keep the previously synced copy, and a total failure degrades to whatever the last successful sync recorded.

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `url` | ✅ Yes* | string | — | Source URL (*exactly one of `path`/`url` per source) |
| `description` | ✅ Yes | string | — | Human-readable source description |
| `id` | ❌ No | string | derived slug-hash | Stable source identifier; must be unique within the list |
| `auth` | ❌ No | map | — | Scheme-appropriate auth block (see below); required for `az://` |
| `headers` | ❌ No | string map | — | Extra request headers; `http(s)://` only |
| `include` / `exclude` | ❌ No | list of patterns | — | fnmatch filters applied to synced file paths |
| `max_files` | ❌ No | positive integer | 100 | Per-source file count bound |
| `max_file_size` | ❌ No | positive integer | 10485760 | Per-file size bound (bytes, 10MB) |
| `max_total_size` | ❌ No | positive integer | 104857600 | Per-source total size bound (bytes, 100MB) |
| `timeout` | ❌ No | positive integer | 300 | Sync timeout (seconds) |
| `accept_new_host_keys` | ❌ No | boolean | false | `rsync+ssh`/`sftp` only: opt into SSH trust-on-first-use (default requires the host in `known_hosts`) |
| `extract` | ❌ No | boolean | false | Treat the URL as a single downloadable archive; extracted contents become the source's files. Not valid for `rsync` schemes or glob URLs |
| `extract_pattern` | ❌ No | glob string | — | Filter for extracted entries; requires `extract: true` |
| `max_extracted_files` / `max_extracted_size` | ❌ No | positive integer | runtime default | Decompression-bomb bounds; require `extract: true` |
| `schedule` | ❌ No | string | — | Periodic re-sync: a cron expression or `@startup` \| `@hourly` \| `@daily` \| `@weekly`. Requires the scheduler service; without it, sources sync at startup only (loud warning) |
| `retry` | ❌ No | map | — | Re-sync retry policy: `max_attempts` (integer ≥ 1), `initial_delay` / `max_delay` (positive seconds), `exponential_base` (number ≥ 1); unknown keys fail load |

**Auth types by scheme** (credentials belong in `${{ secrets.* }}` references):

| Scheme | Auth types | Required fields |
|--------|-----------|-----------------|
| `http` / `https` | `basic`, `bearer` | `username`+`password` / `token` |
| `s3` | `aws` | `access_key`+`secret_key` together, or neither (ambient credential chain) |
| `gs` | `gcp` | optional `credentials_json` (else Application Default Credentials) |
| `az` | `azure` (required) | `connection_string`, or `account_name`+`account_key` |
| `rsync+ssh` | `ssh_key` | `key` |
| `ftp` | `basic` | `username`+`password` |
| `sftp` | `ssh_key`, `basic` | `key` / `username`+`password` |
| `rsync`, `file` | none | — |

Scheme-specific structural rules (all load-time errors): `http(s)` and `rsync` URLs reject glob patterns (`http` has no directory listing; `rsync` uses `include`/`exclude` instead); `s3`/`gs`/`az` need a bucket or container in the URL; `file://` requires an absolute local path.

**Reasoning-RAG settings** (agent-level, optional): large sources can be indexed as navigable trees instead of flat vectors.

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `knowledge.reasoning_threshold` | ❌ No | integer ≥ 0 | runtime default | Token size at/above which a source gets reasoning-based indexing; 0 disables it |
| `knowledge.tree` | ❌ No | map | — | Tree-build tuning; closed key set: `model`, `terminator_model`, `max_depth`, `max_pages_per_node`, `max_tokens_per_node`, `max_document_tokens`, `max_sufficiency_rounds`, `max_fetched_nodes_pct` (model references participate in the model-selection hierarchy) |
| `sources[*].retrieval` | ❌ No | string | `vector` | Per-source retrieval mode: `vector` \| `tree` \| `tree-vector` \| `hybrid` |
| `sources[*].agent_tree` | ❌ No | map | — | Persistent per-agent tree; only key: `regenerate` (`manual` \| `on-source-change` \| `on-formation-load`). Requires a tree-capable `retrieval` mode |

---

### Proactive Configuration
*Outbound notification channels and an optional autonomous heartbeat*

```yaml
proactive:
  channels:
    slack:
      transformer: slack                    # transformer name (formation transformers/
                                            # first, then bundled templates)
      url: "${{ secrets.SLACK_WEBHOOK }}"   # optional; overrides the transformer's endpoint.url
  default_channel: slack                    # channel name or literal "webhook"
  heartbeat:
    enabled: true
    interval: "30m"
    target: "last"                          # last | preferred | webhook | <channel name>
    active_hours:
      start: "09:00"
      end: "18:00"
      timezone: "UTC"                       # IANA name or literal "user"
      weekends: true
    sop: "my-heartbeat"
    instruction: "Focus on today's prep"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `proactive.channels` | ❌ No | map | {} | Channel name (`[a-zA-Z0-9_-]+`) → `{transformer, url?}` |
| `proactive.channels.<name>.transformer` | ✅ Yes (per channel) | string | None | Transformer name (no path) |
| `proactive.channels.<name>.url` | ❌ No | string | None | http(s) URL or `${{ secrets.* }}`; wins over the transformer's `endpoint.url`; **required at load** if the transformer declares none |
| `proactive.default_channel` | ❌ No | string | None | Fallback channel: a declared channel name or literal `webhook` |
| `proactive.heartbeat.enabled` | ❌ No | boolean | true (when block present) | Requires `scheduler.enabled: true` (load-time check) |
| `proactive.heartbeat.interval` | ❌ No | string | "30m" | Duration: `Ns`/`Nm`/`Nh`, optional "every " prefix |
| `proactive.heartbeat.target` | ❌ No | string | "last" | `last` \| `preferred` \| `webhook` \| channel name |
| `proactive.heartbeat.active_hours.start/end` | ✅ Yes (when block present) | string | None | 24-hour `HH:MM`; start > end wraps past midnight |
| `proactive.heartbeat.active_hours.timezone` | ❌ No | string | "UTC" | IANA name or literal `user` (per-user timezones) |
| `proactive.heartbeat.active_hours.weekends` | ❌ No | boolean | true | `false` suppresses Saturday/Sunday |
| `proactive.heartbeat.sop` | ❌ No | string | None | Formation SOP replacing the runtime's bundled default heartbeat SOP; must exist at load |
| `proactive.heartbeat.instruction` | ❌ No | string | None | Appended to the heartbeat prompt |

Rules:
- `last`, `preferred`, and `webhook` are reserved routing targets and cannot be channel names.
- Per-notification routing precedence: explicit channel > user-preferred channel > `default_channel` > the formation's async webhook.

---

### Commands Configuration
*Opt-in slash-command surface*

```yaml
commands:
  enabled: true
  aliases:
    tasks: jobs        # /tasks resolves like /jobs
  builtin:
    reset: false       # hide the built-in /reset
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `commands.enabled` | ❌ No | boolean | true (when block present) | Enable the command surface |
| `commands.aliases` | ❌ No | map | {} | Alias → command/SOP name (both `[a-zA-Z0-9_-]+`) |
| `commands.builtin` | ❌ No | map | {} | Built-in name → boolean; `false` hides it; unknown names fail validation |

Resolution order: alias expansion → formation SOPs by name (**a formation SOP shadows a built-in command of the same name**) → built-in registry. Reference built-in set: `setup`, `help`, `status`, `jobs`, `identity`, `channels`, `preferences`, `reset`.

---

### Artifacts Configuration
*Artifact capture, storage, and retention*

Artifact capture is **on by default** — omitting the block still yields local artifact storage with the defaults below.

```yaml
artifacts:
  enabled: true
  storage:
    type: "local"               # v1: local only
    path: "./artifacts"
  encryption:
    enabled: true
  retention:
    policy: "last_accessed"     # or "last_updated"
    duration: 0                 # days; 0 = forever
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `artifacts.enabled` | ❌ No | boolean | true | Enable artifact capture |
| `artifacts.storage.type` | ❌ No | string | "local" | `local` only in v1; other backends (e.g. `s3`) are rejected at load |
| `artifacts.storage.path` | ❌ No | string | "./artifacts" | Storage path relative to the formation directory |
| `artifacts.encryption.enabled` | ❌ No | boolean | true | Encrypt stored artifacts |
| `artifacts.retention.policy` | ❌ No | string | "last_accessed" | `last_accessed` or `last_updated` |
| `artifacts.retention.duration` | ❌ No | integer | 0 | Retention window in days; `0` = keep forever |

---

### Links Configuration (`links:`)
*Declared external destinations (credential portals, dashboards) for response affordances*

An optional **top-level** mapping of `name -> {label, url, hint}`. Entries declare the external destinations that response producers may surface to clients as `action_link` widgets in the response envelope's `ui` array — with formation-config provenance. An `action_link` URL is never LLM-fabricated: it can only come from a declared link, a tool result, or a trigger payload (see `specs/formation.md` §9).

```yaml
links:
  jira:
    label: "Connect Jira"                          # optional display label
    url: "https://auth.acme.com/connect/jira"      # required; http(s) only
    hint: "Opens your company's credential portal" # optional one-liner
  status:
    url: "https://status.acme.com"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `links.<name>` | ❌ No | map | None | One declared destination; must be a mapping with a `url` field |
| `links.<name>.url` | ✅ Yes | string | None | Destination URL; **must** be `http://` or `https://` |
| `links.<name>.label` | ❌ No | string | None | Display label for the link affordance |
| `links.<name>.hint` | ❌ No | string | None | One-line hint shown alongside the link |

---

### Coding Delegation Configuration (`coding:`)
*Delegate coding tasks to an external headless coding CLI as tracked background jobs*

A **top-level** block (framework-mode friendly, like `rbac:`/`middleware:`). Presence registers one always-asynchronous delegation tool (`delegate_coding(prompt, workdir?, model?, continue_job_id?)` in the reference implementation); **absence means nothing is constructed** — no tool, byte-identical behavior. The runtime verifies the CLI binary exists at load; installing, authenticating, and sandboxing it is the developer's responsibility, and vendor taxonomies (permission modes, safety levels, model names) pass through opaquely.

```yaml
coding:
  client: claude-code            # bundled adapter template (reference set:
                                 # claude-code, droid, opencode, pi), or a
                                 # formation-local coding/<name>.yaml (shadows
                                 # the bundled one). Mutually exclusive with
                                 # the inline adapter form.
  model: sonnet                  # optional default; opaque vendor namespace
  workdirs: ["./workspace"]      # required; declared roots, must exist at load
  cleanup: delete                # delete (default) | keep
  timeout: 30m                   # per-delegation ceiling (default 30m)
  max_concurrent: 3              # default 3
  groups: []                     # allowlist; empty/absent = everyone may delegate
  extra_args:                    # verbatim vendor passthrough (safety flags)
    - "--permission-mode"
    - "acceptEdits"
  env:                           # the ONLY place ${{ secrets.* }} resolves
    ANTHROPIC_API_KEY: "${{ secrets.ANTHROPIC_API_KEY }}"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `coding.client` | ❌ Conditional | string | None | Adapter template name (`[a-zA-Z0-9_-]+`): formation-local `coding/<name>.yaml` shadows the bundled template. Mutually exclusive with the inline adapter keys; one of the two is required |
| `coding.command` / `coding.args` / `coding.output` / `coding.parse` | ❌ Conditional | — | — | Inline adapter form (escape hatch); same schema as a template file (below) |
| `coding.model` | ❌ No | string | None | Default model value — **opaque vendor namespace** (not `llm.aliases`); overridable per delegation call. Requires the adapter to define an `args.model` fragment |
| `coding.workdirs` | ✅ Yes | list | — | Declared root directories (relative to the formation dir or absolute); each must exist at load (symlink-resolved). Every delegation runs in a fresh `<root>/<user_id>/<request_id>` subdirectory as subprocess cwd — never the root itself. The tool's `workdir` param selects a declared root (default: the first) |
| `coding.cleanup` | ❌ No | string | `delete` | `delete`: remove the delegation directory on terminal state (a TTL sweep catches directories orphaned by crashed runs). `keep`: opt-in for debugging |
| `coding.timeout` | ❌ No | duration | `30m` | Per-delegation ceiling (bare seconds or `ms`/`s`/`m`/`h`; must be positive). On expiry the process group is killed and the job marked timed out; the session id is retained (the task stays resumable) |
| `coding.max_concurrent` | ❌ No | integer | 3 | Concurrent delegations per formation (≥ 1); overflow is a friendly tool error, not a queue |
| `coding.groups` | ❌ No | list | `[]` | Resource-side allowlist gating who may delegate (as one unit). Empty/absent = every group. Each name must exist in `groups/` when RBAC is active |
| `coding.extra_args` | ❌ No | list | `[]` | Verbatim vendor passthrough — permission/safety/autonomy flags (`--permission-mode`, `--auto`, `--dangerously-skip-permissions`, ...). Never modeled by the standard. Flags in the adapter's `forbidden_extra_args` (cwd/worktree flags) fail the load |
| `coding.env` | ❌ No | map | `{}` | String → string subprocess environment. **The only place `${{ secrets.* }}` resolves** — a secrets reference anywhere else in the block fails the load pointing at `env:` (argv is `ps`-visible; the environment is not) |

Unknown keys on `coding:` fail the load.

#### The Adapter Schema

An adapter (bundled template, formation-local `coding/<name>.yaml`, or inline) drives one CLI. Allowed keys: `name` (templates only; must match the filename stem), `command`, `args`, `output`, `parse`, `forbidden_extra_args`.

| Key | Required | Description |
|-----|----------|-------------|
| `command` | ✅ Yes | The CLI binary — bare name (resolved on PATH) or absolute path |
| `args.prompt` | ✅ Yes | Fragment containing `{prompt}`, or the literal string `stdin` (prompt written to stdin — required past argv limits) |
| `args.base` | ❌ No | Fragments always present, in order |
| `args.session` | ❌ No | ONE idempotent create-or-resume fragment containing `{id}` |
| `args.session_new` / `args.session_resume` | ❌ No | Distinct create/resume pair, each containing `{id}` |
| `args.model` | ❌ No | Fragment containing `{model}`; appended only when a model value is set |
| `output` | ❌ No | `stream-json` \| `json` \| `text` (default `text`) — selects the output parser |
| `parse.result` / `parse.session_id` | ❌ No | Dot-path selectors over the vendor's JSON (same idiom as trigger `parse:`; negative list indices allowed) |
| `forbidden_extra_args` | ❌ No | Flags `coding.extra_args` must not contain (the runtime owns the cwd) |

**Command assembly is an exec array, never a shell:** `command` + `args.base` + `args.model` (when a model is set) + session fragment + `extra_args` + `args.prompt` (or stdin).

**Session shapes** — exactly one of three per adapter:

| Shape | Declaration | Id acquisition |
|-------|-------------|----------------|
| Idempotent | `session:` only | Runtime-generated; one flag serves create AND resume (droid) |
| Create/resume pair | `session_new:` + `session_resume:` | Runtime-generated; distinct fragments (claude-code) |
| Captured-id | `session_resume:` only | Tool-assigned; the first run gets NO session flag, the id is captured from output via `parse.session_id` (opencode, pi) |

A captured-id adapter cannot use `output: text` and requires `parse.session_id`. Session-id capture is **first-match** (later events never clobber it); in `stream-json` mode the `result` selector takes the **last non-empty** match across events. The persisted session id is replayed on continuation (`continue_job_id`); agents never see vendor session ids.

**Disposable workdirs; git is the persistence layer.** Nothing durable lives in a delegation directory: ad-hoc tasks need nothing durable, new projects are git-inited and pushed by the tool, existing projects are cloned/coded/push-branched within the run. A resumed session gets a **fresh** directory — conversational continuity is the vendor session id, file continuity is git. The runtime sets the subprocess cwd (and its `PWD`) to the delegation directory.

**Always asynchronous.** The tool returns `{"job_id": ..., "status": "started"}` immediately; there is no synchronous mode and none may be offered. Completion re-enters the originating session as an internal request (`route_class: delegation`) through the full middleware + RBAC pipeline; a run that needs human input simply ends with the question as its final message, and the user's answer resumes the session via `continue_job_id`.

See `schemas/coding/` for the annotated `claude-code` reference adapter and `specs/formation.md` §7 for the normative text.

---

### Watch Configuration (`mcp.watch`)
*Remote async-job watching over MCP tools — cadence, deadline, and quotas*

An optional sub-block of the formation's `mcp:` block. It configures the runtime-registered job-watching tool (`watch_job` in the reference implementation), which polls an MCP status tool at a fixed cadence until a deterministic terminal condition and re-enters the result into the originating conversation.

**Default ON iff the formation declares `mcp.servers`** ("declared" = the raw server list; runtime built-ins do not count). No declared servers → no tool, and a `watch:` block is dead config that fails the load. There is no `enabled:` key — the tool grants no new capability (polls run under the original caller's own permission context) — the sole escape hatch is `mcp: { watch: false }`, which removes the tool entirely.

```yaml
mcp:
  watch:                          # optional; all keys optional
    interval: 30                  # THE poll cadence (seconds) — not agent-pickable
    timeout: 7200                 # THE watch deadline (seconds)
    max_concurrent: 10            # active watches per user
    max_consecutive_failures: 3   # consecutive poll errors before the watch fails
  servers:
    - image-gen-mcp
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `mcp.watch` | ❌ No | map / `false` | defaults when servers are declared | `false` removes the tool; `true` or absent = defaults |
| `mcp.watch.interval` | ❌ No | positive number | 30 | Poll cadence in seconds; first poll after one interval, fixed thereafter. Formation configuration — never a tool argument |
| `mcp.watch.timeout` | ❌ No | positive number | 7200 | Watch deadline in seconds; on expiry the watch resolves as timed out and re-enters with that status |
| `mcp.watch.max_concurrent` | ❌ No | integer ≥ 1 | 10 | Active watches **per user**. Governs watches only — bounds nothing else |
| `mcp.watch.max_consecutive_failures` | ❌ No | integer ≥ 1 | 3 | Consecutive failed polls that fail the watch with the last error |

The key set is closed (unknown keys fail load) and a boolean is rejected wherever a number is expected — all validated fail-fast at formation load, never a watch-time surprise.

#### The `watch_job` Tool Contract

```json
watch_job({
  "tool": "image-gen.check_status",     // any MCP tool visible to the caller
  "args": {"id": "job_abc123"},         // arguments passed on every poll
  "done_when": {"path": "$.status", "in": ["succeeded", "failed", "canceled"]},
  "result": "$.output",                 // optional selector; default: full final body
  "label": "logo render"                // optional; human-readable job label
})
→ {"job_id": "watch_9f2", "status": "watching", "status_url": "/jobs/watch_9f2"}
```

- **Always asynchronous.** Returns a watch handle immediately; the poll loop is background work and completion re-enters the conversation as an internal request through the full middleware + RBAC pipeline, fenced as untrusted content. Runtimes **must not** offer a blocking mode (same rule as coding delegation).
- **`done_when` is deterministic — no LLM in the poll loop.** Closed key set `{path, equals, in}`: `path` is a non-empty dot-path selector into the poll body; exactly one of `equals` (single value) or `in` (non-empty list). Matching is exact equality with a string-form fallback (`equals: "3"` matches numeric `3`) and **strictly typed for booleans — a bool matches only a bool** (no `1 == true` coercion). A missing path means "not terminal yet", never an error. Enumerate **every** terminal state (not just success), or a failed job polls until the deadline.
- Cadence and deadline come from `mcp.watch` — they are **not** tool parameters.
- Watches are tracked jobs: listable and cancellable on the runtime's jobs surface; cancellation stops polling with no re-entry.
- Recognition (job-shaped response → `watch_job` → acknowledgment) ships as a bundled dormant SOP fragment; a formation-local `sops/watch_job.md` shadows it (empty file = removed).

#### Group Watch Quota Override

Group files may raise (or lower) the per-user watch quota, mirroring the formation shape:

```yaml
# groups/power-users.yaml
mcp:
  watch:
    max_concurrent: 25      # overrides the formation default for members
```

Closed key sets at both levels: in a group file `mcp:` supports only `watch`, and `watch:` supports only `max_concurrent` (integer ≥ 1). A user in multiple groups gets the **highest** of their groups' values (grants are additive — the same semantics as every other group list); no group value → formation default. The override governs watches only.

See `specs/formation.md` §8 for the normative text.

---

### Skills Configuration
*Reusable agent capabilities following the Agent Skills specification*

Skills are directories under `skills/` containing a `SKILL.md` file with YAML frontmatter and markdown instructions, plus optional `scripts/`, `references/`, and `assets/` subdirectories.

```yaml
# Formation-level skills (public, available to all agents)
skills:
  - pdf-processing
  - data-analysis

# Executor configuration for skill script execution
executor:
  enabled: true
  image: "muxi/executor:latest"
  port: 5560
  timeout_default: 30
  restart_policy: "always"
  resource_limits:
    memory: "2g"
    cpu: 1.0
```

The `skills:` field also accepts a mapping form that additionally disables named **built-in** skills the runtime would otherwise load automatically:

```yaml
skills:
  names: [pdf-processing, data-analysis]
  disable_builtin: [compute]
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `skills` | No | array/map | [] | List of skill names to load (from skills/ directory), or `{names, disable_builtin}` |
| `skills.names` | No | array | [] | (Mapping form) formation skill names to load |
| `skills.disable_builtin` | No | array | [] | (Mapping form) built-in skill names to hide |
| `executor.enabled` | No | bool | true | Enable skill script execution |
| `executor.image` | No | string | "muxi/executor:latest" | Docker image for executor |
| `executor.port` | No | int | 5560 | ZeroMQ port for executor |
| `executor.timeout_default` | No | int | 30 | Default script timeout (seconds) |
| `executor.restart_policy` | No | string | "always" | Container restart policy |
| `executor.resource_limits.memory` | No | string | "2g" | Memory limit |
| `executor.resource_limits.cpu` | No | float | 1.0 | CPU limit |

**Skill directory structure:**
```
skills/
├── pdf-processing/
│   ├── SKILL.md          # Required: YAML frontmatter + instructions
│   ├── scripts/          # Optional: executable code
│   ├── references/       # Optional: additional documentation
│   └── assets/           # Optional: templates, resources
└── data-analysis/
    └── SKILL.md
```

### Agent-Specific Skills
*Skills private to a specific agent (in addition to formation-level public skills)*

```yaml
skills:
  - ticket-handling      # Private skill for this agent
  - customer-lookup      # Only this agent can use these
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `skills` | No | array | [] | List of skill names private to this agent |

> [!NOTE]
> Agent-level skills are private to that agent only. The agent also has access to all formation-level (public) skills. Skills must exist in the `skills/` directory.

---

## 📋 SOP Schema (`sops/*.md`)

SOPs are markdown files with YAML frontmatter under `sops/`, **auto-discovered** recursively. Only files declaring `type: sop` become SOPs; the id is the filename stem. Other files in `sops/` are loadable resources for `[file:path]` references.

```markdown
---
type: sop                      # REQUIRED literal
name: "Weekly Report"          # optional; defaults to the file stem
description: "Compile and deliver the weekly report"
mode: template                 # template (deterministic) | guide (LLM); default template
tags: reporting, weekly        # comma-separated or list
model: fast                    # optional default model for all steps (alias or provider/model)
bypass_approval: true          # default true
synthesis: true                # default true
---

## Steps

1. **Gather activity** [agent:researcher] [mcp:github/search] [parallel]
   Collect the week's merged PRs and closed issues.

2. **Draft the report** [agent:report-writer] [model:premium]
   Follow the format in [file:templates/report-format.md].
```

| Frontmatter key | Required | Type | Default | Description |
|-----------------|----------|------|---------|-------------|
| `type` | ✅ Yes | string | — | Literal `sop`; activates SOP parsing |
| `name` | ❌ No | string | file stem | Display name |
| `description` | ❌ No | string | None | One-line description (shown by `/help`) |
| `mode` | ❌ No | string | "template" | `template` or `guide` |
| `tags` | ❌ No | string/list | None | Semantic-matching tags |
| `model` | ❌ No | string | None | Alias or `provider/model`; default for all steps |
| `bypass_approval` | ❌ No | boolean | true | Skip workflow plan approval |
| `synthesis` | ❌ No | boolean | true | Run a synthesis pass after execution |

Step directives (in `template` mode; case-insensitive):

| Directive | Description |
|-----------|-------------|
| `[agent:name]` | Route the step to the named agent |
| `[skill:name]` / `[skill:name/script]` | Activate a skill (optionally a specific script) |
| `[mcp:server]` / `[mcp:server/action]` | Declare an MCP capability requirement |
| `[model:x]` | Step-level model override (alias or `provider/model`); wins over frontmatter `model:` |
| `[parallel]` | Remove the sequential dependency on the previous step |
| `[file:path]` | Reference a resource file (resolved at execution time) |

Template: `schemas/sops/weekly-report.md`.

---

## ⚡ Trigger Schema (`triggers/*.md`)

Triggers are markdown files with YAML frontmatter under `triggers/`, **auto-discovered**. The id is the filename stem and must match `^[a-zA-Z0-9_-]+$`. Each trigger is exposed at `POST /v1/triggers/{id}` (client key; the request traverses the middleware + RBAC pipeline like every other route); `GET /v1/triggers` lists, `GET /v1/triggers/{id}` returns metadata.

```markdown
---
name: "GitHub issue intake"    # optional display name
type: webhook                  # optional annotation (semantic only)
channel: github                # optional inbound-channel name (source tracking)
model: fast                    # optional model override (alias or provider/model)
parse:
  message: $.issue.title
  user_id: $.sender.login
  context:
    repo: $.repository.full_name
transformer: slack             # optional outbound payload formatter
webhook: "${{ secrets.OPS_SLACK_WEBHOOK }}"   # optional delivery URL
---
Triage this issue: ${{ data.issue.title }}
```

| Frontmatter key | Required | Type | Default | Description |
|-----------------|----------|------|---------|-------------|
| `name` | ❌ No | string | id | Display-name override |
| `type` | ❌ No | string | None | Type annotation (semantic only) |
| `parse` | ❌ No | map | None | Payload extraction: `message`, `user_id`, `files` (JSONPath strings) + `context` (name → JSONPath map); best-effort |
| `webhook` | ❌ No | string | None | http(s) delivery URL |
| `transformer` | ❌ No | string | None | Transformer name (`^[a-zA-Z0-9_-]+$`) |
| `model` | ❌ No | string | None | Alias or `provider/model` for this trigger's turn |
| `channel` | ❌ No | string | None | Inbound channel name (`^[a-zA-Z0-9_-]+$`); feeds proactive "last channel" routing |

Rules:
- The frontmatter key set is **closed** — unknown keys are a load-time error.
- The body is a markdown instruction template; `${{ data.* }}` placeholders reference the inbound POST payload.
- **Composition:** `webhook:` alone delivers the raw standard payload; `transformer:` alone delivers the formatted payload to the transformer's `endpoint.url`; **both together** deliver the formatted payload to the trigger's `webhook:` URL. A transformer reference with no URL from either side is a load-time error.

Template: `schemas/triggers/github-issues.md`.

---

## 📤 Transformer Schema (`transformers/*.afs`)

Transformers are YAML files under `transformers/`, **auto-discovered**, referenced by name from trigger frontmatter and `proactive.channels`. Runtimes ship bundled dormant, payload-format-only templates (`slack`, `telegram`, `discord`, `email`); a formation-local file of the same name **shadows** the bundled template.

```yaml
name: slack-bridge                      # REQUIRED; must match the filename stem
endpoint:                               # optional; omit for payload-format-only templates
  url: "${{ secrets.SLACK_WEBHOOK_URL }}"
  method: POST                          # GET|POST|PUT|PATCH|DELETE; default POST
auth:                                   # optional
  type: bearer                          # bearer | basic | header
  token: "${{ secrets.BRIDGE_TOKEN }}"
headers:
  Content-Type: application/json
body:
  channel: "${{ context.channel }}"
  text: "${{ response.content }}"
content_transform:
  format: text                          # text | markdown | html
  max_length: 4096
  truncation_suffix: "..."
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `name` | ✅ Yes | string | — | Transformer id; must match the filename stem |
| `endpoint.url` | ❌ No | string | None | Delivery URL; supports `${{ secrets.* }}` |
| `endpoint.method` | ❌ No | string | "POST" | `GET`/`POST`/`PUT`/`PATCH`/`DELETE` |
| `auth.type` | ❌ No | string | None | `bearer` (`token`), `basic` (`username`/`password`), `header` (`header_name`/`header_value`) |
| `headers` | ❌ No | map | None | Custom HTTP headers |
| `body` | ❌ No | map/list/string | None | Request-body template with `${{ ... }}` placeholders |
| `content_transform.format` | ❌ No | string | None | `text` (strip markdown), `markdown` (passthrough), `html` (render) |
| `content_transform.max_length` | ❌ No | integer | None | Truncate content to this length |
| `content_transform.truncation_suffix` | ❌ No | string | "..." | Suffix appended when truncating |
| `version` | ❌ No | string | None | Version annotation (semantic only) |

Template variables: `response.content`, `response.files`, `response.metadata`, `request.message`, `request.user_id`, `request.files`, `context.*` (from the trigger's `parse.context`), `agent.name`, `secrets.*`, `timestamp` (ISO 8601 UTC). A value that is exactly one placeholder resolves natively (lists/objects stay unquoted); otherwise placeholders substitute as strings, and absent optional values are dropped from the rendered payload.

Template: `schemas/transformers/slack-bridge.afs`.

---

## 🔄 Override Hierarchy

### LLM Configuration Precedence (Highest to Lowest)
1. **Agent-specific model overrides** (`agents/*.afs` → `llm_models:`)
2. **Overlord LLM configuration** (`formation.afs` → `overlord.llm.{base,synthesis}`)
3. **Formation default LLM settings** (`formation.afs` → `llm.models[text]`)

### Model Selection Hierarchy (model references)

Beyond the capability-level precedence above, a `model:` reference — an `llm.aliases` name or a fully qualified `provider/model` string — is accepted at several authoring surfaces, and **the most specific level wins** (the author closest to the work picks the model):

| Level (most specific first) | Surface |
|-----------------------------|---------|
| SOP step directive | `[model:x]` in the step text |
| SOP frontmatter | `model:` |
| Trigger frontmatter | `model:` |
| Skill frontmatter | `model:` in `SKILL.md` |
| Agent | `llm_models:` capability overrides |
| Formation | `llm.models` |

Every `model:` reference is validated at formation load: it must resolve to a defined alias or be of `provider/model` form.

### Overlord LLM stages: `base` and `synthesis`

The overlord runs two distinct LLM stages:

* **`base`** — routing / task management / delegation. Picks which
  agent handles a request, decomposes complex requests into
  workflows, extracts media for routing context.
* **`synthesis`** — final user-visible reply produced from completed
  task results. This is the last LLM call in a workflow turn and
  the one whose latency the user feels most directly.

Both are configured under `overlord.llm` with identical option
shapes:

```yaml
overlord:
  llm:
    max_extraction_tokens: 500          # routing-pipeline knob (parent-level)

    base:
      model: "llama_cpp/phi-3-mini-4k-instruct"
      api_key: "${{ secrets.OVERLORD_LLM_API_KEY }}"
      settings:
        temperature: 0.2
        max_tokens: 2000
        timeout_seconds: 45
        max_retries: 1
        fallback_model: "openai/gpt-4o-mini"

    synthesis:                          # OPTIONAL — defaults to `base` when omitted
      model: "anthropic/claude-haiku-4-5"
      settings:
        temperature: 0.7
        max_tokens: 4096
        timeout_seconds: 30
        max_retries: 2
        fallback_model: "openai/gpt-4o-mini"
```

### Resolution lattice

```
overlord.llm.synthesis   →   overlord.llm.base   →   llm.models[text]
```

* If `overlord.llm.synthesis` is **set**, the overlord uses it for the
  workflow synthesis stage.
* If `overlord.llm.synthesis` is **omitted**, the overlord uses
  `overlord.llm.base` for synthesis as well.
* If `overlord.llm.base` is **also omitted**, the overlord uses the
  formation-level `llm.models[text]` for both stages.

This means a minimal formation can ship without any `overlord.llm`
block and still work — you only configure what you want to
override.

### BREAKING: flat `overlord.llm` shape removed

Earlier formations placed `model:`, `api_key:`, and `settings:` as
direct children of `overlord.llm:`. That flat shape is no longer
accepted. Move those fields into a nested `base:` block:

```yaml
# ❌ Old (flat) — no longer accepted
overlord:
  llm:
    model: "..."
    api_key: "..."
    max_extraction_tokens: 500
    settings: { ... }

# ✅ New (nested)
overlord:
  llm:
    max_extraction_tokens: 500           # peer of base/synthesis
    base:
      model: "..."
      api_key: "..."
      settings: { ... }
    synthesis: { ... }                   # optional
```

There is no compatibility shim — formations that have not migrated
will fail validation with an error pointing at the old field
location.

### Example Override Flow
```yaml
# formation.afs - Base defaults
llm:
  settings:
    temperature: 0.7        # Base default
    max_tokens: 4096
  models:
    - text: "openai/gpt-4o"

overlord:
  llm:
    base:
      settings:
        temperature: 0.2    # Overrides 0.7 for routing
        max_tokens: 2000    # Overrides 4096 for routing
    synthesis:
      model: "anthropic/claude-haiku-4-5"   # Faster model for the user-visible reply
      settings:
        temperature: 0.5    # Overrides 0.7 for synthesis only

# agents/my_agent.afs - Agent overrides
llm_models:
  - text: "anthropic/claude-3-opus"
    settings:
      temperature: 0.1      # Overrides 0.7 for this agent
      max_tokens: 1500      # Overrides 4096 for this agent
```

### MCP Server Access Rules
- **Formation-level MCP servers**: Available to ALL agents
- **Agent-level MCP servers**: ONLY available to that specific agent
- **Agent auth overrides**: Agent can override MCP server authentication

### API Key Resolution Order
1. **Component-specific key** (agent models, MCP auth, A2A auth)
2. **Formation api_keys section** (by provider)
3. **Environment variables** (fallback)

## 📝 Secrets and User Credentials Interpolation

### Secrets Syntax
```yaml
key: "${{ secrets.SECRET_NAME }}"
```

### User Credentials Syntax
```yaml
key: "${{ user.credentials.SERVICE_NAME }}"
```

### Examples
```yaml
# Formation-wide secrets (loaded at initialization)
llm:
  api_keys:
    openai: "${{ secrets.OPENAI_API_KEY }}"

auth:
  admin_key: "${{ secrets.FORMATION_ADMIN_API_KEY }}"

# User-specific credentials (loaded on-demand)
mcp_server:
  auth:
    # Formation secret for default access
    token: "${{ secrets.DEFAULT_GITHUB_TOKEN }}"

    # OR user-specific credential for personalized access
    token: "${{ user.credentials.github }}"

# Common use cases
agents:
  - id: "assistant"
    mcp_servers:
      - github              # Reference formation-level MCP by ID
      - gmail               # Reference formation-level MCP by ID
```

> [!NOTE]
> **Secrets vs User Credentials**:
> - **Secrets** are formation-wide and loaded at initialization
> - **User credentials** are per-user, loaded on-demand, and isolated between users
>
> How secrets and credentials are stored and managed is implementation-defined. See your runtime documentation for details.


## ✅ Validation Requirements

### Formation Validation
- ✅ Must have `schema`, `id`, `description`
- ✅ LLM models must specify valid capabilities
- ✅ All secret references must be valid
- ✅ Component IDs must be unique
- ✅ `server.auth` is no longer a valid key — a formation carrying it fails the load with a migration error
- ✅ `rbac.active` (if present) must be `auto`, `true`, or `false`
- ✅ `rbac.active: true` requires a `groups/` directory containing group files (empty `groups/` is a warning)
- ✅ `rbac.fallback` (if a group name) must name an existing group file in `groups/`
- ✅ RBAC active + `rbac.fallback: false` + no `middleware` block fails the load (dead config: every request would be rejected)
- ✅ `middleware` must declare exactly one transport: `url` (+ optional `headers`) or `command` (+ optional `args`); `timeout` must be a duration string
- ✅ At load, the declared middleware must be reachable and expose exactly one tool named `middleware` whose declared schema matches the contract; an input schema declaring `groups` fails the load
- ✅ `llm.aliases` keys must match `[a-zA-Z0-9_-]+`, values must be `provider/model`, and keys must not collide with capability names
- ✅ All `model:` references (SOP/trigger/skill frontmatter, `[model:x]` directives) must resolve to an alias or be `provider/model` form
- ✅ `proactive.heartbeat.enabled: true` requires `scheduler.enabled: true`
- ✅ Each `proactive.channels` entry must resolve to a transformer with a URL from the channel `url:` or the transformer's `endpoint.url`
- ✅ A trigger referencing a transformer must have a delivery URL from the trigger's `webhook:` or the transformer's `endpoint.url`
- ✅ `commands.builtin` keys must name known built-in commands
- ✅ `artifacts.storage.type` must be `local` (v1); `artifacts.retention.policy` must be `last_accessed` or `last_updated`

### Agent Validation
- ✅ Must have `schema`, `id`, `name`, `description`
- ✅ Model overrides must use valid capabilities
- ✅ MCP server references must exist
- ✅ Knowledge paths must be valid
- ✅ Must not declare a `soul` field (soul is overlord-only; agent character lives in `system_message`)

### MCP Validation
- ✅ Must have `schema`, `id`, `type`
- ✅ Command servers must have `command`
- ✅ HTTP servers must have `endpoint`
- ✅ Auth configurations must be complete
- ✅ `parameters` (if present) must be a flat key-value map
- ✅ `tools` (if present) must declare `allow` and/or `deny` (`whitelist`/`blacklist` accepted as aliases), each a non-empty string pattern or list of strings; a canonical key together with its own alias in one block is an error, as is any unknown key

### MCP Default Parameters

MCP servers support an optional `parameters` field: a flat key-value map injected into every tool call on that server. This removes infrastructure constants (org drive IDs, tenant IDs, project keys) from agent prompts and LLM inference, making tool execution deterministic.

```yaml
# mcp/ms365-mcp.afs
schema: "1.0.0"
id: ms365-mcp
type: http
endpoint: "https://mcp.example.com/ms365"
parameters:
  driveId: "${{ secrets.ORG_DRIVE_ID }}"
```

Rules:
- Values support secret interpolation (`${{ secrets.X }}`)
- Caller-provided values always take precedence over defaults
- Parameters are injected at execution time, not during planning

### MCP Tool Filtering

MCP servers support an optional `tools` block that scopes the upstream tool catalog at registration time. Useful when:

- The upstream server exposes many more tools than agents in this formation actually need (cuts the per-turn planning prompt that lists every tool's JSON schema).
- Destructive verbs (`delete_*`, `force_push_*`, `merge_*`) should be kept out of the LLM's plannable surface entirely.
- A multi-product MCP server should be exposed as if it were a single-surface server.

```yaml
# mcp/github-mcp.afs
schema: "1.0.0"
id: github-mcp
type: http
endpoint: "https://api.githubcopilot.com/mcp/"
auth:
  type: bearer
  token: "${{ secrets.GITHUB_PAT }}"

tools:
  allow:
    - "search_*"           # fnmatch globs (* ? [...])
    - "get_*"
    - "issue_*"
    - "add_issue_comment"  # literal names match exactly
    - "create_or_update_file"
```

Or allow everything except destructive ops:

```yaml
tools:
  deny:
    - "delete_*"
    - "force_push_branch"
    - "merge_pull_request"
```

Or both together — allow a surface, then subtract from it (deny applies after allow):

```yaml
tools:
  allow: ["issue_*", "get_*"]
  deny: ["issue_delete"]
```

Pattern semantics (POSIX `fnmatch`):

| Token       | Matches                                              |
|-------------|------------------------------------------------------|
| `*`         | any run of characters (including empty)              |
| `?`         | exactly one character                                |
| `[abc]`     | one character from a set                             |
| `[!abc]`    | one character NOT in the set                         |
| no metachar | literal name match (exact, case-sensitive)           |

Rules:
- `allow` and/or `deny` per server: `allow` alone keeps only matching tools, `deny` alone keeps everything except matching tools, both together apply allow first and then subtract deny (deny wins on overlap).
- `whitelist`/`blacklist` are accepted as aliases of `allow`/`deny`. Declaring a canonical key together with its own alias in one block (`allow` + `whitelist`, or `deny` + `blacklist`) is a load-time error; any other key in the block is a load-time error too.
- A single string pattern is accepted in place of a list (`deny: "*"`).
- Patterns are case-sensitive and match against the upstream MCP tool's `name` field.
- An empty list (`allow: []`) is a load-time warning — no filter is applied.
- A pattern that matches **zero** upstream tools surfaces a warning with `difflib`-style "did you mean?" suggestions for literal patterns.
- A post-filter set that contains **zero** tools is a clean skip: the server is **not** registered, agents that reference it get no tools from this source, and a warning is emitted. This is by design — operators may legitimately disable a server via filter — but no agent receives tools from a server whose filter excluded everything.
- The filter runs at registration time, between `tools/list` discovery and registry insertion. It does not affect tool execution; tools that pass the filter behave identically to an unfiltered registration.
- The same block (same keys, same semantics) appears on agent `mcp_servers` attachments — inline definitions and `{id, tools}` references alike — where it chains after the registry-level filter. See "The Tool Override Cascade".

### A2A Validation
- ✅ Must have `schema`, `id`, `url`
- ✅ Auth configurations must be complete
- ✅ URLs must be valid
- ✅ Outbound (service) `auth.type` must be `api_key`, `bearer`, `basic`, `custom`, `hmac`, `oauth2`, or `none` — `openid` is inbound-only
- ✅ Inbound `auth.type` must be `api_key`, `bearer`, `basic`, `custom`, `hmac`, `openid`, or `none` — `oauth2` is outbound-only
- ✅ Per-type required fields: `api_key` needs `key`; `bearer` needs `token`; `basic` needs `username` + `password`; `custom` needs a `headers` map; `hmac` needs `secret`; `oauth2` needs `client_id` + `client_secret` + `token_url`; `openid` needs `issuer` (http(s) URL)
- ✅ `hmac` optional fields: outbound `signature_header`/`timestamp_header` must be strings; inbound `timestamp_tolerance` must be a positive integer
- ✅ `openid` optional fields: `audience`/`jwks_url` must be strings, `allowed_algorithms` a list of strings, `clock_skew_seconds` a non-negative integer
- ✅ `oauth2` optional `scope` must be a string

### SOP Validation
- ✅ Frontmatter must declare `type: sop` (other markdown files in `sops/` are treated as resources)
- ✅ `mode` (if present) must be `template` or `guide`
- ✅ `model` (if present) must resolve to an alias or be `provider/model` form

### Trigger Validation
- ✅ Trigger id (filename stem) must match `^[a-zA-Z0-9_-]+$`
- ✅ Frontmatter keys limited to `name`, `type`, `webhook`, `transformer`, `parse`, `model`, `channel` (unknown keys fail load)
- ✅ `webhook` must be a non-empty http(s) URL
- ✅ `transformer` and `channel` must match `^[a-zA-Z0-9_-]+$`
- ✅ `parse` keys limited to `message`, `user_id`, `context`, `files`
- ✅ A referenced transformer must yield a delivery URL (trigger `webhook:` or transformer `endpoint.url`)

### Transformer Validation
- ✅ `name` is required and must match the filename stem
- ✅ `endpoint.method` (if present) must be `GET`, `POST`, `PUT`, `PATCH`, or `DELETE`
- ✅ `auth.type` (if present) must be `bearer`, `basic`, or `header`, with its required fields present
- ✅ `content_transform.format` (if present) must be `text`, `markdown`, or `html`

### Coding Delegation Validation
All of these fail formation load — never a delegation-time surprise:
- ✅ Keys limited to `client`, `command`, `args`, `output`, `parse`, `model`, `workdirs`, `cleanup`, `groups`, `extra_args`, `env`, `timeout`, `max_concurrent`
- ✅ Exactly one adapter source: `client` (matching `[a-zA-Z0-9_-]+`, resolving to a bundled template or formation-local `coding/<name>.yaml`) OR the inline adapter form — both or neither fails
- ✅ Adapter keys limited to `name`, `command`, `args`, `output`, `parse`, `forbidden_extra_args`; `args` keys to `base`, `prompt`, `session`, `session_new`, `session_resume`, `model`; `parse` keys to `result`, `session_id`
- ✅ A template file's `name` must match its filename stem
- ✅ `args.prompt` is required (fragment containing `{prompt}`, or the literal string `stdin`); fragments are non-empty string lists containing their placeholder (`{prompt}`/`{id}`/`{model}`)
- ✅ Session shapes are exclusive: `session` together with `session_new`/`session_resume` fails; `session_new` without `session_resume` fails (dead config)
- ✅ A captured-id adapter (`session_resume` only) must define `parse.session_id` and must not use `output: text`
- ✅ `output` must be `stream-json`, `json`, or `text`; `parse:` selectors together with `output: text` fail (dead config)
- ✅ `${{ secrets.* }}` resolves under `coding.env` ONLY — a reference anywhere else in the block (`extra_args` especially) or in an adapter definition fails with an error pointing at `env:`
- ✅ `workdirs` is required and non-empty; every root must exist and be a directory at load (symlink-resolved)
- ✅ `cleanup` must be `delete` or `keep`; `timeout` must parse as a positive duration; `max_concurrent` must be an integer ≥ 1
- ✅ `coding.model` requires the adapter to define an `args.model` fragment
- ✅ `extra_args` must not contain any adapter `forbidden_extra_args` flag (the runtime owns the subprocess cwd)
- ✅ The adapter binary must be present (bare `command` on PATH; absolute `command` an executable file) — presence only; install/auth is the developer's business
- ✅ When RBAC is active, every `coding.groups` entry must name an existing group in `groups/`

### Watch Validation
All of these fail formation load — never a watch-time surprise:
- ✅ `mcp.watch` must be a mapping, `true`, or `false`
- ✅ Keys limited to `interval`, `timeout`, `max_concurrent`, `max_consecutive_failures` (closed set)
- ✅ `interval` and `timeout` must be positive numbers (seconds); `max_concurrent` and `max_consecutive_failures` must be integers ≥ 1
- ✅ A boolean is rejected wherever a number is expected
- ✅ A `watch:` block in a formation with no declared `mcp.servers` is dead config and fails load
- ✅ In group files: `mcp` supports only the `watch` key, and `watch` supports only `max_concurrent` (integer ≥ 1)

### Links Validation
- ✅ `links` must be a mapping of `name -> {label, url, hint}`
- ✅ Every entry must be a mapping with a `url` field
- ✅ `url` must be an `http://` or `https://` URL
- ✅ `label` and `hint` (if present) must be strings

### Memory Ingestion Validation
All of these fail formation load with the full config path in the message:
- ✅ `memory.ingestion` and each sub-block must be mappings
- ✅ Booleans are rejected wherever numbers are expected; thresholds and margins must be in 0-1; counts and intervals must be positive
- ✅ `entity_resolution.flag_threshold` must not exceed `auto_merge_threshold`
- ✅ `sources.<name>.tier` must be exactly 1, 2, or 3
- ✅ `entity_types` must be a non-empty list of non-empty strings

### Replanning Validation
- ✅ `overlord.workflow.replanning` rejects unknown keys
- ✅ `max_attempts` must be an integer 1-10; `plan_similarity_threshold` in 0-1; `replan_timeout_seconds` ≥ 1
- ✅ `non_replannable_error_patterns` entries must be non-empty strings

### Knowledge Source Validation
All of these fail formation load — never a sync-time surprise:
- ✅ Every source needs exactly one of `path` (local) or `url` (remote), plus a non-empty `description`
- ✅ Local `path` must be relative to the formation root; absolute paths and `..` traversal are rejected
- ✅ Remote scheme must be one of: `http`, `https`, `s3`, `gs`, `az`, `rsync`, `rsync+ssh`, `ftp`, `sftp`, `file`
- ✅ Scheme structure: host/bucket/container required where applicable; `file://` must be an absolute local path; glob patterns rejected for `http(s)` and `rsync` schemes
- ✅ `auth.type` must be valid for the scheme (see the auth table) with its required fields non-empty; `az://` sources require an `auth` block
- ✅ `extract` options require `extract: true`; `extract` is invalid for `rsync` schemes and glob URLs
- ✅ `schedule` must be a valid cron expression or one of `@startup`/`@hourly`/`@daily`/`@weekly`
- ✅ `retry` keys are a closed set (`max_attempts`, `initial_delay`, `max_delay`, `exponential_base`) with typed bounds
- ✅ Source `id`s must be unique within the list
- ✅ `retrieval` must be one of `vector`/`tree`/`tree-vector`/`hybrid`; `agent_tree` requires a tree-capable mode and supports only `regenerate` (`manual`/`on-source-change`/`on-formation-load`)
- ✅ `knowledge.tree` keys are a closed set; `reasoning_threshold` must be a non-negative integer

### Group Validation
- ✅ Top-level keys limited to `name`, `description`, `inherits`, `agents`, `mcp_servers`, `triggers`, `sops`, `native_apps`, `memory`, `mcp`
- ✅ `inherits` references must exist; inheritance cycles fail load
- ✅ Section values must be a list, the wildcard string `"*"`, or a `{allow, deny}` mapping
- ✅ `mcp_servers.<id>` supports only the `tools` sub-key; `tools` blocks use `allow`/`deny` (both permitted)
- ✅ `memory` supports only the `write` sub-key
- ✅ `mcp` supports only `watch.max_concurrent` (the watch quota override — see [Watch Validation](#watch-validation))
- ✅ A group file grants nothing by itself — it takes effect only when the request middleware attaches its id to a request (or `rbac.fallback` names it)

## 🎯 Best Practices

### Schema Compliance
- Always include `schema: "1.0.0"` in every config file
- Use semantic versioning for component versions
- Validate configurations before deployment

### Secret Management
- Use descriptive secret names: `OPENAI_API_KEY` not `KEY1`
- Group related secrets by provider/service
- Never commit actual secret values

### Component Organization
- Use descriptive IDs: `weather-assistant` not `agent1`
- Group related components in subdirectories
- Keep configurations focused and minimal
- Declare all **architecture** components (agents, MCP servers, A2A services, skills) explicitly in the formation file
- Files in `agents/`, `mcp/`, `a2a/` are definitions; the formation file is the manifest
- **Content/policy** components (SOPs, triggers, groups, transformers) are auto-discovered from their directories — no manifest entry (see `specs/formation.md` §3)

### Override Strategy
- Use formation defaults for common settings
- Override only what's necessary at agent level
- Document override rationale in comments

## 🔍 Common Validation Errors

### Missing Required Fields
```yaml
# ❌ Invalid - missing schema
id: "my-agent"
name: "My Agent"

# ✅ Valid
schema: "1.0.0"
id: "my-agent"
name: "My Agent"
description: "My agent description"
```

### Invalid Secret References
```yaml
# ❌ Invalid - incorrect syntax
api_key: "{{ secrets.API_KEY }}"

# ✅ Valid
api_key: "${{ secrets.API_KEY }}"
```

### Capability Mismatches
```yaml
# ❌ Invalid - unknown capability
models:
  - unknown_capability: "openai/gpt-4o"

# ✅ Valid
models:
  - text: "openai/gpt-4o"
  - vision: "openai/gpt-4o"
```

> **Note**: To configure a separate model for response synthesis, use
> `overlord.llm.synthesis` (see "Overlord LLM stages: `base` and
> `synthesis`" above). Synthesis is an overlord-stage concern, not a
> capability of the formation-level `llm.models` list.

---

This schema guide ensures proper configuration structure and validation compliance for all Agent Formation components.
