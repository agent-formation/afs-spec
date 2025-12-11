# Agent Formation: Logging Configuration Guide

## 📋 Overview

Agent Formation's observability system provides enterprise-grade logging with multi-destination streams, per-destination configuration, and flexible event routing. This guide covers all configuration options, deployment patterns, and best practices.

**Key Principles:**
- **Dual Architecture**: Runtime events (always stdout) + Observability events (configurable streams)
- **Zero Storage**: Runtimes capture and emit events but don't store them
- **Multi-Destination**: Send different events to different outputs simultaneously
- **Per-Stream Config**: Each destination has independent level, format, events, and auth

> [!NOTE]
> **File Extensions**: Agent Formation supports both `.afs` (Agent Formation Schema) and `.yaml` extensions. Examples in this guide use `.afs` but `.yaml` works identically.

## 📚 Table of Contents

- [📋 Overview](#-overview)
- [📚 Table of Contents](#-table-of-contents)
- [🚀 Quick Start](#-quick-start)
	- [Simple Console Logging](#simple-console-logging)
	- [Multi-Destination Setup](#multi-destination-setup)
- [🚚 Transport Types](#-transport-types)
	- [stdout Transport](#stdout-transport)
	- [file Transport](#file-transport)
	- [stream Transport](#stream-transport)
- [🌐 Network Protocols](#-network-protocols)
	- [HTTP/HTTPS](#httphttps)
	- [ZeroMQ (zmq)](#zeromq-zmq)
- [📄 Data Formats](#-data-formats)
- [🔐 Authentication Methods](#-authentication-methods)
- [🎯 Event Filtering](#-event-filtering)
- [🏢 Enterprise Deployment Patterns](#-enterprise-deployment-patterns)
- [🔧 Common Configurations](#-common-configurations)
- [🚨 Troubleshooting](#-troubleshooting)
- [🔒 Security Considerations](#-security-considerations)
- [📊 Performance Guidelines](#-performance-guidelines)

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
      destination: "/var/logs/formation.log"
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
  destination: "/var/logs/formation.log"  # File path (required)
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
- Absolute paths: `/var/logs/formation.log`
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

## 📄 Data Formats

### Standard Formats

| Format | Description |
|--------|-------------|
| `jsonl` | JSON Lines — human-readable, structured |
| `text` | Plain text — development, debugging |
| `msgpack` | Binary — fastest serialization, smallest size |

### Service-Specific Formats

| Format | Service |
|--------|---------|
| `datadog_json` | Datadog |
| `splunk_hec` | Splunk HTTP Event Collector |
| `elastic_bulk` | Elasticsearch |
| `grafana_loki` | Grafana Loki |
| `newrelic_json` | New Relic |
| `opentelemetry` | OpenTelemetry compatible backends |

## 🔐 Authentication Methods

| Type | Description |
|------|-------------|
| `bearer` | `Authorization: Bearer {token}` header |
| `api_key` | `{header}: {key}` header (configurable) |
| `basic` | `Authorization: Basic {base64(user:pass)}` |
| `custom` | Custom headers exactly as configured |
| `none` | No authentication |

## 🎯 Event Filtering

### Level-Based Filtering
```yaml
- transport: "stdout"
  level: "warn"  # Only warnings and above
```

### Event-Based Filtering
```yaml
- transport: "stream"
  events: ["request.*", "error.*", "mcp.*"]
```

### Wildcard Patterns
- `*` — All events
- `request.*` — All request events
- `error.*` — All error events
- `mcp.*` — All MCP tool events

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
      destination: "/var/logs/formation.log"
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
4. Test credentials outside the runtime first

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

This comprehensive guide covers all aspects of Agent Formation's logging system. For schema field reference, see [`SCHEMA_GUIDE.md`](./SCHEMA_GUIDE.md).
