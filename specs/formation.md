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
- Standard operating procedures (SOPs) and inbound triggers
- Outbound payload transformers and proactive messaging channels
- Access control groups
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

#### 2.1.1 Overlord soul (`SOUL.md`)

The overlord's persona (identity, tone, values) comes from a **soul document**, auto-discovered by fixed filename next to the formation file. Runtimes **must** resolve the soul in this precedence order:

1. `SOUL.md` next to the formation file
2. `soul.md` next to the formation file
3. the inline `overlord.soul` field in the formation file
4. the runtime's built-in default persona

The first source found wins; the rest are ignored. The document's content is used verbatim (no templating). Soul is overlord-only — individual agents do not accept a soul document (see §2.2).

### 2.2 Agents
Agents are declared under `agents/` and referenced by the Formation.

Each agent includes:
- identity and role
- goals / responsibilities
- tool access
- memory bindings
- overrides

Agents are single-file contained: an agent's character and persona live in its `system_message`. There is no per-agent soul document — soul is an overlord-level concept only (see §2.1.1).

### 2.3 MCP tool servers
MCP servers provide tools to agents.

They may be:
- local command-based
- remote HTTP-based
- hosted elsewhere

Each server supports an optional `parameters` field: a flat key-value map of default values injected into every tool call. This is intended for infrastructure constants (org-level IDs, tenant keys) that should never be left to LLM inference. Values support `${{ secrets.X }}` interpolation. Caller-provided values always take precedence.

Each server also supports an optional `tools` block (`allow` and/or `deny`; `whitelist`/`blacklist` are accepted aliases) that scopes the upstream tool catalog at registration time. `allow` alone keeps only matching tools; `deny` alone keeps everything except matching tools; both together apply allow first and then subtract deny (deny wins on overlap). Patterns are POSIX `fnmatch` globs (`*`, `?`, `[...]`); names without metacharacters match literally. This narrows the per-turn planning prompt to the tools the formation actually uses and lets operators keep destructive verbs out of the LLM's plannable surface entirely.

**Registry is not grant.** The formation-level `mcp.servers` list defines connections and prunes tool catalogs; capability flows to an agent only via that agent's `mcp_servers` attachment. Declaring a server at the formation level does not by itself put its tools on any agent's surface.

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

Runtimes may ship built-in skills that load automatically. The formation-level `skills:` field accepts either a plain list of skill names, or a mapping form that additionally disables named built-ins:

```yaml
skills:
  names: [pdf-processing, data-analysis]
  disable_builtin: [compute]
```

A skill's `SKILL.md` frontmatter may carry a `model:` reference (alias or `provider/model`) participating in the model selection hierarchy (§4.1).

### 2.6 SOPs (standard operating procedures)

SOPs are reusable, named procedures stored as markdown files under `sops/`. They are **auto-discovered** (see §3): every markdown file in `sops/` (recursively) whose frontmatter declares `type: sop` is loaded as an SOP; its id is the filename stem.

Frontmatter:

| Key | Required | Default | Meaning |
|-----|----------|---------|---------|
| `type` | yes | — | Literal `sop`; activates SOP parsing |
| `name` | no | file stem | Display name |
| `description` | no | — | One-line description (used in command listings) |
| `mode` | no | `template` | `template` (deterministic step parsing) or `guide` (LLM-interpreted) |
| `tags` | no | — | Comma-separated string or list; used for semantic matching |
| `model` | no | — | Default model for all steps: alias or `provider/model` (§4.1) |
| `bypass_approval` | no | `true` | Skip workflow plan approval when this SOP executes |
| `synthesis` | no | `true` | Run a synthesis pass after execution |

The body is markdown. In `template` mode, steps are a numbered list under a `## Steps` heading (or `## Step N: Title` headings). Steps may carry inline directives:

| Directive | Meaning |
|-----------|---------|
| `[agent:name]` | Route the step to the named agent |
| `[skill:name]` / `[skill:name/script]` | Activate a skill (optionally a specific script) |
| `[mcp:server]` / `[mcp:server/action]` | Declare an MCP capability requirement |
| `[model:x]` | Step-level model override — alias or `provider/model`; wins over the SOP frontmatter `model:` (§4.1) |
| `[parallel]` | Remove the sequential dependency on the previous step |
| `[file:path]` | Reference a resource file (resolved at execution time) |

See `schemas/sops/` for the annotated template.

### 2.7 Triggers

