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
- [Input Limits Configuration](#input-limits-configuration)
- [LLM Configuration](#llm-configuration)
  - [LLM Global Settings](#llm-global-settings)
  - [LLM API Keys](#llm-api-keys)
  - [LLM Model Capabilities](#llm-model-capabilities)
  - [Vision Model Settings](#vision-model-settings)
  - [Audio Model Settings](#audio-model-settings)
  - [Video Model Settings](#video-model-settings)
  - [Documents Model Settings](#documents-model-settings)
- [Overlord Configuration](#overlord-configuration)
  - [Overlord Persona Configuration](#overlord-persona-configuration)
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
- [A2A Configuration](#a2a-configuration)
  - [A2A General Configuration](#a2a-general-configuration)
  - [A2A Outbound Configuration](#a2a-outbound-configuration)
  - [A2A Inbound Configuration](#a2a-inbound-configuration)
- [MCP Configuration](#mcp-configuration)
- [User Credentials Configuration](#user-credentials-configuration)
- [Agent Configuration](#agent-configuration)
- [Component Auto-Discovery](#component-auto-discovery)
- [👤 Agent Schema (`agents/*.afs`)](#-agent-schema-agentsafs)
- [Basic Agent Information](#basic-agent-information)
- [System Behavior Configuration](#system-behavior-configuration)
- [Agent-to-Agent Communication](#agent-to-agent-communication)
- [Model Configuration Overrides](#model-configuration-overrides)
- [Role and Specialization](#role-and-specialization)
- [Domain Knowledge Configuration](#domain-knowledge-configuration)
- [Agent-Specific MCP Server Access](#agent-specific-mcp-server-access)
- [🔧 MCP Server Schema (`mcp/*.afs`)](#-mcp-server-schema-mcpafs)
- [Basic MCP Server Information](#basic-mcp-server-information)
- [Command-Based MCP Server Configuration](#command-based-mcp-server-configuration)
- [HTTP-Based MCP Server Configuration](#http-based-mcp-server-configuration)
- [Authentication Configuration](#authentication-configuration-1)
- [🌐 A2A Service Schema (`a2a/*.afs`)](#-a2a-service-schema-a2aafs)
- [Basic A2A Service Information](#basic-a2a-service-information)
- [Rate Limiting Configuration](#rate-limiting-configuration)
- [Authentication Configuration](#authentication-configuration-2)
- [🔄 Override Hierarchy](#-override-hierarchy)
- [LLM Configuration Precedence (Highest to Lowest)](#llm-configuration-precedence-highest-to-lowest)
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

*Note: The complete LLM Configuration, Overlord Configuration, Memory Configuration, Logging Configuration, A2A Configuration, MCP Configuration, and other sections follow the same patterns. See the full schema reference for complete documentation.*

---

## 🔄 Override Hierarchy

### LLM Configuration Precedence (Highest to Lowest)
1. **Agent-specific model overrides** (`agents/*.afs` → `llm_models:`)
2. **Overlord LLM configuration** (`formation.afs` → `overlord.llm`)
3. **Formation default LLM settings** (`formation.afs` → `llm:`)

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
  routing:
    settings:
      temperature: 0.2      # Overrides 0.7 for routing
      max_tokens: 2000      # Overrides 1000 for routing

# agents/my_agent.afs - Agent overrides
llm_models:
  - text: "anthropic/claude-3-opus"
    settings:
      temperature: 0.1      # Overrides 0.7 for this agent
      max_tokens: 1500      # Overrides 1000 for this agent
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
      - id: "github"
        auth:
          type: "bearer"
          token: "${{ user.credentials.github }}"  # User's personal GitHub token

      - id: "gmail"
        auth:
          type: "oauth"
          credentials: "${{ user.credentials.gmail }}"  # User's Gmail OAuth credentials
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

### Agent Validation
- ✅ Must have `schema`, `id`, `name`, `description`
- ✅ Model overrides must use valid capabilities
- ✅ MCP server references must exist
- ✅ Knowledge paths must be valid

### MCP Validation
- ✅ Must have `schema`, `id`, `type`
- ✅ Command servers must have `command`
- ✅ HTTP servers must have `endpoint`
- ✅ Auth configurations must be complete

### A2A Validation
- ✅ Must have `schema`, `id`, `url`
- ✅ Auth configurations must be complete
- ✅ URLs must be valid

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

---

This schema guide ensures proper configuration structure and validation compliance for all Agent Formation components.
