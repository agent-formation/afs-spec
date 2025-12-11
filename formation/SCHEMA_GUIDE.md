# MUXI Formation Schema Guide

## 📋 Overview

This guide documents the complete schema structure for MUXI formations, including all configuration files, override hierarchies, and validation requirements.

> [!TIP]
> **Secrets Management**: Throughout all configuration files, you can reference secrets using the `${{ secrets.NAME }}` syntax. Any secrets added to your formation's secrets store can be accessed this way, providing secure handling of API keys, passwords, and other sensitive configuration values.

> [!NOTE]
> When pushing agents, formations, or MCPs to the registry, your username is automatically prepended to the component id, forming a globally unique identifier like `username/agent-id`.

## 📚 Table of Contents

- [MUXI Formation Schema Guide](#muxi-formation-schema-guide)
  - [📋 Overview](#-overview)
  - [📚 Table of Contents](#-table-of-contents)
  - [🏗️ Schema Version](#️-schema-version)
  - [📁 Formation Schema (`formation.yaml`)](#-formation-schema-formationyaml)
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
    - [Runtime Configuration](#runtime-configuration)
    - [User Credentials Configuration](#user-credentials-configuration)
    - [Agent Configuration](#agent-configuration)
    - [Component Auto-Discovery](#component-auto-discovery)
  - [👤 Agent Schema (`agents/*.yaml`)](#-agent-schema-agentsyaml)
    - [Basic Agent Information](#basic-agent-information)
    - [System Behavior Configuration](#system-behavior-configuration)
    - [Agent-to-Agent Communication](#agent-to-agent-communication)
    - [Model Configuration Overrides](#model-configuration-overrides)
    - [Role and Specialization](#role-and-specialization)
    - [Domain Knowledge Configuration](#domain-knowledge-configuration)
    - [Agent-Specific MCP Server Access](#agent-specific-mcp-server-access)
  - [🔧 MCP Server Schema (`mcp/*.yaml`)](#-mcp-server-schema-mcpyaml)
    - [Basic MCP Server Information](#basic-mcp-server-information)
    - [Command-Based MCP Server Configuration](#command-based-mcp-server-configuration)
    - [HTTP-Based MCP Server Configuration](#http-based-mcp-server-configuration)
    - [Authentication Configuration](#authentication-configuration-1)
  - [🌐 A2A Service Schema (`a2a/*.yaml`)](#-a2a-service-schema-a2ayaml)
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

## 📁 Formation Schema (`formation.yaml`)

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
runtime: "1.2"  # Runtime version constraint (exact, minor, major, or omit for latest)
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
| `runtime` | ❌ No | string | "latest" | Runtime SIF version constraint (semantic versioning) |

**Runtime Version Constraints:**
- `runtime: "1.2.3"` - Exact version (uses muxi-runtime-1.2.3)
- `runtime: "1.2"` - Latest 1.2.x (e.g., resolves to 1.2.5)
- `runtime: "1"` - Latest 1.x.x (e.g., resolves to 1.9.3)
- `runtime: ""` or omitted - Absolute latest runtime version

> [!NOTE]
> When a formation is deployed, the server resolves the runtime constraint to an exact version (e.g., "1.2" → "1.2.5") and pins it. This ensures formations remain stable even when new runtime versions are released. To upgrade a formation's runtime, redeploy with an updated `runtime` field.

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
| `server.api_keys.admin_key` | ❌ No | string | Auto-generated | API key for formation management operations (start/stop, agent management) |
| `server.api_keys.client_key` | ❌ No | string | Auto-generated | API key for user interactions (chat, memories) with required `user_id` header |

> [!NOTE]
> 1. The `admin_key` should be passed as `X-Admin-Key` header for formation management endpoints
> 2. The `client_key` should be passed as `X-Client-Key` header for user interaction endpoints
> 3. User interaction endpoints also require `X-Muxi-User-Id` header for user identification
> 4. If API keys are not provided, they will be auto-generated and displayed on server startup

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

### LLM Configuration
*Language model settings, API keys, and capability-based model definitions*

> [!TIP]
> **Streaming Model**: The optional `streaming` capability allows you to define a fast, lightweight model specifically for real-time progress updates and user feedback during request processing. This model is used to generate conversational updates like "Analyzing your request...", "Searching for information...", etc. Use a faster, cheaper model (like gpt-4o-mini or claude-3.5-haiku) with minimal retries for optimal performance.

```yaml
llm:
  settings:
    temperature: 0.7
    max_tokens: 4096
    timeout_seconds: 30
    max_retries: 3
    fallback_model: "anthropic/claude-3.5-sonnet"

  api_keys:
    openai: "${{ secrets.OPENAI_API_KEY }}"
    anthropic: "${{ secrets.ANTHROPIC_API_KEY }}"

  models:
    - text: "openai/gpt-4o"
      api_key: "${{ secrets.CUSTOM_LLM_API_KEY }}"
      settings:
        temperature: 0.7
        max_tokens: 4096
        timeout_seconds: 30
        max_retries: 2
        fallback_model: "anthropic/claude-3.5-sonnet"
    - streaming: "openai/gpt-4o-mini"
      settings:
        temperature: 0.7
        max_tokens: 100
        timeout_seconds: 10
        max_retries: 0
        fallback_model: "anthropic/claude-3.5-haiku"
    - vision: "openai/gpt-4o"
      settings:
        temperature: 0.7
        max_tokens: 1500
        max_retries: 1
        fallback_model: "anthropic/claude-3.5-sonnet"
        image:
          max_size_mb: 5
          preprocessing:
            resize: true
            max_width: 1024
            max_height: 1024
    - audio: "openai/whisper-1"
      settings:
        max_size_mb: 10
        language: "auto"
    - documents: "openai/gpt-4o"
      settings:
        max_size_mb: 20
        extraction:
          chunk_size: 1000
          overlap: 100
          strategy: "adaptive"
          nlp:
            data_path: "~/nlp_data"
            # spacy_model: "en_core_web_sm"  # Uncomment to override
            # sentence_transformer: "all-MiniLM-L6-v2"  # Uncomment to override
        cache_ttl_seconds: 3600
    - embedding: "openai/text-embedding-3-large"
      settings:
        temperature: 0.7
        max_tokens: 4096
        timeout_seconds: 30
        max_retries: 5
        fallback_model: "cohere/embed-english-v3.0"
```

#### LLM Global Settings
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `llm.settings.temperature` | ❌ No | float | 0.7 | Default creativity level (0.0-1.0) for all models |
| `llm.settings.max_tokens` | ❌ No | integer | 4096 | Default maximum tokens for responses |
| `llm.settings.timeout_seconds` | ❌ No | integer | 30 | Default request timeout in seconds |
| `llm.settings.max_retries` | ❌ No | integer | 3 | Default number of retry attempts for the same model |
| `llm.settings.fallback_model` | ❌ No | string | None | Default fallback model if primary fails |

#### LLM Response Caching Settings
*Intelligent semantic caching powered by OneLLM for 70%+ cost savings and faster responses*

```yaml
llm:
  settings:
    caching:
      enabled: true                       # Enable/disable caching (default: true)
      max_entries: 10000                  # LRU eviction limit (default: 10000)
      p: 0.95                             # Similarity threshold (default: 0.95)
      hash_only: false                    # Disable semantic matching (default: false)
      stream_chunk_strategy: "sentences"  # Chunking: words|sentences|paragraphs|characters
      stream_chunk_length: 1              # Chunk size (default: 1)
      ttl: 86400                          # Time-to-live in seconds (default: 86400 = 1 day)
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `llm.settings.caching.enabled` | ❌ No | boolean | true | Enable/disable LLM response caching (enabled by default) |
| `llm.settings.caching.max_entries` | ❌ No | integer | 10000 | Maximum cache entries before LRU eviction |
| `llm.settings.caching.p` | ❌ No | float | 0.95 | Similarity threshold (0.0-1.0) for semantic matching |
| `llm.settings.caching.hash_only` | ❌ No | boolean | false | Disable semantic matching, use only hash-based exact matches |
| `llm.settings.caching.stream_chunk_strategy` | ❌ No | enum | "sentences" | Chunking strategy for streaming (words, sentences, paragraphs, characters) |
| `llm.settings.caching.stream_chunk_length` | ❌ No | integer | 1 | Number of strategy units per chunk |
| `llm.settings.caching.ttl` | ❌ No | integer | 86400 | Time-to-live in seconds for cache entries (default: 24 hours) |

> [!TIP]
> **Development vs Production**: Disable caching during development (`enabled: false`) to see immediate effects of prompt changes. Re-enable in production for significant cost savings.

> [!NOTE]
> **How It Works**: The caching system uses semantic similarity matching to reuse responses for similar (not just identical) requests. With default settings (p=0.95), requests that are 95% similar will return cached responses, providing 70%+ cost savings in typical conversational AI scenarios.

For complete caching documentation including performance impact, troubleshooting, and best practices, see your runtime's documentation.

#### LLM API Keys
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `llm.api_keys.openai` | ❌ No | string | None | OpenAI API key for GPT models |
| `llm.api_keys.anthropic` | ❌ No | string | None | Anthropic API key for Claude models |
| `llm.api_keys.other` | ❌ No | string | None | Other API key for other models |

#### LLM Model Capabilities
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `models[].text` | ❌ No | string | None | Model for text generation and conversation |
| `models[].streaming` | ❌ No | string | None | Fast model for real-time progress updates and user feedback |
| `models[].vision` | ❌ No | string | None | Model for image analysis and vision tasks |
| `models[].audio` | ❌ No | string | None | Model for audio transcription and processing |
| `models[].video` | ❌ No | string | None | Model for video analysis including visual and audio content |
| `models[].documents` | ❌ No | string | None | Model for document processing and extraction |
| `models[].embedding` | ❌ No | string | None | Model for generating text embeddings |
| `models[].api_key` | ❌ No | string | Provider default | Override API key for specific model |
| `models[].settings` | ❌ No | object | Global defaults | Model-specific configuration overrides |
| `models[].settings.temperature` | ❌ No | float | Global default | Override creativity level (0.0-1.0) for this model |
| `models[].settings.max_tokens` | ❌ No | integer | Global default | Override maximum tokens for this model |
| `models[].settings.timeout_seconds` | ❌ No | integer | Global default | Override request timeout for this model |
| `models[].settings.max_retries` | ❌ No | integer | Global default | Override number of retry attempts for this model |
| `models[].settings.fallback_model` | ❌ No | string | Global default | Override fallback model if this model fails |

#### Vision Model Settings
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `settings.temperature` | ❌ No | float | Global default | Override creativity level (0.0-1.0) for vision model |
| `settings.max_tokens` | ❌ No | integer | Global default | Override maximum tokens for vision model responses |
| `settings.timeout_seconds` | ❌ No | integer | Global default | Override request timeout for vision model |
| `settings.max_retries` | ❌ No | integer | Global default | Override number of retry attempts for vision model |
| `settings.fallback_model` | ❌ No | string | Global default | Override fallback model if vision model fails |
| `settings.image.max_size_mb` | ❌ No | integer | 5 | Maximum image file size in megabytes |
| `settings.image.preprocessing.resize` | ❌ No | boolean | true | Whether to resize large images |
| `settings.image.preprocessing.max_width` | ❌ No | integer | 1024 | Maximum width after resize |
| `settings.image.preprocessing.max_height` | ❌ No | integer | 1024 | Maximum height after resize |

#### Audio Model Settings
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `settings.temperature` | ❌ No | float | Global default | Override creativity level (0.0-1.0) for audio model |
| `settings.max_tokens` | ❌ No | integer | Global default | Override maximum tokens for audio model responses |
| `settings.timeout_seconds` | ❌ No | integer | Global default | Override request timeout for audio model |
| `settings.max_retries` | ❌ No | integer | Global default | Override number of retry attempts for audio model |
| `settings.fallback_model` | ❌ No | string | Global default | Override fallback model if audio model fails |
| `settings.max_size_mb` | ❌ No | integer | 10 | Maximum audio file size in megabytes |
| `settings.language` | ❌ No | string | "auto" | Language for transcription (auto-detect or specific) |

#### Video Model Settings
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `settings.temperature` | ❌ No | float | Global default | Override creativity level (0.0-1.0) for video model |
| `settings.max_tokens` | ❌ No | integer | Global default | Override maximum tokens for video model responses |
| `settings.timeout_seconds` | ❌ No | integer | Global default | Override request timeout for video model |
| `settings.max_retries` | ❌ No | integer | Global default | Override number of retry attempts for video model |
| `settings.fallback_model` | ❌ No | string | Global default | Override fallback model if video model fails |
| `settings.max_size_mb` | ❌ No | integer | 100 | Maximum video file size in megabytes |
| `settings.max_duration_seconds` | ❌ No | integer | 300 | Maximum video duration in seconds (5 minutes default) |
| `settings.include_audio_analysis` | ❌ No | boolean | true | Whether to analyze audio track if present |

#### Documents Model Settings
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `settings.temperature` | ❌ No | float | Global default | Override creativity level (0.0-1.0) for documents model |
| `settings.max_tokens` | ❌ No | integer | Global default | Override maximum tokens for documents model responses |
| `settings.timeout_seconds` | ❌ No | integer | Global default | Override request timeout for documents model |
| `settings.max_retries` | ❌ No | integer | Global default | Override number of retry attempts for documents model |
| `settings.fallback_model` | ❌ No | string | Global default | Override fallback model if documents model fails |
| `settings.max_size_mb` | ❌ No | integer | 20 | Maximum document file size in megabytes |
| `settings.extraction.chunk_size` | ❌ No | integer | 1000 | Text chunk size for document processing |
| `settings.extraction.overlap` | ❌ No | integer | 100 | Overlap between chunks for context preservation |
| `settings.extraction.strategy` | ❌ No | string | "adaptive" | Default extraction strategy (adaptive, semantic, fixed, paragraph) |
| `settings.extraction.nlp.data_path` | ❌ No | string | "~/nlp_data" | Path for NLP model data (NLTK, spaCy, etc.) |
| `settings.extraction.nlp.spacy_model` | ❌ No | string | "en_core_web_sm" | SpaCy model for advanced text processing (commented by default) |
| `settings.extraction.nlp.sentence_transformer` | ❌ No | string | "all-MiniLM-L6-v2" | Sentence transformer model for embeddings (commented by default) |
| `settings.cache_ttl_seconds` | ❌ No | integer | 3600 | Cache TTL for processed documents in seconds |

#### Streaming Model Settings
*Settings for real-time progress update rephrasing with internal monologue style*

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `settings.temperature` | ❌ No | float | 0.7 | Creativity level for rephrasing (0.0-1.0) |
| `settings.max_tokens` | ❌ No | integer | 50 | Maximum tokens for rephrased messages (kept short for real-time) |
| `settings.timeout_seconds` | ❌ No | integer | 2 | Timeout for rephrasing requests (fast response required) |
| `settings.enable_rephrasing` | ❌ No | boolean | Auto | Enable LLM rephrasing (auto: true if streaming model specified, false if using text fallback) |

> **💡 Tip:** The streaming model is used to rephrase progress updates into conversational internal monologue style. It automatically:
> - Detects and matches the user's language
> - Keeps messages concise (10-15 words)
> - Uses first-person internal thought style ("Let me check...", "I'll need to...")
> - Falls back to raw messages if rephrasing fails

Example configuration:
```yaml
llm:
  models:
    - text: "openai/gpt-4o"
    - streaming: "openai/gpt-4o-mini"  # Fast, cheap model for progress updates
      settings:
        temperature: 0.7
        max_tokens: 50
        enable_rephrasing: true  # Optional: explicitly control rephrasing
```

### Overlord Configuration
*Orchestrator behavior settings, intelligent routing configuration, and clarification capabilities*

```yaml
overlord:
  persona: |
    You are Fynn, a helpful assistant for Company XYZ.
    You are friendly, helpful, and professional.

  llm:
    model: "llama_cpp/phi-3-mini-4k-instruct"
    api_key: "${{ secrets.OVERLORD_LLM_API_KEY }}"
    max_extraction_tokens: 500       # Max tokens for media extractions when needed for routing
    settings:
      temperature: 0.2
      max_tokens: 2000
      timeout_seconds: 45
      max_retries: 1
      fallback_model: "openai/gpt-4o-mini"

  caching:
    enabled: true                    # Whether to cache routing decisions
    ttl: 3600                        # Time to live for cached routing decisions

  response:
    format: "markdown"               # Default response format (markdown, text, html, json)
    widgets: true                    # Enable interactive UI elements
    streaming: true                  # Enable streaming for synchronous responses

  workflow:
    auto_decomposition: true         # Enable automatic task decomposition
    plan_approval_threshold: 7       # Complexity threshold for plan approval
    # Additional workflow configuration...

  # Clarification configuration (always enabled for better UX)
  clarification:
    style: "conversational"          # Question style: conversational, formal, brief
    max_rounds:                      # Safety limits - maximum clarifying questions per request
      direct: 3                      # Quick disambiguation
      brainstorm: 10                 # Creative exploration
      planning: 7                    # Requirements gathering
      execution: 3                   # Parameter clarification
      other: 3                       # Fallback for any unlisted modes
```

#### Overlord Persona Configuration
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `overlord.persona` | ❌ No | string | Loaded from utils/system_persona.md | Custom persona text that defines the overlord's identity and communication style. MUXI automatically prepends technical orchestration instructions to this persona. |

#### Overlord LLM Configuration
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `overlord.llm.model` | ❌ No | string | Formation default | Model for intelligent routing and task delegation |
| `overlord.llm.api_key` | ❌ No | string | Provider default | Override API key for routing model |
| `overlord.llm.settings.temperature` | ❌ No | float | 0.2 | Lower temperature for consistent routing behavior |
| `overlord.llm.settings.max_tokens` | ❌ No | integer | 2000 | Maximum tokens for routing decisions |
| `overlord.llm.settings.timeout_seconds` | ❌ No | integer | 45 | Timeout for routing model requests |
| `overlord.llm.settings.max_retries` | ❌ No | integer | 1 | Number of retry attempts for routing model |
| `overlord.llm.settings.fallback_model` | ❌ No | string | None | Fallback model if routing model fails |
| `overlord.llm.max_extraction_tokens` | ❌ No | integer | 500 | Maximum tokens for media content extraction when needed for routing |

#### Overlord Caching Configuration
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `overlord.caching.enabled` | ❌ No | boolean | true | Whether to cache routing decisions for performance |
| `overlord.caching.ttl` | ❌ No | integer | 3600 | Time to live for cached routing decisions in seconds |

#### Overlord Response Configuration
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `overlord.response.format` | ❌ No | enum | "markdown" | Default response format (markdown, text, html, json) |
| `overlord.response.widgets` | ❌ No | boolean | true | Enable interactive UI elements like buttons, forms, charts |
| `overlord.response.streaming` | ❌ No | boolean | false | Enable streaming responses for synchronous chat interactions |
| `overlord.response.progress` | ❌ No | boolean | true | Enable progress events during streaming (when false, only streams final response) |

#### Overlord Workflow Configuration
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `overlord.workflow.auto_decomposition` | ❌ No | boolean | true | Enable automatic task decomposition for complex requests |
| `overlord.workflow.plan_approval_threshold` | ❌ No | integer | 7 | Complexity threshold (1-10) for requiring plan approval |
| `overlord.workflow.complexity_method` | ❌ No | enum | "llm" | Method for complexity calculation (heuristic, llm, custom, hybrid) |
| `overlord.workflow.complexity_threshold` | ❌ No | float | 7.0 | Complexity threshold for triggering workflows (1-10) |
| `overlord.workflow.complexity_weights` | ❌ No | object | {heuristic: 0.4, llm: 0.4, custom: 0.2} | Weights for hybrid complexity calculation |
| `overlord.workflow.routing_strategy` | ❌ No | enum | "capability_based" | Task routing strategy (capability_based, load_balanced, priority_based, custom, round_robin, specialized) |
| `overlord.workflow.enable_agent_affinity` | ❌ No | boolean | true | Prefer agents that successfully completed similar tasks |
| `overlord.workflow.error_recovery` | ❌ No | enum | "retry_with_backoff" | Error recovery strategy (fail_fast, retry_with_backoff, retry_with_alternate, skip_and_continue, compensate, manual_intervention) |
| `overlord.workflow.retry` | ❌ No | object | See below | Retry configuration for failed tasks |
| `overlord.workflow.retry.max_attempts` | ❌ No | integer | 3 | Maximum retry attempts (1-10) |
| `overlord.workflow.retry.initial_delay` | ❌ No | float | 1.0 | Initial retry delay in seconds |
| `overlord.workflow.retry.max_delay` | ❌ No | float | 60.0 | Maximum retry delay in seconds |
| `overlord.workflow.retry.backoff_factor` | ❌ No | float | 2.0 | Exponential backoff factor |
| `overlord.workflow.retry.retry_on_errors` | ❌ No | array | ["timeout", "rate_limit", "temporary_failure"] | Error types to retry on |
| `overlord.workflow.timeouts` | ❌ No | object | See below | Timeout configuration |
| `overlord.workflow.timeouts.task_timeout` | ❌ No | float | 300 | Default timeout per task in seconds |
| `overlord.workflow.timeouts.workflow_timeout` | ❌ No | float | 3600 | Overall workflow timeout in seconds |
| `overlord.workflow.timeouts.enable_adaptive_timeout` | ❌ No | boolean | true | Adjust timeouts based on task complexity |
| `overlord.workflow.parallel_execution` | ❌ No | boolean | true | Execute independent tasks in parallel |
| `overlord.workflow.max_parallel_tasks` | ❌ No | integer | 5 | Maximum number of tasks to execute in parallel (1-20) |
| `overlord.workflow.partial_results` | ❌ No | boolean | true | Return partial results if some tasks fail |
| `overlord.workflow.max_timeout_seconds` | ❌ No | integer | 7200 | Maximum duration for entire workflow execution in seconds (2 hours) |

> [!NOTE]
> **Workflow Timeout Behavior:**
> - `max_timeout_seconds` provides a hard ceiling for the entire workflow execution (default: 7200 seconds = 2 hours)
> - This is different from `timeouts.workflow_timeout` which is used for adaptive timeout calculations
> - Workflows exceeding `max_timeout_seconds` will fail with a timeout error, regardless of task progress
> - This prevents runaway workflows from consuming resources indefinitely
> - For workflows that legitimately need longer execution (e.g., data processing, research), increase this value

#### Overlord Clarification Configuration
*Intelligent clarifying questions for incomplete requests (always enabled for better UX)*

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `overlord.clarification.style` | ❌ No | enum | "conversational" | Question style (conversational, formal, brief) |
| `overlord.clarification.max_rounds.direct` | ❌ No | integer (1-32) | 3 | Maximum clarification rounds for direct disambiguation |
| `overlord.clarification.max_rounds.brainstorm` | ❌ No | integer (1-32) | 10 | Maximum clarification rounds for creative exploration |
| `overlord.clarification.max_rounds.planning` | ❌ No | integer (1-32) | 7 | Maximum clarification rounds for requirements gathering |
| `overlord.clarification.max_rounds.execution` | ❌ No | integer (1-32) | 3 | Maximum clarification rounds for parameter clarification |
| `overlord.clarification.max_rounds.other` | ❌ No | integer (1-32) | 3 | Fallback limit for any unlisted clarification modes |

### Async Configuration
*Asynchronous request-response behavior for long-running agentic tasks*

```yaml
async:
  threshold_seconds: 30
  enable_estimation: true
  webhook_url: "https://myapp.com/webhooks/muxi"
  webhook_retries: 3
  webhook_timeout: 10
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `async.threshold_seconds` | ❌ No | integer | 30 | Time threshold in seconds - requests taking longer switch to async mode |
| `async.enable_estimation` | ❌ No | boolean | true | Allow overlord to estimate processing time for intelligent async decisions |
| `async.webhook_url` | ❌ No | string | None | Default webhook URL for async completion notifications (can be overridden per request) |
| `async.webhook_retries` | ❌ No | integer | 3 | Number of retry attempts for webhook delivery on failure |
| `async.webhook_timeout` | ❌ No | integer | 10 | Timeout in seconds for webhook delivery requests |

> [!NOTE]
> **Async Behavior**: When a request exceeds `threshold_seconds`, the overlord immediately returns a `request_id` and switches to async mode. The actual processing continues in the background, and results are delivered to the specified webhook URL upon completion. This prevents hanging connections and enables scalable handling of long-running agentic tasks.

> [!TIP]
> We recommend using a webhook URL that includes a hash stored in secrets of the request to prevent abuse (i.e. `https://myapp.com/webhooks/muxi?hash=${{ secrets.WEBHOOK_HASH }}`)

### Memory Configuration
*Working memory (always enabled) and optional persistent storage settings*

```yaml
memory:
  working:
    # Shared storage backend configuration (always enabled with defaults)
    max_memory_mb: "auto"  # Default: 10% of RAM (min 64MB, max 1GB)
    fifo_interval_min: 5  # FIFO cleanup interval in minutes
    vector_dimension: 1536
    mode: "local"
    remote:
      url: "tcp://localhost:8000"
      api_key: "${{ secrets.FAISSX_API_KEY }}"
      tenant: "${{ secrets.FAISSX_TENANT_ID }}"

  buffer:
    size: 10
    multiplier: 10
    vector_search: true

  persistent:  # Optional persistent memory
    connection_string: "postgres://user:password@localhost:5432/dbname"
    embedding_model: "text-embedding-ada-002"
```

#### Working Memory Configuration
*Working memory is always enabled and cannot be disabled. These settings control the shared storage backend.*

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `memory.working.max_memory_mb` | ❌ No | string/integer | "auto" | Maximum memory usage in MB. "auto" uses 10% of system RAM (min 64MB, max 1GB). **Note: Remote mode requires explicit integer values.** |
| `memory.working.fifo_interval_min` | ❌ No | integer | 5 | FIFO cleanup interval in minutes |
| `memory.working.vector_dimension` | ❌ No | integer | 1536 | Dimension for embedding vectors |
| `memory.working.mode` | ❌ No | enum | "local" | Vector search mode ("local" or "remote") |
| `memory.working.remote.url` | ❌ No | string | None | FAISSx server URL (required if mode = "remote") |
| `memory.working.remote.api_key` | ❌ No | string | None | FAISSx API key (required if mode = "remote") |
| `memory.working.remote.tenant` | ❌ No | string | None | FAISSx tenant ID (required if mode = "remote") |

> [!IMPORTANT]
> When using remote mode, the `max_memory_mb` must be an integer value.

#### Buffer Memory Configuration
*Buffer memory is always enabled and provides conversation context management.*

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `memory.buffer.size` | ❌ No | integer | 10 | Context window size (number of recent messages) |
| `memory.buffer.multiplier` | ❌ No | integer | 10 | Buffer multiplier (total capacity = size × multiplier) |
| `memory.buffer.vector_search` | ❌ No | boolean | true | Enable vector similarity search capabilities |

#### Persistent Memory Configuration
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `memory.persistent.connection_string` | ❌ No | string | None | Database connection string (PostgreSQL or SQLite) |
| `memory.persistent.embedding_model` | ❌ No | string | llm.models.embedding | Override embedding model for persistent memory |
| `memory.persistent.query_timeout_seconds` | ❌ No | integer | 30 | Maximum execution time for individual SQL queries in seconds |
| `memory.persistent.user_synopsis.enabled` | ❌ No | boolean | true | Enable/disable LLM-synthesized user synopsis generation |
| `memory.persistent.user_synopsis.cache_ttl` | ❌ No | integer | 3600 | Cache TTL in seconds for user synopsis (range: 60-86400) |

> [!NOTE]
> The `query_timeout_seconds` setting applies to both synchronous and asynchronous database engines. This prevents hung queries from exhausting the connection pool. Queries exceeding this timeout will be terminated automatically. If you experience legitimate slow queries (e.g., large aggregations on memory/observability tables), you may need to increase this value. However, 30 seconds should be sufficient for most production workloads.

**Note:** Document processing configuration is now integrated into the LLM model capabilities under `llm.models.documents.settings`. See the [Documents Model Settings](#documents-model-settings) section for complete configuration options.

**User Synopsis:**
The user synopsis feature automatically generates LLM-synthesized summaries of user context (identity, preferences, activities) for injection into enhanced messages. It uses a two-tier caching architecture for optimal performance. See your runtime's documentation for complete details.

### Logging Configuration
*Multi-destination observability streams with per-destination configuration*

```yaml
logging:
  enabled: true
  streams:
    # Simple stdout logging
    - transport: "stdout"
      level: "info"
      format: "jsonl"

    # File logging with debug detail
    - transport: "file"
      destination: "/var/logs/formation.log"
      level: "debug"
      format: "text"

    # Stream to external service
    - transport: "stream"
      destination: "https://logs.company.com/ingest"
      protocol: "http"
      format: "jsonl"
      auth:
        type: "bearer"
        token: "${{ secrets.LOG_TOKEN }}"
      events: ["request.*", "error.*"]

    # MUXI Trail service
    - transport: "trail"
      token: "${{ secrets.TRAIL_TOKEN }}"

    # Kafka streaming
    - transport: "stream"
      destination: "kafka://broker1:9092,broker2:9092"
      protocol: "kafka"
      topic: "application-logs"
      format: "jsonl"
      auth:
        type: "sasl"
        username: "${{ secrets.KAFKA_USER }}"
        password: "${{ secrets.KAFKA_PASS }}"
```

**Key Features:**
- **Multiple destinations**: Send different events to different outputs simultaneously
- **Per-stream configuration**: Each stream has its own level, format, events, and auth
- **Transport types**: `stdout`, `file`, `stream`, `trail` (MUXI-specific)
- **Protocols**: Auto-detected from URL (`https://` → http, `tcp://` → zmq, `kafka://` → kafka)
- **Formats**: `jsonl`, `text`, `msgpack`, `datadog_json`, `splunk_hec`, `elastic_bulk`, `grafana_loki`, `newrelic_json`, `opentelemetry`
- **Authentication**: Per-stream auth (bearer, basic, api_key, custom headers)
- **Event filtering**: Level-based or explicit event lists per stream

> [!TIP]
> **URL-based encryption**: Use `tcps://` and `ipcs://` for encrypted ZMQ connections (automatically uses CURVE encryption)

> [!NOTE]
> For comprehensive logging configuration examples, authentication methods, format specifications, and enterprise deployment patterns, see [`LOGGING.md`](./LOGGING.md).

### Scheduler Configuration
*Proactive task scheduling system for recurring AI tasks*

```yaml
scheduler:
  enabled: true                     # Enable/disable the scheduler service
  timezone: "UTC"                   # Formation timezone for cron execution
  check_interval_minutes: 1         # Check for due jobs every N minutes
  max_concurrent_jobs: 10           # Maximum concurrent job executions
  max_failures_before_pause: 3      # Auto-pause jobs after N consecutive failures
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `scheduler.enabled` | ❌ No | boolean | true | Enable or disable the scheduler service |
| `scheduler.timezone` | ❌ No | string | "UTC" | Formation timezone for cron expression execution and DST handling |
| `scheduler.check_interval_minutes` | ❌ No | integer | 1 | How often (in minutes) to check for jobs that are due for execution |
| `scheduler.max_concurrent_jobs` | ❌ No | integer | 10 | Maximum number of jobs that can run simultaneously |
| `scheduler.max_failures_before_pause` | ❌ No | integer | 3 | Number of consecutive failures before a job is automatically paused |

> [!NOTE]
> **Scheduler Behavior**:
> - The scheduler enables users to schedule recurring AI tasks using natural language (e.g., "check my email every hour for messages from my wife")
> - Jobs are executed using the existing `overlord.chat()` system with `f"job_{job.id}"` as session_id
> - Results are delivered through existing Formation webhook settings
> - The scheduler uses a map/reduce pattern for job selection and supports dynamic exclusion rules
> - Timezone conversion handles DST transitions automatically using pytz

> [!TIP]
> **Timezone Handling**:
> - User times are converted to formation timezone during job creation
> - Cron expressions are stored in formation timezone
> - DST transitions are handled automatically at execution time
> - For best results, use "UTC" for consistent scheduling across regions

### A2A Configuration
*Agent-to-Agent communication settings for inbound and outbound connections*

```yaml
a2a:
  enabled: true

  # Intelligent agent filtering for large formations
  filtering:
    enabled: false                    # Enable intelligent filtering
    threshold: 50                    # Filter if total agents > this
    always_include_threshold: 0.8    # Always include high-confidence matches
    min_relevance_score: 0.3         # Minimum relevance score to consider
    cache_ttl: 1800                  # Cache TTL in seconds (30 minutes)

  outbound:
    enabled: true
    registries:
      - "https://a2a.muxihub.com"
      - "https://agents.partner.com"
    default_retry_attempts: 3
    default_timeout_seconds: 30

    # Services can be defined inline or auto-discovered from a2a/*.yaml files
    services:
      - id: "external-billing-service"
        name: "External Billing Service"
        description: "External billing and payment processing service"
        url: "https://billing.external.com/a2a"
        auth:
          type: "api_key"
          header: "X-API-Key"
          key: "${{ secrets.BILLING_API_KEY }}"

  inbound:
    enabled: true
    registries:
      - "https://private.company.com"
    port: 8181
    trusted_endpoints:
      - "muxi.partner.com"

    # Inbound authentication configuration
    auth:
      type: "bearer"                              # Authentication type: bearer, api_key, basic
      token: "${{ secrets.A2A_BEARER_TOKEN }}"    # Authentication token/key
```

#### A2A General Configuration
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `a2a.enabled` | ❌ No | boolean | true | Enable Agent-to-Agent communication capabilities |
| `a2a.filtering.enabled` | ❌ No | boolean | false | Enable intelligent agent filtering for planning optimization |
| `a2a.filtering.threshold` | ❌ No | integer | 50 | Apply filtering when total agents exceed this threshold |
| `a2a.filtering.always_include_threshold` | ❌ No | float | 0.8 | Always include agents with confidence score above this value |
| `a2a.filtering.min_relevance_score` | ❌ No | float | 0.3 | Minimum relevance score for an agent to be considered |
| `a2a.filtering.cache_ttl` | ❌ No | integer | 1800 | Cache time-to-live in seconds for filtered results |

#### A2A Outbound Configuration
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `a2a.outbound.enabled` | ❌ No | boolean | true | Enable outbound A2A communication |
| `a2a.outbound.startup_policy` | ❌ No | enum | "lenient" | Registry connection policy: lenient, strict, retry |
| `a2a.outbound.retry_timeout_seconds` | ❌ No | integer | 30 | Retry duration for "retry" policy before applying required flags |
| `a2a.outbound.registries` | ❌ No | array/object | [] | List of external A2A registries (see formats below) |
| `a2a.outbound.default_retry_attempts` | ❌ No | integer | 3 | Default number of retry attempts for A2A requests |
| `a2a.outbound.default_timeout_seconds` | ❌ No | integer | 30 | Default timeout for A2A requests |
| `a2a.outbound.services` | ❌ No | array | [] | Inline services or auto-discovered from `a2a/*.yaml`. See [A2A Service Schema](#-a2a-service-schema-a2ayaml) for full field reference |
| `a2a.outbound.services[].id` | ✅ Yes | string | None | Unique service identifier |
| `a2a.outbound.services[].name` | ✅ Yes | string | None | Human-readable service name |
| `a2a.outbound.services[].description` | ✅ Yes | string | None | Service description |
| `a2a.outbound.services[].url` | ✅ Yes | string | None | Service A2A endpoint URL |
| `a2a.outbound.services[].auth` | ❌ No | object | None | Authentication configuration |
| `a2a.outbound.services[].auth.type` | ✅ Yes | enum | None | Auth type: bearer, api_key, basic |
| `a2a.outbound.services[].auth.token` | ✅ Yes (if bearer) | string | None | Bearer token |
| `a2a.outbound.services[].auth.key` | ✅ Yes (if api_key) | string | None | API key value |
| `a2a.outbound.services[].auth.header` | ❌ No | string | "X-API-Key" | API key header name |
| `a2a.outbound.services[].auth.username` | ✅ Yes (if basic) | string | None | Basic auth username |
| `a2a.outbound.services[].auth.password` | ✅ Yes (if basic) | string | None | Basic auth password |

**Registry Configuration Formats:**

Registries support two formats - simple strings for backward compatibility and extended objects for fine control:

```yaml
# Simple format (all registries are optional by default)
registries:
  - "https://a2a.muxihub.com"
  - "https://agents.partner.com"

# Extended format with per-registry configuration
registries:
  - url: "https://critical.registry.com"
    required: true                      # Formation fails to start if unreachable
    health_check_timeout_seconds: 5     # Timeout for startup health check
    retry_attempts: 5                   # Override default retry attempts

  - url: "https://optional.registry.com"
    required: false                      # Formation continues without this registry
    health_check_timeout_seconds: 2
```

**Extended Registry Fields:**
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `url` | ✅ Yes | string | None | Registry URL |
| `required` | ❌ No | boolean | false | Whether formation should fail if registry is unreachable |
| `health_check_timeout_seconds` | ❌ No | integer | 5 | Timeout for startup health check |
| `retry_attempts` | ❌ No | integer | (uses default) | Override default retry attempts for this registry |

**Startup Policies:**
- **`lenient`** (default): Log warnings and continue if registries are unreachable. Best for development and resilient production systems.
- **`strict`**: Fail immediately if any registry marked as `required: true` is unreachable. Best for production systems with critical dependencies.
- **`retry`**: Attempt connections for `retry_timeout_seconds`, then apply `required` flags. Best for systems with transient network issues.

**Examples:**

```yaml
# Development - Continue regardless of registry availability
a2a:
  outbound:
    startup_policy: "lenient"
    registries:
      - "http://localhost:9090"

# Production - Critical registry must be available
a2a:
  outbound:
    startup_policy: "strict"
    registries:
      - url: "https://registry.production.com"
        required: true
        health_check_timeout_seconds: 10

# Mixed - Some registries are critical, others optional
a2a:
  outbound:
    startup_policy: "retry"
    retry_timeout_seconds: 60
    registries:
      - url: "https://critical.internal.com"
        required: true
      - url: "https://optional.partner.com"
        required: false
```

> [!NOTE]
> **Service ID Format**: The `service_id` identifies which authentication to use for outbound requests. It supports multiple formats with precedence:
> - `agent-id@hostname:port` - Most specific, for agent-specific authentication
> - `hostname:port` - For all agents at a specific server endpoint
> - `hostname` - For all services on a host
> - `port` - For all localhost services on a specific port
>
> Example: If calling `http://api.partner.com:8080/agents/project-manager/message`, the system will check for service_id in this order:
> 1. `project-manager@api.partner.com:8080`
> 2. `api.partner.com:8080`
> 3. `api.partner.com`
> 4. `8080` (for localhost only)

#### A2A Inbound Configuration
| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `a2a.inbound.enabled` | ❌ No | boolean | true | Enable inbound A2A communication |
| `a2a.inbound.startup_policy` | ❌ No | enum | "lenient" | Registry connection policy (same as outbound) |
| `a2a.inbound.retry_timeout_seconds` | ❌ No | integer | 30 | Retry duration for "retry" policy |
| `a2a.inbound.registries` | ❌ No | array/object | [] | List of registries for server registration (same formats as outbound) |
| `a2a.inbound.port` | ❌ No | integer | 8181 | Port for A2A server to listen on |
| `a2a.inbound.trusted_endpoints` | ❌ No | array | [] | List of trusted external endpoints |
| `a2a.inbound.auth` | ❌ No | object | None | Authentication configuration for inbound requests |
| `a2a.inbound.auth.type` | ✅ Yes (if auth defined) | enum | None | Authentication type (bearer, api_key, basic) |
| `a2a.inbound.auth.token` | ✅ Yes (if type=bearer) | string | None | Bearer token for authentication |
| `a2a.inbound.auth.key` | ✅ Yes (if type=api_key) | string | None | API key for authentication |
| `a2a.inbound.auth.header` | ❌ No | string | "X-API-Key" | Header name for API key authentication |
| `a2a.inbound.auth.username` | ✅ Yes (if type=basic) | string | None | Username for basic authentication |
| `a2a.inbound.auth.password` | ✅ Yes (if type=basic) | string | None | Password for basic authentication |

> [!NOTE]
> **Inbound Authentication**: When configured, all incoming A2A requests must provide the specified authentication. The auth configuration format is consistent with outbound services for easier management.

### MCP Configuration
*Model Context Protocol server defaults and manual configurations*

```yaml
mcp:
  # Connection/retry settings (for transient failures)
  default_retry_attempts: 3           # Retry attempts for server connection issues
  default_timeout_seconds: 30         # Timeout per individual tool call

  # Tool execution settings (for intelligent chaining)
  max_tool_iterations: 10             # Max loops of (execute → analyze → decide)
  max_tool_calls: 50                  # Max total individual tool calls
  max_repeated_errors: 3              # Number of same errors before stopping

  # Timeout settings
  max_timeout_in_seconds: 300         # Total timeout for entire operation
  max_tool_timeout_in_seconds: 30     # Timeout per individual tool call

  # Message enhancement for better tool selection
  enhance_user_prompts: true          # Use LLM to enhance ambiguous messages for tool selection

  servers: []                         # Manual MCP server configurations
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `mcp.default_retry_attempts` | ❌ No | integer | 3 | Retry attempts for transient failures (network, timeouts) |
| `mcp.default_timeout_seconds` | ❌ No | integer | 30 | Default timeout for MCP tool calls |
| `mcp.max_tool_iterations` | ❌ No | integer | 10 | Maximum execution loops for intelligent problem solving |
| `mcp.max_tool_calls` | ❌ No | integer | 50 | Maximum total tool calls across all iterations |
| `mcp.max_repeated_errors` | ❌ No | integer | 3 | Number of similar errors before stopping |
| `mcp.max_timeout_in_seconds` | ❌ No | integer | 300 | Total timeout for entire operation chain |
| `mcp.max_tool_timeout_in_seconds` | ❌ No | integer | 30 | Timeout per individual tool call |
| `mcp.enhance_user_prompts` | ❌ No | boolean | true | Use LLM to enhance ambiguous messages for better tool selection |
| `mcp.servers` | ❌ No | array | [] | Manual MCP server configurations (auto-discovered from mcp/) |

> [!NOTE]
> **Intelligent Tool Chaining**: When an agent encounters an error during tool execution, it will intelligently analyze the error and attempt to resolve it by:
> - Using alternative tools (e.g., creating a directory before writing a file)
> - Trying different approaches (e.g., writing to a different location if permission denied)
> - Explaining why a task cannot be completed when recovery is not possible
>
> This behavior is always enabled and helps agents complete complex tasks without manual intervention.

> [!TIP]
> **Message Enhancement**: When `enhance_user_prompts` is enabled (default: true), the system uses an LLM to automatically enhance ambiguous user messages before tool selection. For example:
> - "list my repositories" → "list all repositories in my GitHub account"
> - "my issues" → "show all issues assigned to me in my GitHub account"
>
> This helps reduce clarification prompts and improves tool selection accuracy without changing the user's intent.

### Runtime Configuration
*Built-in MCP servers and runtime behavior settings*

```yaml
runtime:
  # Simple configuration
  built_in_mcps: true  # Enable/disable all built-in MCPs

  # OR granular control (recommended)
  built_in_mcps:
    - file-generation     # Enable file generation MCP
    - web-search         # Enable web search MCP (future)
    # - database         # Disable database MCP (future)
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `runtime.built_in_mcps` | ❌ No | boolean/array | true | Enable/disable built-in MCP servers. Can be boolean (simple mode) or array of specific MCPs (granular mode) |

**Built-in MCP Options:**
- `file-generation`: Enables automatic file creation (charts, documents, spreadsheets, images, presentations)
- `web-search`: Enables web search capabilities (future)
- `database`: Enables database query tools (future)

> [!NOTE]
> **Built-in MCPs**: These are pre-installed MCP servers that provide common functionality like file generation. They are automatically registered and available to all agents when enabled. The system supports both simple boolean control (all on/off) and granular array control (specific MCPs).

> [!TIP]
> **File Generation**: When enabled, agents can generate files by writing Python code that gets safely executed. Supports matplotlib/pandas for charts, python-docx for documents, openpyxl for spreadsheets, and more. Code is validated and executed in a secure subprocess environment.

### User Credentials Configuration
*Security-focused credential handling for MCP services and tools*

```yaml
user_credentials:
  # Credential handling mode
  mode: "redirect"  # Options: "redirect" (default) | "dynamic"

  # Custom message shown when redirecting credential requests
  redirect_message: |
    For security, credentials must be configured outside of this chat interface.
    Please use your organization's credential management system to set up authentication.

  # Optional encryption key for credential storage (used in dynamic mode)
  encryption_key: "${{ secrets.CREDENTIAL_ENCRYPTION_KEY }}"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `user_credentials.mode` | ❌ No | enum | "redirect" | Credential handling mode (redirect, dynamic) |
| `user_credentials.redirect_message` | ❌ No | string | See example | Custom message when redirecting credential requests |
| `user_credentials.encryption.key` | ❌ No | string | null | Encryption key for credential storage (null uses formation_id) |
| `user_credentials.encryption.salt` | ❌ No | string | "muxi-user-credentials-salt-v1" | Salt for key derivation (configurable per formation) |

> [!NOTE]
> **Security Modes**:
> - **Redirect Mode** (default): Always redirects users to external credential management systems. Provides maximum security by never handling credentials in the chat interface.
> - **Dynamic Mode**: Intelligently decides whether to accept credentials inline based on authentication type and security context. Only available in specified environments.

> [!TIP]
> **Encryption Configuration**:
> - **Encryption Key** (`encryption.key`): Main encryption key for credential storage. If not provided, defaults to `formation_id` (which triggers a security warning).
> - **Salt** (`encryption.salt`): Used for key derivation with PBKDF2 (100,000 iterations). Each formation can use a unique salt for additional security isolation.
> - **Portability**: Both key and salt travel with the formation YAML, making formations portable across installations.
> - **Security Best Practice**: Use a strong, randomly-generated encryption key (not formation_id) and consider using a unique salt per formation.

> [!IMPORTANT]
> **Dynamic Mode Security**: When using dynamic mode:
> - Only enable in development/staging environments
> - Always use HTTPS in production
> - Credentials are encrypted with either the provided key or formation_id
> - TTL ensures credentials don't persist indefinitely
> - Failed attempts trigger automatic lockout

**Example Configurations:**

```yaml
# Production setup - always redirect
user_credentials:
  mode: "redirect"
  redirect_message: |
    🔐 Security Policy: Credentials must be managed through our SSO portal.
    Visit: https://sso.company.com/credentials
    Contact IT: support@company.com

# Development setup - allow inline for convenience
user_credentials:
  mode: "dynamic"
  allowed_environments: ["development"]
  encryption_key: "${{ secrets.DEV_ENCRYPTION_KEY }}"
  credential_ttl_minutes: 30
  max_attempts: 5

# Enterprise setup with custom branding
user_credentials:
  mode: "redirect"
  redirect_message: |
    Welcome to SecureCorp AI Assistant

    For your security, authentication credentials must be configured
    through our centralized identity management system.

    Please visit: https://identity.securecorp.com/ai-credentials

    For assistance, contact your IT administrator or email: ai-support@securecorp.com
```

### Agent Configuration
*Manual agent configurations (automatically discovered from agents/ directory)*

```yaml
agents: []
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `agents` | ❌ No | array | [] | Manual agent configurations (auto-discovered from agents/) |

### Component Auto-Discovery
*Overview of automatically discovered components from directory structure*

```yaml
# These are auto-discovered from directories, no need to list unless custom config needed
agents: []      # Auto-discovered from agents/
mcp:
  servers: []   # Auto-discovered from mcp/
a2a:
    outbound:
        services: [] # Auto-discovered from a2a/
```

---

## 👤 Agent Schema (`agents/*.yaml`)

### Basic Agent Information
*Essential metadata and identification for individual agents*

```yaml
schema: "1.0.0"                     # REQUIRED: Schema version
id: "weather-assistant"             # REQUIRED: Unique agent identifier
name: "Weather Assistant"           # REQUIRED: Human-readable name
description: "Specialized in providing weather forecasts and meteorological information."  # REQUIRED
active: true                        # Optional: Agent activation state
allow_filtering: true               # Optional: Whether agent can be filtered out in planning

# Optional metadata fields
author: "Author Name <email@domain.com>"
url: "https://example.com"
license: "MIT"
version: "1.0.0"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `schema` | ✅ Yes | string | None | Agent schema version using semantic versioning |
| `id` | ✅ Yes | string | None | Unique identifier for this agent (supports namespacing with '/') |
| `name` | ✅ Yes | string | None | Human-readable display name for the agent |
| `description` | ✅ Yes | string | None | Clear description of the agent's purpose and capabilities |
| `active` | ❌ No | boolean | true | Whether the agent is active and available for interactions |
| `allow_filtering` | ❌ No | boolean | true | Whether agent can be filtered out when formations have many agents (>50) |
| `author` | ❌ No | string | None | Author information with optional email contact |
| `url` | ❌ No | string | None | URL for agent documentation or repository |
| `license` | ❌ No | string | "Unlicense" | License type (e.g., MIT, Apache-2.0) |
| `version` | ❌ No | string | None | Agent version using semantic versioning |

### System Behavior Configuration
*Agent personality, behavior instructions, and operational guidelines*

```yaml
system_message: |
  You are a weather assistant that provides accurate forecasts and meteorological information.
  Only answer questions related to weather. For other topics, explain that you are a
  specialized weather assistant and cannot help with unrelated questions.
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `system_message` | ❌ No | string | None | Multi-line system prompt that defines agent behavior and personality |

### Agent-to-Agent Communication
*Configuration for intra-formation and external A2A participation*

```yaml
a2a:
  internal: true  # Participates in formation A2A
  external: true  # Participates in external A2A
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `a2a.internal` | ❌ No | boolean | true | Whether agent participates in intra-formation A2A communication |
| `a2a.external` | ❌ No | boolean | true | Whether agent participates in external A2A communication (if registries configured) |

> [!NOTE]
> A2A requires `formation.a2a.enabled` to be set to `true` (default behavior) for the agent to participate in A2A communication.

### Model Configuration Overrides
*Agent-specific model settings that override formation defaults*

```yaml
llm_models:
  - text: "openai/gpt-4o"             # Override text capability
    api_key: "${{ secrets.AGENT_OPENAI_KEY }}"    # Agent-specific key
    settings:
      temperature: 0.2                # Lower temperature for factual responses
      max_tokens: 4096
      timeout_seconds: 30
  - vision: "anthropic/claude-3-opus"
    api_key: "${{ secrets.AGENT_ANTHROPIC_KEY }}"
    settings:
      temperature: 0.7
      max_tokens: 1500
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `llm_models[].text` | ❌ No | string | Formation default | Override model for text generation and conversation |
| `llm_models[].vision` | ❌ No | string | Formation default | Override model for image analysis and vision tasks |
| `llm_models[].audio` | ❌ No | string | Formation default | Override model for audio transcription and processing |
| `llm_models[].documents` | ❌ No | string | Formation default | Override model for document processing and extraction |
| `llm_models[].embedding` | ❌ No | string | Formation default | Override model for generating text embeddings |
| `llm_models[].api_key` | ❌ No | string | Formation api_keys | Agent-specific API key override for this model |
| `llm_models[].settings` | ❌ No | object | Formation defaults | Model-specific configuration overrides |
| `llm_models[].settings.temperature` | ❌ No | float | Formation default | Creativity level (0.0-1.0) for this agent's model |
| `llm_models[].settings.max_tokens` | ❌ No | integer | Formation default | Maximum tokens for responses from this agent |
| `llm_models[].settings.timeout_seconds` | ❌ No | integer | Formation default | Request timeout for this agent's model calls |
| `llm_models[].settings.max_retries` | ❌ No | integer | Formation default | Override number of retry attempts for this agent's model |
| `llm_models[].settings.fallback_model` | ❌ No | string | Formation default | Override fallback model if this agent's model fails |

### Role and Specialization
*Agent classification and domain expertise for intelligent routing*

```yaml
role: "specialist"                 # Options: "general", "specialist", "assistant"
specialties:
  - "weather_forecasting"          # Areas this agent specializes in
  - "meteorology"                  # Used for routing decisions
  - "climate_data"                 # and capability discovery
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `role` | ❌ No | enum | Auto-inferred | Agent classification (general, specialist, assistant, etc.) |
| `specialties` | ❌ No | array | Auto-inferred | List of domain areas this agent specializes in for routing |

> [!NOTE]
> **Automatic Inference**: Role and specialties can be automatically inferred from the `system_message` and `description` fields. Include them only if you want to override the automatic inference or provide more specific routing hints.

### Domain Knowledge Configuration
*External knowledge sources confined to formation directory*

```yaml
knowledge:
  enabled: true
  sources:
    - path: "knowledge/faq/"
      description: "Frequently asked questions about our products"
    - path: "knowledge/products.txt"
      description: "Information about our product catalog"
    - path: "docs/pricing.txt"
      description: "Pricing information (can be anywhere in formation)"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `knowledge.enabled` | ❌ No | boolean | false | Whether to enable domain knowledge enhancement for this agent |
| `knowledge.sources` | ❌ No | array | [] | List of knowledge source configurations |
| `knowledge.sources[].path` | ✅ Yes (if sources defined) | string | None | Path to knowledge file or directory relative to formation root (absolute paths rejected) |
| `knowledge.sources[].description` | ✅ Yes (if sources defined) | string | None | Description of what this knowledge source contains |

> [!IMPORTANT]
> **Path Security**: All knowledge paths must be relative to the formation directory root. Absolute paths (starting with `/`) and parent directory traversal (`..`) are rejected for security. This ensures formations are self-contained and portable.

> [!TIP]
> **Organization**: We recommend keeping knowledge files in a `knowledge/` subdirectory for consistency with `agents/`, `mcp/`, and `a2a/` directories. However, knowledge can be stored anywhere within the formation directory.

> [!NOTE]
> **Future Enhancement**: Remote knowledge sources (S3, HTTP) will be supported in a future release. These will be downloaded during formation deployment and stored locally within the formation directory.
>
> We automatically cache the knowledge and won't re-parse it unless the source list changes.

### Agent-Specific MCP Server Access
*MCP servers exclusively available to this agent with optional authentication overrides*

> This should follow the same format as the MCP server schema in the mcp/ directory.

```yaml
mcp_servers:
  - id: "weather_service"          # Must match MCP server ID defined in formation
    retry_attempts: 3              # Optional: Override default retry attempts
    timeout_seconds: 30            # Optional: Override default retry attempts
    description: "External weather service" # Required
    active: true                   # Optional: Server activation state
    type: "http"                   # REQUIRED: Server type ("command" or "http")
    endpoint: "http://localhost:3000"  # REQUIRED: Server endpoint URL
    auth:                          # Optional: If MCP server requires authentication
      type: "api_key"
      header: "X-API-Key"
      key: "${{ secrets.WEATHER_API_KEY }}"
  - id: "local_tools"              # Another MCP server
    # ...
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `mcp_servers` | ❌ No | array | [] | List of MCP servers exclusively available to this agent |
| `mcp_servers[].id` | ✅ Yes (if servers defined) | string | None | Must match an MCP server ID defined in formation or mcp/ directory |
| `mcp_servers[].retry_attempts` | ❌ No | integer | None | Override default retry attempts for this MCP server |
| `mcp_servers[].timeout_seconds` | ❌ No | integer | None | Override default timeout for this MCP server |
| `mcp_servers[].description` | ✅ Yes (if servers defined) | string | None | Description of the MCP server |
| `mcp_servers[].active` | ❌ No | boolean | true | Whether the MCP server is active and available for tool calls |
| `mcp_servers[].type` | ✅ Yes (if servers defined) | enum | None | Server type ("command" or "http") |
| `mcp_servers[].endpoint` | ✅ Yes (if type=http) | string | None | Server endpoint URL (must include protocol: http:// or https://) |
| `mcp_servers[].auth` | ❌ No | object | None | Required if MCP server requires authentication |
| `mcp_servers[].auth.type` | ✅ Yes (if auth defined) | enum | None | Authentication type (api_key, bearer, basic, none) |
| `mcp_servers[].auth.accept_inline` | ❌ No | boolean | false | Whether credentials can be collected inline in dynamic mode |
| `mcp_servers[].auth.header` | ❌ No | string | "Authorization" | HTTP header name for authentication |
| `mcp_servers[].auth.key` | ✅ Yes (if type=api_key) | string | None | API key value for authentication |
| `mcp_servers[].auth.token` | ✅ Yes (if type=bearer) | string | None | Bearer token for authentication |
| `mcp_servers[].auth.username` | ✅ Yes (if type=basic) | string | None | Username for basic authentication |
| `mcp_servers[].auth.password` | ✅ Yes (if type=basic) | string | None | Password for basic authentication |

> [!IMPORTANT]
> **MCP Server Access**:
> - **Formation-level MCP servers**: Available to ALL agents in the formation
> - **Agent-level MCP servers**: ONLY available to this specific agent
> - **Authentication overrides**: Agent can override MCP server authentication while using formation defaults for connection details

---

## 🔧 MCP Server Schema (`mcp/*.yaml`)

### Basic MCP Server Information
*Essential identification and metadata for MCP (Model Context Protocol) servers*

```yaml
schema: "1.0.0"                    # REQUIRED: Schema version
id: "local-tools"                  # REQUIRED: Unique server identifier
description: "Local command tools for file operations and system utilities"  # REQUIRED
active: true                       # Optional: Server activation state
type: "command"                    # REQUIRED: Server type ("command" or "http")

# Optional metadata fields
author: "Author Name <email@domain.com>"
url: "https://github.com/author/mcp-server"
license: "MIT"
version: "1.0.0"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `schema` | ✅ Yes | string | None | MCP server schema version using semantic versioning |
| `id` | ✅ Yes | string | None | Unique identifier for this MCP server within the formation |
| `description` | ✅ Yes | string | None | Clear description of the server's purpose and available tools |
| `active` | ❌ No | boolean | true | Whether the server is active and available for tool calls |
| `type` | ✅ Yes | enum | None | Server connection type ("command" for local executables, "http" for web services) |
| `author` | ❌ No | string | None | Author information with optional email contact |
| `url` | ❌ No | string | None | URL for server documentation or repository |
| `license` | ❌ No | string | "Unlicense" | License type (e.g., MIT, Apache-2.0) |
| `version` | ❌ No | string | None | Server version using semantic versioning |

### Command-Based MCP Server Configuration
*Local executable MCP servers that run as child processes*

```yaml
schema: "1.0.0"
id: "local-tools"
description: "Local command tools for file operations"
active: true
type: "command"                    # REQUIRED for command servers

# Installation configuration
install: "npm install -g @modelcontextprotocol/server-json-rpc"  # Optional: Auto-install command

# Command execution configuration
command: "npx"                     # REQUIRED: Executable command
args: ["-y", "@modelcontextprotocol/server-json-rpc"]  # Optional: Command arguments
working_directory: "/home/user/tools"  # Optional: Working directory
timeout_seconds: 60                # Optional: Process timeout
max_retries: 3                     # Optional: Retry attempts on failure

# Use auth.type="env" to pass environment variables to command-based MCP servers
# auth:
#   type: "env"
#   API_KEY: "${{ secrets.TOOLS_API_KEY }}"
#   DEBUG: "true"
#   LOG_LEVEL: "info"
#   BRAVE_API_KEY: "${{ secrets.BRAVE_API_KEY }}"
#   OPENAI_API_KEY: "${{ user.credentials.openai }}"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `install` | ❌ No | string | None | Command to auto-install the MCP server during formation deployment |
| `command` | ✅ Yes | string | None | Executable command or binary to run (e.g., "python", "node", "npx") |
| `args` | ❌ No | array | [] | Array of command-line arguments to pass to the executable |
| `working_directory` | ❌ No | string | Current directory | Working directory for the command execution |
| `timeout_seconds` | ❌ No | integer | Formation default | Maximum time to wait for command startup |
| `max_retries` | ❌ No | integer | Formation default | Number of retry attempts if the process fails to start |

> [!TIP]
> **Installation & Command Examples**:
> - **NPM Global**: `install: "npm install -g @org/mcp-server"`, `command: "npx"`, `args: ["-y", "@org/mcp-server"]`
> - **Python Package**: `install: "pip install my-mcp-server"`, `command: "python"`, `args: ["-m", "my_mcp_server"]`
> - **Node.js Local**: `install: "npm install"`, `command: "node"`, `args: ["server.js"]`
> - **Custom Binary**: `install: "curl -L https://releases.com/server | tar -xz"`, `command: "./my-mcp-server"`
> - **No Install**: Omit `install` field if server is pre-installed or available in PATH

> [!NOTE]
> **Environment Variable Authentication**: For command-based MCP servers that require API keys via environment variables (like Brave Search), use `auth.type="env"`:
> ```yaml
> # web-search.yaml
> schema: "1.0.0"
> id: "web-search-mcp"
> description: "Web search using Brave Search API"
> type: "command"
> command: "npx"
> args: ["-y", "brave-search-mcp"]
>
> auth:
>   type: "env"
>   BRAVE_API_KEY: "${{ secrets.BRAVE_API_KEY }}"      # From secrets
>   # BRAVE_API_KEY: "${{ user.credentials.brave }}"   # From user credentials
>   # Additional env vars can be added as needed
> ```

### HTTP-Based MCP Server Configuration
*Remote web-based MCP servers accessed via HTTP/HTTPS*

```yaml
schema: "1.0.0"                    # REQUIRED: Schema version
id: "web-tools"                    # REQUIRED: Unique server identifier
description: "External web tools"  # REQUIRED: Human-readable description
active: true                       # Optional: Server activation state
type: "http"                       # REQUIRED: Server type for HTTP servers

# Connection configuration
endpoint: "http://localhost:3000"  # REQUIRED: Server endpoint URL
timeout_seconds: 30                # Optional: Request timeout override
retry_attempts: 3                  # Optional: Number of retry attempts
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `endpoint` | ✅ Yes | string | None | Server endpoint URL (must include protocol: http:// or https://) |
| `timeout_seconds` | ❌ No | integer | Formation default | Request timeout in seconds |
| `retry_attempts` | ❌ No | integer | Formation default | Number of retry attempts for failed requests |

### Authentication Configuration
*Authentication settings for MCP server access*

```yaml
# Bearer token authentication (as shown in web_tools.yaml)
auth:
  type: "bearer"                   # Auth type: bearer, basic, api_key, env, none
  accept_inline: true              # Allow inline credential collection in dynamic mode
  token: "${{ secrets.MCP_TOKEN }}" # Auth token (for bearer)

# Alternative for basic auth:
# auth:
#   type: "basic"
#   accept_inline: true              # Allow inline collection
#   username: "${{ secrets.MCP_USERNAME }}"
#   password: "${{ secrets.MCP_PASSWORD }}"

# Alternative for API key:
# auth:
#   type: "api_key"
#   accept_inline: true              # API keys typically safe for inline
#   header: "X-API-Key"
#   key: "${{ secrets.API_KEY }}"

# Environment variable authentication (for command-based MCP servers only)
# auth:
#   type: "env"
#   accept_inline: false             # Environment vars may contain multiple values
#   BRAVE_API_KEY: "${{ secrets.BRAVE_API_KEY }}"     # Using secrets
#   OPENAI_API_KEY: "${{ user.credentials.openai }}"  # Using user credentials
#   DEBUG_MODE: "true"                                 # Hardcoded value
#   # Any number of environment variables can be added

# No authentication
# auth:
#   type: "none"
#   accept_inline: false             # No credentials to collect
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `auth.type` | ❌ No | enum | "none" | Authentication method (bearer, basic, api_key, env, none) |
| `auth.accept_inline` | ❌ No | boolean | false | Whether credentials can be collected inline in dynamic mode |
| `auth.token` | ✅ Yes (if type=bearer) | string | None | Bearer token for Authorization header |
| `auth.username` | ✅ Yes (if type=basic) | string | None | Username for basic authentication |
| `auth.password` | ✅ Yes (if type=basic) | string | None | Password for basic authentication |
| `auth.header` | ❌ No | string | "X-API-Key" | Header name for API key authentication |
| `auth.key` | ✅ Yes (if type=api_key) | string | None | API key value |
| `auth.*` | ✅ Yes (if type=env) | string | None | Environment variables to pass to command-based MCP servers (any key except 'type' or 'accept_inline') |

---

## 🌐 A2A Service Schema (`a2a/*.yaml`)

### Basic A2A Service Information
*Essential identification and connection details for external Agent-to-Agent services*

```yaml
schema: "1.0.0"                    # REQUIRED: Schema version
id: "external-billing-service"     # REQUIRED: Unique service identifier
name: "External Billing Service"   # REQUIRED: Human-readable name
description: "External billing and payment processing service for order management"  # REQUIRED
url: "https://billing.external.com/a2a"  # REQUIRED: Service A2A endpoint
active: true                       # Optional: Service activation state

# Optional metadata fields
author: "External Partner <api@external.com>"
version: "2.1.0"
documentation: "https://docs.external.com/a2a"
support_contact: "support@external.com"
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `schema` | ✅ Yes | string | None | A2A service schema version using semantic versioning |
| `id` | ✅ Yes | string | None | Unique identifier for this A2A service within the formation |
| `name` | ✅ Yes | string | None | Human-readable display name for the service |
| `description` | ✅ Yes | string | None | Clear description of the service's purpose and capabilities |
| `url` | ✅ Yes | string | None | Base URL for A2A communication endpoint (must include protocol) |
| `active` | ❌ No | boolean | true | Whether the service is active and available for A2A communication |
| `author` | ❌ No | string | None | Service provider information with optional contact |
| `version` | ❌ No | string | None | Service API version using semantic versioning |
| `documentation` | ❌ No | string | None | URL for service documentation or API reference |
| `support_contact` | ❌ No | string | None | Contact information for service support |


### Rate Limiting Configuration
*Traffic control and performance management settings*

```yaml
# Retry and timeout overrides
retry_attempts: 3              # Optional: Override default retry attempts from a2a.outbound.default_retry_attempts
timeout_seconds: 30            # Optional: Override default timeout from a2a.outbound.default_timeout_seconds
```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `retry_attempts` | ❌ No | integer | 3 | Override default retry attempts from a2a.outbound.default_retry_attempts |
| `timeout_seconds` | ❌ No | integer | 30 | Override default timeout from a2a.outbound.default_timeout_seconds |


### Authentication Configuration
*Authentication methods for accessing external A2A services*

```yaml
# API Key Authentication
auth:
  type: "api_key"
  header: "X-API-Key"              # Custom header name
  key: "${{ secrets.EXTERNAL_BILLING_API_KEY }}"

# Bearer Token Authentication
auth:
  type: "bearer"
  token: "${{ secrets.EXTERNAL_SERVICE_TOKEN }}"

# Basic Authentication
auth:
  type: "basic"
  username: "${{ secrets.EXTERNAL_USERNAME }}"
  password: "${{ secrets.EXTERNAL_PASSWORD }}"

# Custom Header Authentication
auth:
  type: "custom"
  headers:
    Authorization: "Custom ${{ secrets.CUSTOM_TOKEN }}"
    X-Client-ID: "${{ secrets.CLIENT_ID }}"
    X-Tenant: "${{ secrets.TENANT_ID }}"

# No Authentication
  auth:
    type: "none"
  ```

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `auth.type` | ❌ No | enum | "none" | Authentication method (api_key, bearer, basic, custom, none) |
| `auth.header` | ❌ No | string | "Authorization" | Header name for API key authentication |
| `auth.key` | ✅ Yes (if type=api_key) | string | None | API key value for authentication |
| `auth.token` | ✅ Yes (if type=bearer) | string | None | Bearer token for Authorization header |
| `auth.username` | ✅ Yes (if type=basic) | string | None | Username for basic authentication |
| `auth.password` | ✅ Yes (if type=basic) | string | None | Password for basic authentication |
| `auth.headers` | ✅ Yes (if type=custom) | object | None | Custom headers object for authentication |

> [!IMPORTANT]
> **Authentication Methods**:
> - **API Key**: Adds `{header}: {key}` header (default: `Authorization: {key}`)
> - **Bearer**: Adds `Authorization: Bearer {token}` header
> - **Basic**: Adds `Authorization: Basic {base64(username:password)}` header
> - **Custom**: Adds all specified headers exactly as configured
> - **None**: No authentication headers sent


---

## 🔄 Override Hierarchy

### LLM Configuration Precedence (Highest to Lowest)
1. **Agent-specific model overrides** (`agents/*.yaml` → `llm_models:`)
2. **Overlord LLM configuration** (`formation.yaml` → `overlord.llm`)
3. **Formation default LLM settings** (`formation.yaml` → `llm:`)

### Example Override Flow
```yaml
# formation.yaml - Base defaults
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

# agents/my_agent.yaml - Agent overrides
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
> **User Credentials**: Unlike secrets which are formation-wide and loaded at initialization, user credentials are:
> - User-specific and isolated per user
> - Loaded on-demand when needed
> - Stored securely in the database credentials table
> - Automatically trigger clarification flow if missing
> - Cached in memory during the session for performance

> [!WARNING]
> When using user credentials, you must ensure that you have a secret stored with a similar name, to enable tool discovery upon initialization (eg. if you use `${{ user.credentials.gmail }}` in the formation, you must have a secret stored with the name `USER_CREDENTIALS_GMAIL` in the secrets store).


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

This schema guide ensures proper configuration structure and validation compliance for all MUXI formation components.