Triggers are inbound HTTP entry points stored as markdown files under `triggers/`. They are **auto-discovered** (see §3); the trigger id is the filename stem and **must** match `^[a-zA-Z0-9_-]+$`.

Each trigger is exposed by id at:

```
POST /v1/triggers/{id}
```

authenticated with the formation's client key; the request then traverses the request middleware + RBAC pipeline (§5) like every other route. Runtimes should also expose `GET /v1/triggers` (list) and `GET /v1/triggers/{id}` (metadata).

Frontmatter keys (closed set — unknown keys are a load error):

| Key | Type | Meaning |
|-----|------|---------|
| `name` | string | Optional display-name override |
| `type` | string | Optional type annotation (semantic only) |
| `parse` | mapping | Payload extraction spec (below) |
| `webhook` | string (http(s) URL) | Outbound delivery destination |
| `transformer` | string | Name of a transformer (§2.8) to format the outbound payload |
| `model` | string | Model override for this trigger's turn: alias or `provider/model` (§4.1) |
| `channel` | string | Names the inbound channel for source tracking; feeds proactive "last channel" routing (§6) |

`parse:` extracts fields from the inbound POST payload. Allowed keys: `message`, `user_id`, `files` (each a JSONPath string such as `$.event.text`) and `context` (a mapping of name → JSONPath for platform-specific values, e.g. `channel: $.event.channel`). Extraction is best-effort; a missing path yields no value rather than an error.

The body (after the frontmatter) is a markdown instruction template. `${{ data.* }}` placeholders reference the inbound POST payload.

**Outbound composition — `webhook:` and `transformer:` compose; they are not mutually exclusive:**

| Present | Behavior |
|---------|----------|
| `webhook:` only | The raw standard payload is delivered to the webhook URL |
| `transformer:` only | The transformer formats the payload and delivers it to the transformer's own `endpoint.url` |
| both | The transformer formats the payload; the trigger's `webhook:` URL is the delivery destination (trigger URL wins) |

A trigger that references a transformer where neither the trigger's `webhook:` nor the transformer's `endpoint.url` provides a destination **must** fail at formation load.

See `schemas/triggers/` for the annotated template.

### 2.8 Transformers

Transformers are outbound payload formatters stored as YAML files under `transformers/`. They turn a response into the JSON shape a delivery target expects (a Slack webhook, a Telegram bot bridge, an email bridge, ...), and are referenced by name from trigger frontmatter (§2.7) and proactive channels (§6).

File format (the `name` field is required and must match the filename stem):

| Key | Required | Meaning |
|-----|----------|---------|
| `name` | yes | Transformer id; must match the filename |
| `endpoint.url` | no | Delivery URL (supports `${{ secrets.* }}`); omitted for payload-format-only templates |
| `endpoint.method` | no | `GET`/`POST`/`PUT`/`PATCH`/`DELETE`; default `POST` |
| `auth` | no | `type: bearer` (`token`), `basic` (`username`/`password`), or `header` (`header_name`/`header_value`) |
| `headers` | no | Custom HTTP headers |
| `body` | no | Request-body template with `${{ ... }}` placeholders |
| `content_transform` | no | `format` (`text` strips markdown, `markdown` passthrough, `html` renders), `max_length`, `truncation_suffix` |
| `version` | no | Version annotation (semantic only) |

