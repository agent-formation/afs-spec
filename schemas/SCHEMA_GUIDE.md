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
- [📚 Table of Contents](#-table-of-contents)
- [🏗️ Schema Version](#️-schema-version)
- [📁 Formation Schema (`formation.afs`)](#-formation-schema-formationafs)
- [Basic Formation Information](#basic-formation-information)
- [Server Configuration](#server-configuration)
- [Access Control (`server.auth` + `groups/`)](#access-control-serverauth--groups)
  - [Group Definition Format](#group-definition-format)
  - [Permission Resolution Rules](#permission-resolution-rules)
  - [The Tool Override Cascade](#the-tool-override-cascade)
- [Input Limits Configuration](#input-limits-configuration)
- [LLM Configuration](#llm-configuration)
  - [LLM Global Settings](#llm-global-settings)
  - [LLM API Keys](#llm-api-keys)
  - [LLM Model Aliases](#llm-model-aliases)
  - [LLM Model Capabilities](#llm-model-capabilities)
  - [Vision Model Settings](#vision-model-settings)
  - [Audio Model Settings](#audio-model-settings)
  - [Video Model Settings](#video-model-settings)
  - [Documents Model Settings](#documents-model-settings)
- [Overlord Configuration](#overlord-configuration)
  - [Overlord Soul Configuration](#overlord-soul-configuration)
  - [Overlord LLM Configuration](#overlord-llm-configuration)
  - [Overlord Behavior Configuration](#overlord-behavior-configuration)
  - [Overlord Clarification Configuration](#overlord-clarification-configuration)
- [Async Configuration](#async-configuration)
- [Memory Configuration](#memory-configuration)
  - [Working Memory Configuration](#working-memory-configuration)
  - [Buffer Memory Configuration](#buffer-memory-configuration)
  - [Persistent Memory Configuration](#persistent-memory-configuration)
- [Logging Configuration](#logging-configuration)
- [Scheduler Configuration](#scheduler-configuration)
- [Proactive Configuration](#proactive-configuration)
- [Commands Configuration](#commands-configuration)
- [Artifacts Configuration](#artifacts-configuration)
- [A2A Configuration](#a2a-configuration)
  - [A2A General Configuration](#a2a-general-configuration)
  - [A2A Outbound Configuration](#a2a-outbound-configuration)
  - [A2A Inbound Configuration](#a2a-inbound-configuration)
- [MCP Configuration](#mcp-configuration)
- [User Credentials Configuration](#user-credentials-configuration)
- [Skills Configuration](#skills-configuration)
- [Agent Configuration](#agent-configuration)
- [Component Declaration](#component-declaration)
- [👤 Agent Schema (`agents/*.afs`)](#-agent-schema-agentsafs)
- [Basic Agent Information](#basic-agent-information)
- [System Behavior Configuration](#system-behavior-configuration)
- [Agent-to-Agent Communication](#agent-to-agent-communication)
- [Model Configuration Overrides](#model-configuration-overrides)
- [Role and Specialization](#role-and-specialization)
- [Domain Knowledge Configuration](#domain-knowledge-configuration)
- [Agent-Specific Skills](#agent-specific-skills)
- [Agent-Specific MCP Server Access](#agent-specific-mcp-server-access)
- [🔧 MCP Server Schema (`mcp/*.afs`)](#-mcp-server-schema-mcpafs)
- [Basic MCP Server Information](#basic-mcp-server-information)
- [Command-Based MCP Server Configuration](#command-based-mcp-server-configuration)
- [HTTP-Based MCP Server Configuration](#http-based-mcp-server-configuration)
- [Authentication Configuration](#authentication-configuration-1)
- [MCP Default Parameters](#mcp-default-parameters)
- [MCP Tool Filtering](#mcp-tool-filtering)
- [🌐 A2A Service Schema (`a2a/*.afs`)](#-a2a-service-schema-a2aafs)
- [Basic A2A Service Information](#basic-a2a-service-information)
- [Rate Limiting Configuration](#rate-limiting-configuration)
- [Authentication Configuration](#authentication-configuration-2)
- [📋 SOP Schema (`sops/*.md`)](#-sop-schema-sopsmd)
- [⚡ Trigger Schema (`triggers/*.md`)](#-trigger-schema-triggersmd)
- [📤 Transformer Schema (`transformers/*.afs`)](#-transformer-schema-transformersafs)
- [🔄 Override Hierarchy](#-override-hierarchy)
- [LLM Configuration Precedence (Highest to Lowest)](#llm-configuration-precedence-highest-to-lowest)
- [Model Selection Hierarchy (model references)](#model-selection-hierarchy-model-references)
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
- [A2A Validation](#a2a-validation)
- [SOP Validation](#sop-validation)
- [Trigger Validation](#trigger-validation)
- [Transformer Validation](#transformer-validation)
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
  auth: "open"      # Default: open - Access control mode ("open" | "required")

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
| `server.auth` | ❌ No | string | "open" | Access control mode: `open` or `required` (see Access Control) |
| `server.api_keys.admin_key` | ❌ No | string | Auto-generated | API key for formation management operations |
| `server.api_keys.client_key` | ❌ No | string | Auto-generated | API key for user interactions |

> [!NOTE]
> API key header names and user identification headers are implementation-defined. See your runtime documentation for details.

### Access Control (`server.auth` + `groups/`)
*Group-based access control: who can reach the formation, and which resources each group can use*

```yaml
# formation.afs
server:
  auth: required  # or open (default)
```

| Value | Behavior |
|-------|----------|
| `open` | Any user can interact with the formation. A `groups/` directory containing group files is **not** permitted with `open` — the combination fails formation load. |
| `required` | Only users present in the runtime's user database can interact. Unknown users are rejected across all channels. If `groups/` exists, resource filtering is applied; if not, authenticated users have full access. |

Group permission files live in a `groups/` directory and are **auto-discovered** (content/policy tier — no manifest entry, unlike agents/MCP/A2A/skills). A group file grants nothing until the runtime's user database maps a user to the group id, so discovery-on-presence is safe. An empty `groups/` directory is inert (warning only). How users and group memberships are populated is a runtime/operational concern outside this standard.

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

#### Permission Resolution Rules

1. **Deny takes precedence over allow.** If any of a user's groups denies a resource, it is denied.
2. **Union of allows** across all of a user's groups.
3. **Wildcards** — patterns are POSIX `fnmatch` globs (`*`, `?`, `[...]`) in both allow and deny lists.
4. **Inheritance** — parent permissions resolve first; list sections merge additively; a child's tool-override block **replaces** the parent's block for the same (agent, server) key; deny in the child overrides allow in the parent.
5. **No `groups/` directory** = no resource filtering for authenticated users.
6. **User in DB with no group memberships** — passes the auth gate but reaches no resources.

#### The Tool Override Cascade

Tool control is one concern appearing at four levels; the most specific level wins:

| Level | Keys | Role |
|-------|------|------|
| Formation `mcp.servers[].tools` | `whitelist` / `blacklist` (exactly one) | Hard catalog bound — pruned at registration; nothing below can resurrect a pruned tool |
| Agent-level MCP definition `tools` | `whitelist` / `blacklist` (exactly one) | The agent's default tool surface for an agent-private server |
| Group `mcp_servers.<id>.tools` | `allow` / `deny` (either or both) | Group-wide override for that server, across all granted agents |
| Group `agents.<agent>.<id>.tools` | `allow` / `deny` (either or both) | Most specific: this group, this agent, this server |

**Group override semantics:** if a group provides a `tools:` block, it **supersedes** the inherited block; otherwise the inherited config applies unchanged. Within a block: `allow` alone = exactly this set (expanded against the post-registry catalog, so a group override may supersede — not merely intersect — the agent's inherited view); `deny` alone = inherited minus these; both = allow-then-subtract. `tools: {deny: "*"}` hides a server from a group entirely. Cross-group merge: union of allows, any group's deny wins (deny is global, allow is per-group).

> [!NOTE]
> **Vocabulary split.** Registry- and agent-level blocks use `whitelist`/`blacklist` with a strict one-of-the-two rule; group-level blocks use `allow`/`deny` and permit both together (deny applies after allow). The keys are not interchangeable across levels.

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

### Agent Soul Documents
*Per-agent identity documents prepended to the system message*

```yaml
# agents/my-assistant.afs
soul: "./SOUL.md"    # relative path, resolved inside the formation directory
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `soul` | ❌ No | string | None | Relative path to a markdown soul document; content is prepended verbatim to the agent's system message |

Rules:
- The path must resolve **inside** the formation directory (same confinement as knowledge paths).
- A missing file is a **load-time error**, not a silent skip.
- No templating is applied to the content.
- Distinct from the overlord-level soul (`SOUL.md` next to the formation file, or `overlord.soul`), which defines the orchestrator persona.

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

Triggers are markdown files with YAML frontmatter under `triggers/`, **auto-discovered**. The id is the filename stem and must match `^[a-zA-Z0-9_-]+$`. Each trigger is exposed at `POST /v1/triggers/{id}` (client key + user auth gate); `GET /v1/triggers` lists, `GET /v1/triggers/{id}` returns metadata.

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
- ✅ `server.auth` (if present) must be `open` or `required`
- ✅ A `groups/` directory containing group files requires `server.auth: required` (open + groups fails load; empty `groups/` is a warning)
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
- ✅ `soul` (if present) must resolve to an existing file inside the formation directory

### MCP Validation
- ✅ Must have `schema`, `id`, `type`
- ✅ Command servers must have `command`
- ✅ HTTP servers must have `endpoint`
- ✅ Auth configurations must be complete
- ✅ `parameters` (if present) must be a flat key-value map
- ✅ `tools` (if present) must declare exactly one of `whitelist` or `blacklist`, each a non-empty list of strings

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
  whitelist:               # mutually exclusive with blacklist
    - "search_*"           # fnmatch globs (* ? [...])
    - "get_*"
    - "issue_*"
    - "add_issue_comment"  # literal names match exactly
    - "create_or_update_file"
```

Or, equivalently, allow everything except destructive ops:

```yaml
tools:
  blacklist:
    - "delete_*"
    - "force_push_branch"
    - "merge_pull_request"
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
- Exactly one of `whitelist` or `blacklist` per server (declaring both is a load-time error).
- Patterns are case-sensitive and match against the upstream MCP tool's `name` field.
- An empty list (`whitelist: []`) is a load-time warning — no filter is applied.
- A pattern that matches **zero** upstream tools surfaces a warning with `difflib`-style "did you mean?" suggestions for literal patterns.
- A post-filter set that contains **zero** tools is a clean skip: the server is **not** registered, agents that reference it get no tools from this source, and a warning is emitted. This is by design — operators may legitimately disable a server via filter — but no agent receives tools from a server whose filter excluded everything.
- The filter runs at registration time, between `tools/list` discovery and registry insertion. It does not affect tool execution; tools that pass the filter behave identically to an unfiltered registration.

### A2A Validation
- ✅ Must have `schema`, `id`, `url`
- ✅ Auth configurations must be complete
- ✅ URLs must be valid

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

### Group Validation
- ✅ Top-level keys limited to `name`, `description`, `inherits`, `agents`, `mcp_servers`, `triggers`, `sops`, `native_apps`, `memory`
- ✅ `inherits` references must exist; inheritance cycles fail load
- ✅ Section values must be a list, the wildcard string `"*"`, or a `{allow, deny}` mapping
- ✅ `mcp_servers.<id>` supports only the `tools` sub-key; `tools` blocks use `allow`/`deny` (both permitted)
- ✅ `memory` supports only the `write` sub-key
- ✅ Group files require `server.auth: required` in the formation

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
