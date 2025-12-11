# MUXI Logging Configuration Guide

## 📋 Overview

MUXI's observability system provides enterprise-grade logging with multi-destination streams, per-destination configuration, and flexible event routing. This guide covers all configuration options, deployment patterns, and best practices.

**Key Principles:**
- **Dual Architecture**: Runtime events (always stdout) + Observability events (configurable streams)
- **Zero Storage**: MUXI captures and emits events but doesn't store them
- **Multi-Destination**: Send different events to different outputs simultaneously
- **Per-Stream Config**: Each destination has independent level, format, events, and auth

## 📚 Table of Contents

- [MUXI Logging Configuration Guide](#muxi-logging-configuration-guide)
  - [📋 Overview](#-overview)
  - [📚 Table of Contents](#-table-of-contents)
  - [🚀 Quick Start](#-quick-start)
    - [Simple Console Logging](#simple-console-logging)
    - [Multi-Destination Setup](#multi-destination-setup)
  - [🚚 Transport Types](#-transport-types)
    - [stdout Transport](#stdout-transport)
    - [file Transport](#file-transport)
    - [stream Transport](#stream-transport)
    - [trail Transport (MUXI-Specific)](#trail-transport-muxi-specific)
  - [🌐 Network Protocols](#-network-protocols)
    - [HTTP/HTTPS (webhook)](#httphttps-webhook)
    - [ZeroMQ (zmq)](#zeromq-zmq)
    - [WebSocket (websocket)](#websocket-websocket)
  - [📄 Data Formats](#-data-formats)
    - [Standard Formats](#standard-formats)
      - [jsonl (JSON Lines)](#jsonl-json-lines)
      - [text (Human-Readable)](#text-human-readable)
      - [msgpack (Binary)](#msgpack-binary)
    - [Service-Specific Formats](#service-specific-formats)
      - [datadog\_json](#datadog_json)
      - [splunk\_hec](#splunk_hec)
      - [elastic\_bulk](#elastic_bulk)
      - [grafana\_loki](#grafana_loki)
      - [newrelic\_json](#newrelic_json)
      - [opentelemetry](#opentelemetry)
  - [🔐 Authentication Methods](#-authentication-methods)
    - [Bearer Token](#bearer-token)
    - [API Key](#api-key)
    - [Basic Authentication](#basic-authentication)
    - [Custom Headers](#custom-headers)
    - [Message-Level Authentication (ZMQ)](#message-level-authentication-zmq)
    - [No Authentication](#no-authentication)
  - [🎯 Event Filtering](#-event-filtering)
    - [Level-Based Filtering](#level-based-filtering)
    - [Event-Based Filtering](#event-based-filtering)
    - [Hybrid Approach](#hybrid-approach)
  - [📋 Available Events Reference](#-available-events-reference)
    - [Request Ingestion \& Validation](#request-ingestion--validation)
    - [Multi-Modal Content Processing](#multi-modal-content-processing)
    - [Overlord Orchestration](#overlord-orchestration)
    - [Memory \& Context Operations](#memory--context-operations)
    - [Agent Processing](#agent-processing)
    - [Model Operations](#model-operations)
    - [Tool \& MCP Operations](#tool--mcp-operations)
    - [A2A \& Collaboration](#a2a--collaboration)
    - [Response Generation](#response-generation)
    - [Async \& Delivery](#async--delivery)
    - [Error Handling \& Recovery](#error-handling--recovery)
    - [Performance \& Monitoring](#performance--monitoring)
    - [Clarification \& Parameter Collection](#clarification--parameter-collection)
    - [Proactive Clarification \& Modes](#proactive-clarification--modes)
    - [Planning Workflow Detection](#planning-workflow-detection)
    - [Enhanced Tool Processing](#enhanced-tool-processing)
    - [Multilingual \& Detection](#multilingual--detection)
    - [Context \& Information Management](#context--information-management)
    - [Session \& State Management](#session--state-management)
    - [Clarification Performance \& Quality](#clarification-performance--quality)
    - [Wildcard Patterns](#wildcard-patterns)
  - [🏢 Enterprise Deployment Patterns](#-enterprise-deployment-patterns)
    - [Cost Optimization](#cost-optimization)
    - [Security \& Compliance](#security--compliance)
    - [Performance Optimization](#performance-optimization)
    - [Multi-Environment Strategy](#multi-environment-strategy)
  - [🔧 Common Configurations](#-common-configurations)
    - [Development Setup](#development-setup)
    - [Production Setup](#production-setup)
    - [High-Performance Setup](#high-performance-setup)
    - [Multi-Service Integration](#multi-service-integration)
  - [🚨 Troubleshooting](#-troubleshooting)
    - [Common Issues](#common-issues)
      - [Stream Connection Failures](#stream-connection-failures)
      - [Performance Issues](#performance-issues)
      - [Authentication Errors](#authentication-errors)
    - [Debug Configuration](#debug-configuration)
    - [Monitoring Stream Health](#monitoring-stream-health)
  - [🔒 Security Considerations](#-security-considerations)
    - [Secret Management](#secret-management)
    - [Network Security](#network-security)
    - [Data Privacy](#data-privacy)
    - [Access Control](#access-control)
  - [📊 Performance Guidelines](#-performance-guidelines)
    - [Throughput Recommendations](#throughput-recommendations)
    - [Format Performance](#format-performance)
    - [Optimization Tips](#optimization-tips)

## 🚀 Quick Start

### Simple Console Logging
```yaml
logging:
  enabled: true
  streams:
    - transport: "stdout"
      level: "info"
      format: "jsonl"
```

### Multi-Destination Setup
```yaml
logging:
  enabled: true
  streams:
    # Console for development
    - transport: "stdout"
      level: "debug"
      format: "text"

    # File for persistence
    - transport: "file"
      destination: "/var/logs/muxi.log"
      level: "info"
      format: "jsonl"

    # External monitoring
    - transport: "stream"
      destination: "https://logs.company.com/ingest"
      protocol: "http"
      format: "jsonl"
      auth:
        type: "bearer"
        token: "${{ secrets.LOG_TOKEN }}"
```

## 🚚 Transport Types

### stdout Transport
**Use case**: Development, Docker deployments, console monitoring

```yaml
- transport: "stdout"
  level: "info"
  format: "jsonl"  # or "text" for human-readable
  events: ["request.*", "error.*"]
```

**Features:**
- Always available, no configuration needed
- Perfect for Docker/Kubernetes deployments
- Real-time monitoring and debugging
- Can be piped to external log processors

### file Transport
**Use case**: Local persistence, audit trails, backup logging

```yaml
- transport: "file"
  destination: "/var/logs/muxi.log"  # File path (required)
  level: "debug"
  format: "jsonl"
  events: ["*"]  # All events
```

**Features:**
- Local file persistence with automatic rotation
- Perfect for compliance and audit requirements
- High-performance with minimal overhead
- Works offline without external dependencies

**Path Options:**
- Absolute paths: `/var/logs/muxi.log`
- Relative paths: `logs/debug.log` (relative to formation directory)
- Log rotation handled automatically

### stream Transport
**Use case**: External services, monitoring platforms, analytics

```yaml
- transport: "stream"
  destination: "https://logs.company.com/ingest"
  protocol: "http"  # Auto-detected if not specified
  format: "datadog_json"
  auth:
    type: "bearer"
    token: "${{ secrets.LOG_TOKEN }}"
  events: ["request.*", "mcp.*", "error.*"]
```

**Supported Protocols:**
- `http` (HTTP/HTTPS)
- `zmq` (ZeroMQ)
- `kafka` (Apache Kafka)
- More protocols planned

### trail Transport (MUXI-Specific)
**Use case**: MUXI Trail Analytics service

```yaml
- transport: "trail"
  token: "${{ secrets.TRAIL_TOKEN }}"
```

**Features:**
- Pre-configured for MUXI Trail service
- Automatic destination: `tcps://trail.muxi.ai/ingest`
- Automatic format: `msgpack` (high-performance binary)
- Automatic events: All events (`["*"]`)
- Encrypted ZMQ transport with CURVE authentication

## 🌐 Network Protocols

### HTTP/HTTPS
**Best for**: Standard web services, monitoring platforms

```yaml
- transport: "stream"
  destination: "https://logs.company.com/api/v1/logs"
  protocol: "http"  # Auto-detected from https://
  format: "jsonl"
  auth:
    type: "bearer"
    token: "${{ secrets.API_TOKEN }}"
```

**Features:**
- POST requests with JSON payloads
- Standard HTTP status codes and retries
- Wide compatibility with monitoring services
- Built-in compression and batching

**URL Detection:**
- `https://` → http (HTTP POST)
- `http://` → http (HTTP POST)

### ZeroMQ (zmq)
**Best for**: High-performance, low-latency, binary protocols

```yaml
- transport: "stream"
  destination: "tcp://logs.company.com:5555"
  protocol: "zmq"  # Auto-detected from tcp://
  format: "msgpack"  # Perfect for ZMQ
  auth:
    type: "token"  # Message-level authentication
    token: "${{ secrets.ZMQ_TOKEN }}"
```

**Features:**
- Zero-copy operations and minimal latency
- Perfect for high-volume event streams
- Binary protocol with msgpack serialization
- Enterprise-grade with CURVE encryption

**URL Detection:**
- `tcp://` → zmq (TCP transport)
- `ipc://` → zmq (Inter-process communication)
- `tcps://` → zmq + CURVE encryption
- `ipcs://` → zmq + CURVE encryption

**Encryption:**
- `tcps://server:5555` = `tcp://server:5555` + CURVE encryption
- `ipcs://path/socket` = `ipc://path/socket` + CURVE encryption
- Automatic key exchange and authentication

### Kafka
**Best for**: High-throughput event streaming, enterprise message pipelines

```yaml
- transport: "stream"
  destination: "kafka://broker1:9092,broker2:9092"
  protocol: "kafka"
  format: "jsonl"  # or msgpack for performance
  topic: "application-logs"
  auth:
    type: "sasl"
    username: "${{ secrets.KAFKA_USER }}"
    password: "${{ secrets.KAFKA_PASS }}"
```

**Features:**
- High-throughput distributed streaming
- Built-in persistence and replay capabilities
- Multiple consumer support for fanout patterns
- Enterprise-grade with SASL/SSL security

**URL Detection:**
- `kafka://` → kafka (Kafka protocol)

**Configuration Options:**
- `topic`: Kafka topic name (required)
- `partition`: Specific partition (optional, auto-assigned if not specified)
- Multiple brokers supported via comma-separated list

## 📄 Data Formats

### Standard Formats

#### jsonl (JSON Lines)
**Use case**: Standard structured logging, easy parsing

```yaml
format: "jsonl"
```

**Output Example:**
```json
{"id":"evt_ABC123","timestamp":1699123456789,"level":"info","event":"request.received","request":{"id":"req_XYZ","user_id":"user_123"},"data":{"message_length":150}}
{"id":"evt_DEF456","timestamp":1699123456890,"level":"info","event":"mcp.tool.called","request":{"id":"req_XYZ"},"data":{"tool_name":"get_weather","server_id":"weather-api"}}
```

#### text (Human-Readable)
**Use case**: Development, console monitoring, debugging

```yaml
format: "text"
```

**Output Example:**
```
2024-01-15 10:15:22 | INFO | request.received | req_XYZ | User message received (150 chars)
2024-01-15 10:15:23 | INFO | mcp.tool.called | req_XYZ | Called weather tool: get_weather
```

#### msgpack (Binary)
**Use case**: High-performance, bandwidth optimization

```yaml
format: "msgpack"
```

**Features:**
- ~50% smaller than JSON
- 3-5x faster serialization
- Perfect for ZMQ and high-volume streams
- Binary format (not human-readable)

### Service-Specific Formats

#### datadog_json
**Use case**: Datadog integration

```yaml
format: "datadog_json"
```

**Output Example:**
```json
{
  "ddsource": "muxi",
  "ddtags": "env:prod,service:formation,version:1.0.0",
  "timestamp": "2024-01-15T10:15:22Z",
  "level": "info",
  "message": "User message received",
  "service": "muxi-runtime",
  "muxi_event": "request.received",
  "request_id": "req_XYZ"
}
```

#### splunk_hec
**Use case**: Splunk HTTP Event Collector

```yaml
format: "splunk_hec"
```

**Output Example:**
```json
{
  "time": 1699123456.789,
  "index": "main",
  "source": "muxi",
  "sourcetype": "muxi:events",
  "event": {
    "level": "info",
    "muxi_event": "request.received",
    "request_id": "req_XYZ",
    "message": "User message received"
  }
}
```

#### elastic_bulk
**Use case**: Elasticsearch Bulk API

```yaml
format: "elastic_bulk"
```

**Output Example:**
```json
{"index": {"_index": "muxi-logs", "_type": "_doc"}}
{"@timestamp": "2024-01-15T10:15:22Z", "level": "info", "muxi_event": "request.received", "request_id": "req_XYZ", "message": "User message received"}
```

#### grafana_loki
**Use case**: Grafana Loki LogQL-compatible logs

```yaml
format: "grafana_loki"
```

**Output Example:**
```json
{
  "streams": [
    {
      "stream": {
        "service": "muxi-runtime",
        "level": "info",
        "formation_id": "customer-support"
      },
      "values": [
        ["1699123456789000000", "{\"muxi_event\": \"request.received\", \"request_id\": \"req_XYZ\", \"message\": \"User message received\"}"]
      ]
    }
  ]
}
```

#### newrelic_json
**Use case**: New Relic Logs API

```yaml
format: "newrelic_json"
```

**Output Example:**
```json
{
  "timestamp": 1699123456789,
  "level": "info",
  "message": "User message received",
  "service.name": "muxi-runtime",
  "muxi.event": "request.received",
  "muxi.request.id": "req_XYZ",
  "muxi.formation.id": "customer-support",
  "attributes": {
    "user_id": "user_123",
    "message_length": 150
  }
}
```

#### opentelemetry
**Use case**: OpenTelemetry OTLP logs format

```yaml
format: "opentelemetry"
```

**Output Example:**
```json
{
  "resourceLogs": [
    {
      "resource": {
        "attributes": [
          {"key": "service.name", "value": {"stringValue": "muxi-runtime"}},
          {"key": "service.version", "value": {"stringValue": "1.0.0"}}
        ]
      },
      "instrumentationLibraryLogs": [
        {
          "instrumentationLibrary": {
            "name": "muxi.observability",
            "version": "1.0.0"
          },
          "logs": [
            {
              "timeUnixNano": "1699123456789000000",
              "severityNumber": 9,
              "severityText": "info",
              "body": {"stringValue": "User message received"},
              "attributes": [
                {"key": "muxi.event", "value": {"stringValue": "request.received"}},
                {"key": "muxi.request.id", "value": {"stringValue": "req_XYZ"}}
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## 🔐 Authentication Methods

### Bearer Token
**Use case**: OAuth 2.0, API tokens, modern REST APIs

```yaml
auth:
  type: "bearer"
  token: "${{ secrets.API_TOKEN }}"
```

**HTTP Header:** `Authorization: Bearer <token>`

### API Key
**Use case**: Custom header authentication, legacy APIs

```yaml
auth:
  type: "api_key"
  header: "X-API-Key"  # Custom header name (default: "Authorization")
  key: "${{ secrets.API_KEY }}"
```

**HTTP Header:** `X-API-Key: <key>`

### Basic Authentication
**Use case**: Legacy systems, simple authentication

```yaml
auth:
  type: "basic"
  username: "${{ secrets.LOG_USERNAME }}"
  password: "${{ secrets.LOG_PASSWORD }}"
```

**HTTP Header:** `Authorization: Basic <base64(username:password)>`

### Custom Headers
**Use case**: Complex authentication, multiple headers

```yaml
auth:
  type: "custom"
  headers:
    Authorization: "Custom ${{ secrets.CUSTOM_TOKEN }}"
    X-Client-ID: "${{ secrets.CLIENT_ID }}"
    X-Tenant: "${{ secrets.TENANT_ID }}"
```

### Message-Level Authentication (ZMQ)
**Use case**: ZeroMQ streams, binary protocols

```yaml
auth:
  type: "token"
  token: "${{ secrets.ZMQ_TOKEN }}"
```

**Implementation:** Token embedded in message payload before transmission

### No Authentication
**Use case**: Internal networks, development

```yaml
auth:
  type: "none"
```

## 🎯 Event Filtering

### Level-Based Filtering
**Simple approach**: Filter by minimum log level

```yaml
level: "info"  # Includes: error, warn, info (excludes: debug)
```

**Level Hierarchy:** `error` > `warn` > `info` > `debug`

**Predefined Event Levels:**
- `request.received` → INFO
- `agent.thinking.started` → DEBUG
- `error.timeout.detected` → WARN
- `mcp.tool.failed` → ERROR

### Event-Based Filtering
**Precise control**: Specify exact events to capture

```yaml
events:
  - "request.received"
  - "response.delivered"
  - "error.*"           # Wildcard for all errors
  - "mcp.tool.*"        # All MCP tool events
```

### Hybrid Approach
**Logic**: If `events` is specified, `level` is ignored

```yaml
# This configuration:
level: "debug"
events: ["error.*", "request.*"]

# Only captures error.* and request.* events (ignores level)
```

## 📋 Available Events Reference

### Request Ingestion & Validation
*Events related to initial request processing, authentication, rate limiting, and validation*

| Event | Level | Description |
|-------|-------|-------------|
| `request.received` | INFO | Request initially received by MUXI |
| `request.denied.auth` | WARN | Request denied due to authentication failure |
| `request.denied.rate_limit` | WARN | Request denied due to rate limiting |
| `request.denied.validation` | WARN | Request denied due to validation failure |
| `request.validated` | DEBUG | Request format and structure validation passed |

### Multi-Modal Content Processing
*Events for processing documents, images, audio, and other media content types*

| Event | Level | Description |
|-------|-------|-------------|
| `content.document.parsed` | INFO | Document attachment processing |
| `content.image.analyzed` | INFO | Image analysis and vision processing |
| `content.audio.transcribed` | INFO | Audio transcription |
| `content.extraction.failed` | ERROR | Content processing failure |

### Overlord Orchestration
*Events tracking the overlord's routing decisions, task decomposition, and orchestration activities*

| Event | Level | Description |
|-------|-------|-------------|
| `overlord.initialized` | DEBUG | Overlord component startup |
| `overlord.routing.started` | DEBUG | Begin routing decision process |
| `overlord.routing.completed` | INFO | Routing decision made |
| `overlord.task.decomposed` | INFO | Request broken into subtasks |

### Memory & Context Operations
*Events for memory storage, retrieval, and context management across short-term and long-term memory systems*

| Event | Level | Description |
|-------|-------|-------------|
| `memory.retrieval.started` | DEBUG | Memory search initiated |
| `memory.retrieval.short_term` | DEBUG | Short-term buffer search |
| `memory.retrieval.long_term` | DEBUG | Long-term memory search |
| `memory.retrieval.context` | DEBUG | User context memory lookup |
| `memory.storage.short_term` | DEBUG | Buffer memory storage |
| `memory.storage.long_term` | DEBUG | Persistent memory storage |
| `memory.extraction.started` | INFO | Automatic user info extraction |

### Agent Processing
*Events tracking individual agent activities including reasoning, planning, and context application*

| Event | Level | Description |
|-------|-------|-------------|
| `agent.selected` | INFO | Specific agent chosen for processing |
| `agent.thinking.started` | DEBUG | Agent reasoning process begins |
| `agent.thinking.completed` | INFO | Agent reasoning finished |
| `agent.planning.created` | INFO | Agent generates execution plan |
| `agent.context.applied` | DEBUG | System message/persona applied |

### Model Operations
*Events for LLM API calls, inference operations, and streaming response handling*

| Event | Level | Description |
|-------|-------|-------------|
| `model.inference.started` | DEBUG | Model API call initiated |
| `model.inference.completed` | INFO | Model response received |
| `model.streaming.started` | DEBUG | Streaming response initiated |

### Tool & MCP Operations
*Events for MCP server connections, tool discovery, execution, and error handling*

| Event | Level | Description |
|-------|-------|-------------|
| `mcp.connection.established` | DEBUG | MCP server connection |
| `mcp.tool.discovered` | DEBUG | Available tools identified |
| `mcp.tool.called` | INFO | Tool execution initiated |
| `mcp.tool.completed` | INFO | Tool execution finished |
| `mcp.tool.failed` | ERROR | Tool execution error |

### A2A & Collaboration
*Events for agent-to-agent communication, external agent discovery, and multi-agent collaboration*

| Event | Level | Description |
|-------|-------|-------------|
| `a2a.discovery.started` | DEBUG | External agent discovery |
| `a2a.request.sent` | INFO | A2A request to external agent |
| `a2a.response.received` | INFO | A2A response received |
| `collaboration.internal.started` | INFO | Internal multi-agent collaboration |

### Response Generation
*Events for response composition, multi-modal content creation, validation, and formatting*

| Event | Level | Description |
|-------|-------|-------------|
| `response.generation.started` | DEBUG | Begin response composition |
| `response.multimodal.created` | INFO | Multi-modal response generated |
| `response.validation.completed` | DEBUG | Response safety/validation check |
| `response.formatted` | DEBUG | Final response formatting |

### Async & Delivery
*Events for asynchronous processing, webhook delivery, and response completion tracking*

| Event | Level | Description |
|-------|-------|-------------|
| `async.threshold.detected` | INFO | Request exceeds sync threshold |
| `async.processing.started` | INFO | Background processing initiated |
| `webhook.sent` | INFO | Webhook delivery attempted |
| `response.delivered` | INFO | Final response sent to user |

### Error Handling & Recovery
*Events for error detection, retry mechanisms, fallback activation, and recovery completion*

| Event | Level | Description |
|-------|-------|-------------|
| `error.timeout.detected` | WARN | Operation timeout |
| `error.retry.attempted` | WARN | Retry mechanism triggered |
| `error.fallback.activated` | WARN | Fallback mechanism used |
| `error.recovery.completed` | INFO | Error recovery successful |

### Performance & Monitoring
*Events for performance metrics, resource usage tracking, and session management*

| Event | Level | Description |
|-------|-------|-------------|
| `performance.duration.recorded` | DEBUG | Component performance metric |
| `resource.usage.measured` | DEBUG | Resource consumption tracking |
| `session.created` | INFO | User session established |
| `session.context.updated` | DEBUG | Session context modified |

### Clarification & Parameter Collection
*Events for intelligent parameter collection, clarifying questions, and missing parameter detection*

| Event | Level | Description |
|-------|-------|-------------|
| `clarification.analysis.started` | DEBUG | Information requirement analysis initiated |
| `clarification.analysis.completed` | INFO | Missing parameters/information identified |
| `clarification.question.generated` | INFO | Clarifying question created for user |
| `clarification.response.parsed` | DEBUG | User clarification response processed |
| `clarification.parameter.enriched` | DEBUG | Parameter filled from user context |
| `clarification.parameter.validated` | DEBUG | Parameter validation completed |
| `clarification.failed` | WARN | Clarification process failed, falling back |

### Proactive Clarification & Modes
*Events for proactive clarification sessions, user-requested questioning, and mode management*

| Event | Level | Description |
|-------|-------|-------------|
| `clarification.proactive.detected` | INFO | Explicit turn-taking request detected |
| `clarification.mode.started` | INFO | Proactive clarification session initiated |
| `clarification.mode.questioning` | DEBUG | Proactive questioning mode active |
| `clarification.mode.planning` | DEBUG | Plan analysis mode active |
| `clarification.mode.context_building` | DEBUG | Context building mode active |
| `clarification.mode.goal_achievement` | DEBUG | Goal achievement mode active |
| `clarification.session.completed` | INFO | Proactive session reached completion criteria |
| `clarification.session.cancelled` | INFO | User cancelled proactive session |

### Planning Workflow Detection
*Events for implicit planning workflow identification, data synthesis, and continuation*

| Event | Level | Description |
|-------|-------|-------------|
| `planning.workflow.detected` | INFO | Implicit planning workflow identified |
| `planning.data.synthesized` | INFO | Tool results synthesized for decision-making |
| `planning.continuation.started` | INFO | Planning continuation after data gathering |
| `planning.step.analyzed` | DEBUG | Individual plan step feasibility assessed |
| `planning.dependencies.identified` | DEBUG | Plan step dependencies mapped |
| `planning.options.presented` | INFO | Decision options generated for user |

### Enhanced Tool Processing
*Events for tool parameter collection, validation, and context-enhanced execution*

| Event | Level | Description |
|-------|-------|-------------|
| `tool.parameter.missing` | INFO | Missing required tool parameters identified |
| `tool.parameter.clarified` | INFO | Tool parameter obtained via clarification |
| `tool.validation.failed` | WARN | Tool parameter validation failed |
| `tool.execution.enhanced` | DEBUG | Tool executed with enhanced parameter processing |
| `tool.context.applied` | DEBUG | User context applied to tool parameters |

### Multilingual & Detection
*Events for language detection, multilingual processing, and pattern recognition*

| Event | Level | Description |
|-------|-------|-------------|
| `language.detection.started` | DEBUG | LLM-based language detection initiated |
| `language.detection.completed` | DEBUG | Input language identified |
| `language.processing.multilingual` | DEBUG | Multilingual processing mode activated |
| `language.fallback.activated` | WARN | Fallback to regex patterns (if applicable) |
| `intent.proactive.detected` | INFO | Proactive clarification intent identified |
| `intent.planning.detected` | INFO | Planning workflow intent identified |
| `intent.goal.extracted` | DEBUG | User goal extracted from natural language |
| `pattern.llm.analysis` | DEBUG | LLM-based pattern analysis completed |
| `pattern.detection.failed` | WARN | Pattern detection failed, using fallback |

### Context & Information Management
*Events for information requirements analysis, gap identification, and context management*

| Event | Level | Description |
|-------|-------|-------------|
| `info.requirements.analyzed` | DEBUG | Information requirements determined |
| `info.gaps.identified` | INFO | Information gaps found in user request |
| `info.confidence.scored` | DEBUG | Information confidence level calculated |
| `info.extraction.automated` | DEBUG | Automatic information extraction attempted |
| `info.context.insufficient` | WARN | Insufficient context for parameter filling |
| `goal.type.determined` | DEBUG | Goal type classification completed |
| `goal.progress.tracked` | DEBUG | Progress toward goal completion measured |
| `goal.completion.criteria` | DEBUG | Goal completion criteria evaluated |
| `goal.context.created` | INFO | Goal context established for session |
| `goal.achievement.measured` | DEBUG | Goal achievement percentage calculated |

### Session & State Management
*Events for clarification session lifecycle, state management, and mode transitions*

| Event | Level | Description |
|-------|-------|-------------|
| `session.clarification.created` | INFO | New clarification session established |
| `session.clarification.updated` | DEBUG | Session state updated with new information |
| `session.clarification.cleaned` | DEBUG | Session cleanup and resource release |
| `session.mode.switched` | INFO | Clarification mode changed within session |
| `session.progress.checkpoint` | DEBUG | Session progress checkpoint reached |
| `conversation.turn.clarification` | DEBUG | Clarification turn in multi-turn conversation |
| `conversation.context.maintained` | DEBUG | Context preserved across clarification turns |
| `conversation.flow.interrupted` | WARN | Normal conversation flow interrupted for clarification |
| `conversation.flow.resumed` | INFO | Normal conversation flow resumed after clarification |

### Clarification Performance & Quality
*Events for performance metrics, quality tracking, and system health monitoring*

| Event | Level | Description |
|-------|-------|-------------|
| `performance.clarification.duration` | DEBUG | Time spent in clarification process |
| `performance.question.generation` | DEBUG | Question generation latency measured |
| `performance.llm.detection` | DEBUG | LLM-based detection performance |
| `quality.parameter.completion` | INFO | Parameter completion rate measured |
| `quality.clarification.success` | INFO | Clarification success rate tracked |
| `health.clarification.enabled` | INFO | Clarification system initialized successfully |
| `health.clarification.disabled` | WARN | Clarification system disabled/failed |
| `health.mode.manager.active` | DEBUG | Mode manager health check passed |
| `health.session.cleanup.completed` | DEBUG | Session cleanup completed successfully |

### Wildcard Patterns
*Convenient pattern matching for event filtering and monitoring*

| Pattern | Description |
|---------|-------------|
| `request.*` | All request-related events |
| `error.*` | All error events |
| `mcp.*` | All MCP/tool-related events |
| `agent.*` | All agent processing events |
| `memory.*` | All memory operation events |
| `response.*` | All response generation events |
| `a2a.*` | All agent-to-agent communication events |
| `performance.*` | All performance monitoring events |
| `clarification.*` | All clarification-related events |
| `planning.*` | All planning workflow events |
| `session.clarification.*` | All clarification session events |
| `tool.parameter.*` | All tool parameter collection events |
| `intent.*` | All intent detection events |
| `goal.*` | All goal tracking and achievement events |
| `info.*` | All information analysis and management events |
| `language.*` | All multilingual processing events |
| `performance.clarification.*` | All clarification performance events |
| `quality.*` | All quality metrics and success rates |
| `health.*` | All system health monitoring events |
| `conversation.*` | All conversation flow and context events |
| `*` | All events (use with caution) |

> [!TIP]
> **Event Selection Strategies:**
> - **Development**: `["*"]` or `level: "debug"` for full visibility
> - **Production Monitoring**: `["request.*", "response.*", "error.*"]` for main flow + errors
> - **Performance Analysis**: `["performance.*", "resource.*", "model.inference.*"]`
> - **Debugging Issues**: `["error.*", "*.failed", "*.timeout.*"]`
> - **Security Auditing**: `["request.denied.*", "auth.*", "security.*"]`
> - **Clarification Quality**: `["clarification.*", "planning.*", "quality.*"]` for parameter collection effectiveness
> - **User Experience**: `["conversation.*", "session.clarification.*", "intent.*"]` for interaction flow analysis
> - **Multilingual Support**: `["language.*", "intent.*", "pattern.*"]` for international deployment monitoring

## 🏢 Enterprise Deployment Patterns

### Cost Optimization
**Send expensive events to cheap storage, summaries to expensive services**

```yaml
logging:
  enabled: true
  streams:
    # Full debug locally (cheap)
    - transport: "file"
      destination: "/var/logs/full-debug.log"
      level: "debug"
      format: "jsonl"

    # Only errors to expensive SaaS (cost control)
    - transport: "stream"
      destination: "https://expensive-monitoring.com/api/logs"
      protocol: "webhook"
      level: "error"
      format: "datadog_json"
      auth:
        type: "bearer"
        token: "${{ secrets.EXPENSIVE_SERVICE_TOKEN }}"
```

### Security & Compliance
**Send sensitive data internally, sanitized data externally**

```yaml
logging:
  enabled: true
  streams:
    # Full data for internal compliance
    - transport: "file"
      destination: "/secure/logs/audit.log"
      events: ["*"]
      format: "jsonl"

    # Sanitized data for external monitoring
    - transport: "stream"
      destination: "https://external-monitoring.com"
      events: ["request.received", "response.delivered", "performance.*"]
      format: "jsonl"
      auth:
        type: "bearer"
        token: "${{ secrets.EXTERNAL_TOKEN }}"
```

### Performance Optimization
**High-volume events to binary protocol, alerts to HTTP**

```yaml
logging:
  enabled: true
  streams:
    # High-volume metrics via binary protocol
    - transport: "stream"
      destination: "tcp://metrics.company.com:5555"
      protocol: "zmq"
      format: "msgpack"
      events: ["performance.*", "resource.*"]
      auth:
        type: "token"
        token: "${{ secrets.METRICS_TOKEN }}"

    # Critical alerts via HTTP
    - transport: "stream"
      destination: "https://alerts.company.com/webhook"
      protocol: "http"
      format: "jsonl"
      events: ["error.*", "timeout.*"]
      auth:
        type: "bearer"
        token: "${{ secrets.ALERTS_TOKEN }}"
```

### Multi-Environment Strategy
**Different configurations per environment**

```yaml
# production.yaml
logging:
  enabled: true
  streams:
    - transport: "stream"
      destination: "https://prod-logs.company.com"
      level: "warn"  # Only warnings and errors in prod

# development.yaml
logging:
  enabled: true
  streams:
    - transport: "stdout"
      level: "debug"  # Full debug in development
      format: "text"
```

## 🔧 Common Configurations

### Development Setup
```yaml
logging:
  enabled: true
  streams:
    - transport: "stdout"
      level: "debug"
      format: "text"
```

### Production Setup
```yaml
logging:
  enabled: true
  streams:
    # Console for Docker/K8s
    - transport: "stdout"
      level: "info"
      format: "jsonl"

    # Local backup
    - transport: "file"
      destination: "/var/logs/muxi.log"
      level: "warn"
      format: "jsonl"

    # External monitoring
    - transport: "stream"
      destination: "https://logs.company.com/ingest"
      protocol: "http"
      format: "datadog_json"
      auth:
        type: "bearer"
        token: "${{ secrets.DATADOG_API_KEY }}"
```

### High-Performance Setup
```yaml
logging:
  enabled: true
  streams:
    # Ultra-fast binary logging
    - transport: "stream"
      destination: "tcps://high-perf-logs.company.com:5555"
      protocol: "zmq"
      format: "msgpack"
      events: ["*"]
      auth:
        type: "token"
        token: "${{ secrets.ZMQ_TOKEN }}"
```

### Multi-Service Integration
```yaml
logging:
  enabled: true
  streams:
    # Datadog for APM
    - transport: "stream"
      destination: "https://http-intake.logs.datadoghq.com/v1/input/${{ secrets.DATADOG_API_KEY }}"
      format: "datadog_json"
      events: ["request.*", "response.*", "performance.*"]

    # Splunk for security
    - transport: "stream"
      destination: "https://splunk.company.com:8088/services/collector"
      format: "splunk_hec"
      events: ["error.*", "auth.*", "security.*"]
      auth:
        type: "bearer"
        token: "${{ secrets.SPLUNK_TOKEN }}"

    # Elasticsearch for search
    - transport: "stream"
      destination: "https://elasticsearch.company.com/_bulk"
      format: "elastic_bulk"
      events: ["*"]
      auth:
        type: "basic"
        username: "${{ secrets.ELASTIC_USER }}"
        password: "${{ secrets.ELASTIC_PASS }}"

    # Grafana Loki for open-source
    - transport: "stream"
      destination: "https://logs-prod-us-central1.grafana.net/loki/api/v1/push"
      format: "grafana_loki"
      events: ["request.*", "error.*", "agent.*"]
      auth:
        type: "basic"
        username: "${{ secrets.GRAFANA_USER }}"
        password: "${{ secrets.GRAFANA_API_KEY }}"

    # New Relic for full-stack observability
    - transport: "stream"
      destination: "https://log-api.newrelic.com/log/v1"
      format: "newrelic_json"
      events: ["request.*", "response.*", "mcp.*", "error.*"]
      auth:
        type: "api_key"
        header: "X-License-Key"
        key: "${{ secrets.NEWRELIC_LICENSE_KEY }}"

    # OpenTelemetry compatible backend
    - transport: "stream"
      destination: "https://otlp.company.com/v1/logs"
      format: "opentelemetry"
      events: ["*"]
      auth:
        type: "bearer"
        token: "${{ secrets.OTLP_TOKEN }}"
```

## 🚨 Troubleshooting

### Common Issues

#### Stream Connection Failures
**Symptoms:** Events not appearing in external service
**Solutions:**
1. Verify destination URL and credentials
2. Check network connectivity and firewall rules
3. Enable debug logging to see connection attempts
4. Test authentication with curl/manual requests

#### Performance Issues
**Symptoms:** High latency, memory usage, or CPU load
**Solutions:**
1. Use binary formats (`msgpack`) for high-volume streams
2. Implement event filtering to reduce volume
3. Consider ZMQ protocol for performance-critical streams
4. Batch events for HTTP endpoints

#### Authentication Errors
**Symptoms:** 401/403 errors, authentication failures
**Solutions:**
1. Verify secret values are correctly set
2. Check token expiration and renewal
3. Ensure correct authentication type for service
4. Test credentials outside MUXI first

### Debug Configuration
```yaml
logging:
  enabled: true
  streams:
    # Enable all events for debugging
    - transport: "stdout"
      level: "debug"
      format: "text"
      events: ["*"]

    # Log to file for analysis
    - transport: "file"
      destination: "/tmp/debug.log"
      level: "debug"
      format: "jsonl"
      events: ["*"]
```

### Monitoring Stream Health
Each stream reports its own health and statistics:
- Connection status
- Message success/failure rates
- Authentication status
- Performance metrics

## 🔒 Security Considerations

### Secret Management
- Always use `${{ secrets.NAME }}` syntax for sensitive values
- Never commit actual credentials to version control
- Rotate credentials regularly
- Use least-privilege principles for API keys

### Network Security
- Use encrypted transports (HTTPS, WSS, tcps://)
- Implement proper firewall rules
- Consider VPN/private networks for sensitive data
- Validate SSL/TLS certificates

### Data Privacy
- Filter sensitive events before external transmission
- Use different streams for different data sensitivity levels
- Implement data retention policies
- Consider GDPR/compliance requirements

### Access Control
- Restrict formation configuration to authorized users
- Use separate credentials per environment
- Monitor credential usage and access patterns
- Implement credential rotation procedures

## 📊 Performance Guidelines

### Throughput Recommendations
- **stdout/file**: >100K events/second
- **HTTP webhook**: 1K-10K events/second (depending on batching)
- **ZMQ + msgpack**: >50K events/second
- **WebSocket**: 5K-20K events/second

### Format Performance
1. **msgpack**: Fastest serialization, smallest size
2. **jsonl**: Good performance, human-readable
3. **text**: Fastest for development, not structured
4. **Service formats**: Optimized for specific platforms

### Optimization Tips
- Use event filtering to reduce volume
- Choose binary formats for high-throughput streams
- Enable compression for HTTP streams
- Consider batching for network protocols
- Monitor memory usage with multiple streams

---

This comprehensive guide covers all aspects of MUXI's logging system. For schema field reference, see [`SCHEMA_GUIDE.md`](./SCHEMA_GUIDE.md).