Template variables available in `body`/`headers`: `response.content`, `response.files`, `response.metadata`, `request.message`, `request.user_id`, `request.files`, `context.*` (from the trigger's `parse.context`), `agent.name`, `secrets.*`, `timestamp`. A value that is exactly one placeholder resolves natively (lists/objects stay unquoted); otherwise placeholders substitute as strings.

**Bundled channel templates.** Runtimes ship dormant, payload-format-only templates named `slack`, `telegram`, `discord`, and `email` (no `endpoint`; the referencing trigger or proactive channel supplies the URL). A formation-local `transformers/<name>.yaml` **shadows** a bundled template of the same name — the same shadowing rule as built-in skills.

See `schemas/transformers/` for the annotated template.

---

## 3. Component declaration and discovery (two tiers)

Component loading follows a two-tier rule:

| Tier | Components | Loading | Rationale |
|------|-----------|---------|-----------|
| **Architecture** | agents, MCP servers, A2A services, skills | Explicit declaration in the formation manifest | They define the formation's capability surface |
| **Content / policy** | SOPs, triggers, groups, transformers | Auto-discovered from their directory | Data consumed by the architecture; their effect is gated elsewhere (SOP semantic matching, trigger URL + auth, middleware-resolved group membership) |

**Architecture tier.** Components are declared explicitly in the formation file by ID. Files in subdirectories (`agents/`, `mcp/`, `a2a/`, `skills/`) are pure definitions; only components listed in the formation manifest are loaded.

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

**Content/policy tier.** Files under `sops/`, `triggers/`, `groups/`, and `transformers/` are auto-discovered — presence in the directory loads them; no manifest entry exists. The component id derives from the filename stem. This is intentional: these files are policy and content, inert until something else activates them, and they churn operationally at a rate the manifest should not have to track.

---

## 4. Overrides and precedence

Default precedence order:
1. Formation defaults
2. Component defaults (agents / services)
3. Agent-specific overrides

This enables concise top-level definitions with targeted specialization.

### 4.1 Model aliases and the model selection hierarchy

The formation may define semantic model aliases:

```yaml
llm:
  aliases:
    fast: "openai/gpt-4o-mini"
    premium: "anthropic/claude-sonnet-4-5"
```

Alias names match `[a-zA-Z0-9_-]+`, map to fully qualified `provider/model` strings, and **must not** collide with capability names (`text`, `vision`, `audio`, `video`, `documents`, `embedding`, `streaming`).

A `model:` reference — an alias or a `provider/model` string — is accepted at multiple levels, and **the lowest (most specific) level wins**: the author closest to the work picks the model.

| Level (most specific first) | Surface |
|-----------------------------|---------|
| SOP step directive | `[model:x]` (§2.6) |
| SOP / trigger / skill frontmatter | `model:` (§2.6, §2.7, §2.5) |
| Agent | `llm_models:` capability overrides |
| Formation | `llm.models` |

Model references are validated at load time: each must resolve to a defined alias or be of `provider/model` form.

---

## 5. Access control

The runtime stores **no group memberships**. Groups reach a formation in exactly one way: a formation-declared **request middleware** — a standard MCP server the runtime calls with every request payload after client-key auth and before any processing. The middleware matches `user_id` to groups against whatever the organization uses (its DB, WorkOS, LDAP, a static map); how it does so is outside this standard.

### 5.1 `rbac` and `middleware`

Two **top-level** blocks — not under `server:`, because the pipeline applies equally to HTTP traffic and to embedded `overlord.chat(...)` use:

```yaml
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

**`rbac`:**

| Setting | Behavior |
|---------|----------|
| `active: auto` (default) | RBAC is on iff `groups/` contains group files |
| `active: true` | Declares intent explicitly; no group files **must** be a load-time error |
| `active: false` | Kill switch: `groups/` may exist but filtering is disabled; runtimes must log this loudly at load |
| `fallback: false` (default) | A request that ends up with **no groups** is rejected |
| `fallback: <group>` | No-group requests proceed with that group's permissions (`public` is the idiomatic open tier); the named group must exist in `groups/`, validated at load |

`fallback` applies only to a **clean no-groups outcome** — no middleware declared, or the middleware cleanly answered "none". It **never** applies to middleware errors (fail-closed, below).

**Dead-config rule:** RBAC active + `fallback: false` + no `middleware` block would reject every request — this **must** be a load-time error. (With `fallback: <group>` the combination is legal: every request gets the fallback tier.)

**`middleware`** is a single optional request transformer that **must** be an actual MCP server — stdio (`command` + optional `args`) or http (`url` + optional `headers`), exactly one transport — plus `timeout` (a duration string such as `2s`). It **must** expose exactly one tool named `middleware` whose input and output schemas are defined by this spec. At formation load the runtime connects, lists tools, and **must fail fast** if the tool is absent or its declared schema does not match the contract.

**Tool contract — request payload in, request payload out:**

- Input: the full request payload — `user_id`, `message`, `attachments`, `metadata`, `route_class` — as the tool arguments. `groups` is **never** part of the inbound payload; a middleware declaring it as an input property **must** fail formation load. Groups can only be attached on the way out, so they can never arrive as a caller's claim.
- Output: the same-shaped payload, possibly modified, plus an optional `groups` list of group ids — the **only** channel through which memberships enter the runtime (no request-asserted form, therefore no precedence rules). Identity mapping (rewriting `user_id`) and payload policy are permitted; `route_class` must be echoed unchanged. The runtime **must** validate every response against the request schema before continuing with it.
- `route_class` identifies the origin: external routes (`chat`, `audiochat`, `trigger`, `api`) and the internal origins `heartbeat` and `scheduler`. Internally-originated requests synthesize the same payload and traverse the identical pipeline — no special cases.
- The middleware's only voice into the request is the returned payload. Middleware wanting to persist context does so itself through the public API; it gets no side channel.

**Pipeline** (identical for external and internally-originated requests):

```
client-key auth (external) / internal origin
   └─ middleware (if declared)         request payload -> request payload (+ groups)
        └─ rbac (if active)
             groups attached? -> resolve permissions from groups/ (§5.2)
             no groups?       -> fallback group | reject
                  └─ process request (filtered context)
```

**Fail-closed:** a middleware error, timeout, or malformed/schema-invalid response **must** reject the request. `rbac.fallback` does not apply to errors — a fallback on error would let an identity-provider outage silently reassign users to the fallback group. Rejections must be observable (authorization-failure / middleware events).

**No runtime-side caching:** the middleware is called on every request with full transformation rights — one consistent semantic. Responding fast is the middleware's responsibility; it may cache internally however it likes. The only runtime knob is `timeout`.

**Removed surface:** earlier drafts of this section specified `server.auth: required|open` gated by a runtime-side user/membership database. Both are removed. A formation still carrying `server.auth` **must** fail to load with a migration error. The client key authenticates the calling application; user-level gating is expressed as `rbac.fallback: false` (grouped users only) plus a middleware that returns no groups for unknown users.

### 5.2 Groups

Group permission files live in a `groups/` directory and are **auto-discovered** (§3). A group file grants nothing by itself: it takes effect only when the request middleware attaches its id to a request (or `rbac.fallback` names it), so discovery-on-presence is safe. An empty `groups/` directory is inert (warning only).

Group file format — the group id is the filename stem:

```yaml
# groups/analyst.afs
name: "Business Analyst"               # optional
description: "Analysis and reporting"  # optional
inherits: base-user                    # optional; string or list; cycles are a load error

# Plain lists are allow-lists. "*" matches all. Use the long form
# {allow: [...], deny: [...]} when subtracting from wildcards or
# overriding inherited allows.
agents:
  - researcher                         # plain grant
  - db-assistant:                      # grant + agent-scoped tool override
      database-mcp:
        tools:
          allow: [get_financials, list_orders]

mcp_servers:                           # group-wide tool overrides per server
  database-mcp:
    tools:
      deny: ["update_*", "delete_*"]

triggers:
  - invoice-processor
  - "report-*"

sops: "*"

native_apps:
  - memory-visualizer

memory:
  write: ["group:analyst"]             # shared-memory write grants
```

Sections: `agents`, `mcp_servers`, `triggers`, `sops`, `native_apps`, `memory.write`. Patterns are `fnmatch` globs. Resolution rules:

1. **Union of allows** across a user's groups; **any group's deny wins** (deny is global, allow is per-group).
2. **Inheritance** resolves parents first (depth-first, cycle-checked); list sections merge additively; a child's tool-override block **replaces** the parent's block for the same (agent, server) key.
3. **No `groups/` directory** = RBAC is inactive under `active: auto`; no resource filtering.
4. **A request that ends up with no groups** (no middleware, or the middleware cleanly returned none) is rejected — unless `rbac.fallback` names a group, in which case it proceeds with that group's permissions (§5.1).

### 5.3 The tool override cascade

Tool control is one concern appearing at four levels; the most specific level wins:

| Level | Keys | Role |
|-------|------|------|
| Formation `mcp.servers[].tools` | `allow` / `deny` (either or both) | Hard catalog bound — pruned at registration; nothing below can resurrect a pruned tool |
| Agent `mcp_servers` attachment `tools` | `allow` / `deny` (either or both) | The agent's default tool surface for that server — on an inline (agent-private) definition or on a `{id, tools}` reference to a formation-declared server; applied after the registry bound |
| Group `mcp_servers.<id>.tools` | `allow` / `deny` (either or both) | Group-wide override for that server, across all granted agents |
| Group `agents.<agent>.<id>.tools` | `allow` / `deny` (either or both) | Most specific: this group, this agent, this server |

An agent's `mcp_servers` entry may be a plain string (attach the formation-declared server as-is), a `{id, tools}` mapping (attach it with a narrowing override), or a full inline definition (agent-private server, optionally with its own `tools` block). Attachment-level `tools` blocks chain **after** the registry bound: they select from the already-pruned catalog, so an attachment can narrow the agent's view but never resurrect a registry-pruned tool.

Group override semantics: if a group provides a `tools:` block at some level, it **supersedes** the inherited block; otherwise the inherited config applies unchanged. Within a block: `allow` alone = exactly this set (expanded against the post-registry catalog, so a group override may supersede — not merely intersect — the agent's inherited view); `deny` alone = inherited minus these; both = allow-then-subtract. `tools: {deny: "*"}` hides a server from a group entirely.

The vocabulary is uniform across all four levels: `allow`/`deny`, either or both, with deny applied after allow (deny wins on overlap). A single string pattern is accepted wherever a list is (the `deny: "*"` idiom). At the registry and attachment levels, `whitelist`/`blacklist` are accepted as aliases of `allow`/`deny`; declaring a canonical key together with its own alias in one block (`allow` + `whitelist`, or `deny` + `blacklist`) is a load-time error. Group blocks accept the canonical keys only.

### 5.4 Design principle: tool granularity is the permission granularity

Access control in Agent Formation gates **tools**. Formations should ship semantic tools (`get_financials`, `update_order`), not generic ones (`query`). The mechanisms in this section compose well-designed tools; they do not attempt data-level enforcement inside badly-designed ones.

---

## 6. Proactive messaging and commands

### 6.1 `proactive:` block

Declares outbound notification channels and an optional autonomous heartbeat:

```yaml
proactive:
  channels:
    slack:
      transformer: slack                   # transformers/slack.yaml, or the bundled template
      url: "${{ secrets.SLACK_WEBHOOK }}"  # optional; overrides the transformer's endpoint.url
  default_channel: slack                   # channel name or literal "webhook"
  heartbeat:
    enabled: true                          # default true when the block is present
    interval: "30m"                        # duration string (Ns/Nm/Nh); default 30m
    target: last                           # last | preferred | webhook | <channel name>
    active_hours:
      start: "09:00"
      end: "18:00"
      timezone: "UTC"                      # IANA name, or literal "user"
      weekends: true                       # false suppresses Sat/Sun
    sop: my-heartbeat                      # optional; replaces the bundled default heartbeat SOP
    instruction: "Focus on today's prep"   # optional; appended to the heartbeat prompt
```

Rules:
- Each channel references a transformer by name (formation `transformers/` first, then bundled templates). A channel whose transformer has no `endpoint.url` **must** supply `url:` — validated at load.
- `last`, `preferred`, and `webhook` are reserved routing targets and cannot be used as channel names.
- Per-notification routing precedence: explicit channel > user-preferred channel > `default_channel` > the formation's async webhook.
- An enabled heartbeat requires the scheduler to be enabled (load-time validation).
- The default heartbeat behavior comes from a runtime-bundled SOP; `heartbeat.sop` replaces it with a formation SOP.

### 6.2 `commands:` block

Opt-in slash-command surface:

```yaml
commands:
  enabled: true          # default true when the block is present
  aliases:
    tasks: jobs          # /tasks resolves like /jobs
  builtin:
    reset: false         # hide the built-in /reset
```

Resolution order: alias expansion → formation SOPs by name → built-in registry. A formation SOP **shadows** a built-in command of the same name. Runtimes ship built-ins (reference set: `setup`, `help`, `status`, `jobs`, `identity`, `channels`, `preferences`, `reset`); the `builtin:` map disables them individually, and unknown names in the map are a validation error.

---

## 7. Artifacts

Optional `artifacts:` block controlling artifact capture and retention. Artifact capture is **on by default** (omit the block and you still get local artifact storage):

```yaml
artifacts:
  enabled: true               # default true
  storage:
    type: local               # v1: local only (s3 and friends are rejected)
    path: "./artifacts"       # default; relative to the formation directory
  encryption:
    enabled: true             # default true
  retention:
    policy: last_accessed     # last_accessed (default) | last_updated
    duration: 0               # days; 0 = keep forever (default)
```

---

## 8. Secrets and environment variables

- Secrets are referenced as: `${{ secrets.NAME }}`
- Environment variables as: `${{ env.VAR }}`

Concrete storage and resolution are runtime-defined, but the syntax is standard.

---

## 9. Init hook

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

## 10. Extensions

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

## 11. Backward compatibility

- Patch/minor releases are backward compatible.
- Major releases may break compatibility and must include migration notes.

See `versioning.md`.
