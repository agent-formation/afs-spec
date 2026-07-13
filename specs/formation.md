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
- Coding-agent delegation to external headless CLIs
- Remote async-job watching over MCP tools
- Declared external links and typed response affordances
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

A second auto-discovered document may live beside the soul: `MUXI.md`, the formation's curated operational learnings (who the formation *is* lives in `SOUL.md`; what it has *learned* lives in `MUXI.md`). See §11.2.

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

Formations that declare MCP servers also get remote async-job watching by default — see §8 (`mcp.watch`).

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
- `route_class` identifies the origin: external routes (`chat`, `audiochat`, `trigger`, `api`) and the internal origins `heartbeat`, `scheduler`, and `delegation` (coding-delegation completion re-entry, §7). Internally-originated requests synthesize the same payload and traverse the identical pipeline — no special cases.
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

Sections: `agents`, `mcp_servers`, `triggers`, `sops`, `native_apps`, `memory.write`. A group file may additionally carry an `mcp:` block overriding the formation's watch quota — the only supported key is `mcp.watch.max_concurrent` (§8.3). Patterns are `fnmatch` globs. Resolution rules:

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

## 7. Coding-agent delegation (`coding:`)

Optional **top-level** `coding:` block declaring how the formation delegates coding tasks to an external **headless coding CLI** (Claude Code, droid, opencode, pi, ...). Like `rbac:`/`middleware:`, the block is framework-mode friendly — it works identically with or without a `server:` block.

**Inert when absent.** No `coding:` block means no delegation tool is registered and nothing is constructed — runtimes **must** exhibit byte-identical behavior to a formation without the feature. Presence implies enablement.

The block configures a runtime-registered delegation tool (`delegate_coding` in the reference implementation) with the signature `(prompt, workdir?, model?, continue_job_id?)`. MUXI ships the mechanism only: installation, authentication, and sandboxing of the CLI are the developer's responsibility, and vendor taxonomies (permission modes, safety levels, model names) pass through opaquely.

```yaml
coding:
  client: claude-code            # bundled/formation-local adapter template name,
                                 # OR the inline adapter form (mutually exclusive)
  model: sonnet                  # optional default model (opaque vendor namespace)
  workdirs: ["./workspace"]      # required; declared roots, load-validated
  cleanup: delete                # delete (default) | keep
  timeout: 30m                   # per-delegation ceiling; default 30m
  max_concurrent: 3              # default 3
  groups: []                     # allowlist; empty/absent = every group may delegate
  extra_args:                    # verbatim vendor passthrough (permission/safety flags)
    - "--permission-mode"
    - "acceptEdits"
  env:                           # the ONLY place ${{ secrets.* }} resolves
    ANTHROPIC_API_KEY: "${{ secrets.ANTHROPIC_API_KEY }}"
```

Allowed keys: `client`, `command`, `args`, `output`, `parse`, `model`, `workdirs`, `cleanup`, `groups`, `extra_args`, `env`, `timeout`, `max_concurrent`. Unknown keys **must** fail formation load.

### 7.1 Adapters: client reference vs inline form

An **adapter** describes how to drive one CLI: the binary, its argument fragments, its output format, and how to extract values from that output. Adapters are declarative content, following the same convention as channel transformer templates (§2.8): runtimes ship **bundled dormant templates** (reference set: `claude-code`, `droid`, `opencode`, `pi`), inert until `coding.client:` references one by name.

- `client:` **must** match `[a-zA-Z0-9_-]+` and resolve to a bundled template or a formation-local adapter file at `coding/<name>.yaml` (or `.yml`). A formation-local file **shadows** the bundled template of the same name — the same shadowing rule as built-in skills and channel transformers. A template file's `name:` field **must** match its filename stem.
- The **inline form** is the escape hatch: the adapter keys (`command`, `args`, `output`, `parse`) appear directly on the `coding:` block. `client:` together with any inline adapter key **must** fail formation load; so must a block with neither.
- The `coding/` directory is **not** auto-discovered (unlike §3 content-tier directories): an adapter file loads only when `coding.client:` names it.

Adapter schema (template file or inline; allowed keys `name`, `command`, `args`, `output`, `parse`, `forbidden_extra_args` — unknown keys fail load):

| Key | Required | Meaning |
|-----|----------|---------|
| `command` | yes | The CLI binary (bare name resolved on PATH, or an absolute path) |
| `args.prompt` | yes | Arg fragment containing `{prompt}`, or the literal string `stdin` (prompt written to the subprocess's stdin — required for prompts past argv limits) |
| `args.base` | no | Fragments always present, in order (e.g. `["--print", "--output-format", "stream-json"]`) |
| `args.session` | no | ONE idempotent create-or-resume fragment containing `{id}` |
| `args.session_new` / `args.session_resume` | no | Distinct create/resume pair, each containing `{id}` |
| `args.model` | no | Fragment containing `{model}`; appended only when a model value is set |
| `output` | no | `stream-json` \| `json` \| `text` (default `text`) — selects the output parser |
| `parse.result` / `parse.session_id` | no | Extraction selectors applied to the vendor's JSON (§7.3) |
| `forbidden_extra_args` | no | Flags that `coding.extra_args` **must not** contain (load-validated) |

Every fragment is a non-empty list of strings, and each fragment **must** contain its placeholder (`{prompt}`, `{id}`, `{model}`).

**Command assembly is an exec array, never a shell** (no injection surface): `command` + `args.base` + `args.model` (when a model is set) + session fragment + `extra_args` + `args.prompt` (or stdin).

### 7.2 Session shapes

An adapter declares exactly one of three session shapes; declaring `session` together with `session_new`/`session_resume` **must** fail load, as must `session_new` without `session_resume` (a session that can be created but never resumed is dead config).

| Shape | Declaration | Id acquisition |
|-------|-------------|----------------|
| **Idempotent** | `session:` only | Runtime-generated: one flag serves create AND resume; the runtime generates the id on the first delegation (droid style) |
| **Create/resume pair** | `session_new:` + `session_resume:` | Runtime-generated: distinct fragments for the first run and for resumption (claude-code style) |
| **Captured-id** | `session_resume:` only | Tool-assigned: the first delegation runs with NO session flag and the runtime **captures** the id from parsed output via `parse.session_id` (opencode/pi style) |

A captured-id adapter **must not** use `output: text` and **must** define `parse.session_id` — both are load errors. Session-id capture is **first-match**: the first event yielding a value wins, and later events carrying an unrelated id **must not** overwrite it.

Whichever the shape, the vendor session id is persisted on the tracked job and replayed on continuation (`continue_job_id`); agents never see vendor session ids.

### 7.3 Output modes and parse selectors

`output:` selects the parser; `parse.result`/`parse.session_id` are dot-path selectors (`$.a.b`, list indexing via `[0]` or numeric segments, negative indices allowed — the same `parse:` idiom as triggers, §2.7).

| Mode | Behavior |
|------|----------|
| `stream-json` | JSONL — one event per line; unparseable lines are skipped. Selectors apply to **each** event: `result` takes the **last non-empty** match (streams repeat/accumulate, the last wins); `session_id` takes the **first** match |
| `json` | A single document on exit; selectors apply to it. Runtimes **should** fall back to the last parseable line when the CLI prepends informational output |
| `text` | Opaque — the full stdout is the result; no extraction. `parse:` selectors together with `output: text` **must** fail load (dead config) |

When a selector extracts nothing, the raw stdout **must** be kept as the result rather than dropped.

### 7.4 Workdirs are disposable; git is the persistence layer

`workdirs:` is **required**: a non-empty list of declared root directories (relative to the formation directory, or absolute). Each root **must** exist and be a directory at formation load (symlink-resolved).

Every delegation runs in a **fresh, runtime-created `<root>/<user_id>/<request_id>` directory** as the subprocess working directory — never the root itself. Runtimes **must** also present that directory as the process's logical cwd in the environment (e.g. rewrite `PWD`), since some CLIs resolve their working directory from it. The tool's `workdir` parameter selects one of the declared roots (default: the first); a value outside the allowlist **must** be rejected as a tool error, never an exception.

Nothing durable lives in a delegation directory — **git is the persistence layer**: ad-hoc tasks need nothing durable, new projects are git-inited and pushed by the tool, existing projects are cloned/coded/push-branched within the run. Consequently a resumed session gets a **fresh** directory: conversational continuity comes from the vendor session id, file continuity comes from git.

`cleanup:` is `delete` (default — the directory is removed when the job reaches a terminal state) or `keep` (opt-in, debugging). Runtimes **should** run a TTL sweep removing stray directories left by crashed runs.

Because the runtime owns the cwd, `extra_args` **must not** contain the tool's own cwd/worktree flags; adapters declare these via `forbidden_extra_args` and the load **must** fail on a match.

### 7.5 Access, secrets, and passthrough

- **`groups:`** — a resource-side allowlist gating who may delegate, as one unit (per-inner-tool modeling would require a stable vendor tool namespace). Empty or absent = every group may delegate. When RBAC is active (§5), each entry **must** name an existing group in `groups/` — validated at load, like `rbac.fallback`.
- **Secrets placement rule:** `${{ secrets.* }}` resolves under `coding.env:` **only**. A secrets reference anywhere else in the block — `extra_args` especially — or anywhere in an adapter definition **must** fail formation load with an error pointing at `env:`. Rationale: argv is visible to every user on the host via `ps`; environment variables are not. One credential path means no command-line redaction machinery is needed; observability events never log env values.
- **`extra_args:`** — verbatim vendor passthrough; this is where vendor permission/safety/autonomy flags live (`--permission-mode`, `--auto`, `--dangerously-skip-permissions`, ...). The standard does not model, translate, or validate them beyond the `forbidden_extra_args` check.
- **`model:`** — an opaque, non-empty string in the vendor's namespace; overridable per call. Deliberately **not** integrated with `llm.aliases` or the model-selection hierarchy (§4.1). Setting `coding.model` when the adapter defines no `args.model` fragment **must** fail load.
- **`env:`** — a mapping of string names to string values, passed to the subprocess environment verbatim (after secrets resolution).

### 7.6 Execution contract: always asynchronous

Delegation **must** be asynchronous — a fire-and-collect **tracked job**:

- The delegation tool returns a job handle immediately (`{"job_id": ..., "status": "started"}`); the calling turn completes normally. Runtimes **must not** offer a synchronous mode or a sync escape hatch.
- On completion the runtime synthesizes an internal request into the originating session with `route_class: delegation`, traversing the full middleware + RBAC pipeline (§5.1) like every other request.
- Headless CLIs never block mid-task: a run that needs human input ends its turn with the question as its final message; the user's answer resumes the session via the continuation parameter. No pause/approval primitive exists.
- `timeout:` (duration string — bare seconds or `ms`/`s`/`m`/`h`; default `30m`; must be positive) is the per-delegation ceiling. On expiry the runtime **must** kill the delegation's whole process group and mark the job timed out; the session id is retained, so post-timeout resumption is never blocked by the runtime.
- `max_concurrent:` (integer ≥ 1, default 3) bounds concurrent delegations per formation; a delegation beyond the bound **must** be a friendly tool error, not a queue.
- Cancellation kills the whole process group and retains the session id (the task stays resumable). Pause/resume need not be supported — a one-shot headless run has no meaningful pause.

### 7.7 Fail-fast load validation

All of these **must** fail formation load, never surface at delegation time:

- `client:` names no bundled or formation-local adapter, and no inline adapter is given; `client:` alongside inline adapter keys
- Adapter schema invalid (missing `command`/`args.prompt`; conflicting session shapes; `{prompt}`/`{id}`/`{model}` placeholders missing; unknown keys; captured-id adapter without `parse.session_id` or with `output: text`)
- The adapter binary is absent (bare `command` not on PATH; absolute `command` missing or not executable) — the runtime verifies presence only; installing and authenticating the tool is the developer's business
- Any `workdirs` root missing or not a directory; `workdirs` absent or empty
- A `${{ secrets.* }}` reference outside `env:`
- A `groups:` entry naming a group that does not exist in `groups/` (when RBAC is active)
- `output` not one of `stream-json`/`json`/`text`; `cleanup` not one of `delete`/`keep`; `timeout` unparseable or non-positive; `max_concurrent` not an integer ≥ 1
- `coding.model` set with no adapter `args.model` fragment; `extra_args` containing a `forbidden_extra_args` flag

See `schemas/coding/` for the adapter template format and the annotated `claude-code` reference adapter.

---

## 8. Remote job watching (`mcp.watch`)

Some MCP-reachable work outlives a turn: image or video generation, long renders, batch jobs. A well-designed MCP server answers inline when fast and returns a job handle (`{job_id, status: "processing"}`) when slow — **async-ness is a property of the response, not the tool**, so the standard never marks MCP tools async (no `async:` flag, no callback injection). What it standardizes instead is one runtime-registered polling tool — `watch_job` in the reference implementation — that polls a status tool at a formation-configured cadence until a deterministic terminal condition, then re-enters the result into the originating conversation.

**Default ON when MCP servers are declared; inert otherwise.** The tool registers whenever the formation declares `mcp.servers` ("declared" means the raw server list — runtime built-ins do not count). It grants no new capability: every poll executes the named tool under the **original caller's** resolved permission context (§5) — a user who cannot call the status tool cannot watch it. There is deliberately no `enabled:` key; the sole escape hatch is `mcp: { watch: false }`, which removes the tool entirely (tool-catalog hygiene, or a strict no-background-work compliance posture).

### 8.1 The `watch:` sub-block

Cadence and deadline are **formation configuration, not agent arguments**: polls are zero-token deterministic tool calls, so a uniform formation-set interval is cheap even when suboptimal for a given job, and numeric knobs are exactly what LLMs pick badly. Runtimes **must not** expose cadence or deadline as tool parameters.

```yaml
mcp:
  watch:                          # optional; all keys optional
    interval: 30                  # THE poll cadence (seconds)
    timeout: 7200                 # THE watch deadline (seconds)
    max_concurrent: 10            # active watches per user
    max_consecutive_failures: 3   # consecutive poll errors before the watch fails
  servers:
    - image-gen-mcp
```

| Key | Type | Default | Meaning |
|-----|------|---------|---------|
| `interval` | positive number (seconds) | 30 | Fixed poll cadence; first poll after one interval |
| `timeout` | positive number (seconds) | 7200 | Watch deadline; on expiry the watch resolves as timed out and re-enters with that status (nothing silently vanishes) |
| `max_concurrent` | integer ≥ 1 | 10 | Active watches **per user**. This quota governs watches only — it bounds nothing else |
| `max_consecutive_failures` | integer ≥ 1 | 3 | Consecutive failed polls that fail the watch with the last error |

Validation is fail-fast at formation load, never a watch-time surprise:

- The key set is closed — unknown keys under `watch:` **must** fail load.
- `interval`/`timeout` **must** be positive numbers; `max_concurrent`/`max_consecutive_failures` **must** be integers ≥ 1. A boolean **must** be rejected wherever a number is expected.
- `watch: false` disables the feature; `watch: true` or an absent `watch:` key (with servers declared) yields the defaults.
- A `watch:` block in a formation that declares no `mcp.servers` is dead config and **must** fail load.

### 8.2 The `watch_job` tool contract

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

`tool` and `done_when` are required; `args`, `result`, and `label` are optional.

**Always asynchronous.** The tool **must** return a job handle immediately and end there; the poll loop runs in the background and completion re-enters the conversation as an internal request through the full middleware + RBAC pipeline (§5.1), with the poll body treated as untrusted external content. Runtimes **must not** offer a blocking mode or a sync escape hatch — the same rule as coding delegation (§7.6). Watches are tracked jobs: listable and cancellable on the runtime's jobs surface; cancellation stops polling with no re-entry.

**`done_when` is deterministic — no LLM in the poll loop.** It is an object with a closed key set (`path`, `equals`, `in`; unknown keys **must** be rejected):

- `path` (required): a non-empty dot-path selector into the poll response body (e.g. `$.status`).
- Exactly **one** of `equals` (a single terminal value) or `in` (a non-empty list of terminal values) — both or neither **must** be rejected.
- The condition is met when the value at `path` matches the expected value(s). Matching is exact equality with a string-form fallback (`equals: "3"` matches a numeric `3`), and **strictly typed for booleans: a boolean matches only a boolean** — numeric coercion (`1 == true`) **must not** count as a match, or determinism breaks.
- A missing `path` in the poll body is simply "not terminal yet" — never an error.

`done_when` should enumerate **every** terminal state the service can report (not just success); otherwise a failed job polls until the deadline.

Runtimes **should** teach the recognition behavior (job-shaped response → `watch_job` → conversational acknowledgment) via a bundled dormant SOP fragment appended to agent instructions whenever the tool registers. A formation-local `sops/watch_job.md` **shadows** the bundled fragment (an empty file removes it) — the same shadowing rule as built-in skills and channel transformers.

### 8.3 Group quota override

Group files (§5.2) may override the watch concurrency quota, mirroring the formation shape so the override looks like the thing it overrides:

```yaml
# groups/power-users.yaml
mcp:
  watch:
    max_concurrent: 25      # overrides the formation default for members
```

- Both key sets are closed: in a group file, `mcp:` supports only `watch`, and `watch:` supports only `max_concurrent` (an integer ≥ 1). Anything else **must** fail load.
- A user in multiple groups gets the **highest** of their groups' values — grants are additive, the same semantics as every other group list (§5.2). No group value → formation default. Inheritance keeps the highest value along the chain.
- The override governs **watches only**; it grants no tools and bounds nothing else.

---

## 9. Declared links and response affordances (`links:` + `ui`)

Two principles anchor this section: the runtime is a **gateway, not an app** — it never renders anything, ships no components, no HTML, no JS; and rich UI is **text-first, progressively enhanced** — clients that understand an affordance render it natively, everyone else loses nothing.

### 9.1 `links:` — declared external destinations

Optional **top-level** section declaring named external destinations (credential portals, OAuth consent pages, dashboards) that response producers may surface as `action_link` widgets (§9.3) with formation-config provenance:

```yaml
links:
  jira:
    label: "Connect Jira"                          # optional display label
    url: "https://auth.acme.com/connect/jira"      # required; http(s) only
    hint: "Opens your company's credential portal" # optional one-liner
```

A mapping of `name -> {label, url, hint}`. Rules (validated at formation load):

- `url` is required and **must** be an `http://` or `https://` URL.
- `label` and `hint` are optional strings.
- An entry that is not a mapping with a `url` field **must** fail load.

### 9.2 The `ui` envelope array

The response envelope gains an optional, typed `ui` array of *affordances*:

```jsonc
{
  "text": "Which repository did you mean? I found three.",   // always complete alone
  "ui": [
    {
      "type": "options",
      "id": "ui_7f3a",                       // runtime-assigned, for the reply path
      "prompt": "Which repo?",
      "options": [
        {"value": "muxi-ai/runtime", "label": "runtime"},
        {"value": "muxi-ai/cli",     "label": "cli"}
      ],
      "multi": false
    },
    {
      "type": "action_link",
      "id": "ui_9c21",
      "label": "Connect Jira",
      "url": "https://auth.acme.com/connect/jira",
      "hint": "Opens your company's credential portal"
    }
  ]
}
```

Rules:

- **`ui` is additive and optional.** When a response carries no widgets the key **must** be absent entirely (not `null`, not `[]`) — the envelope **must** be byte-identical to a pre-feature response.
- **`text` carries the fallback duty.** Producers **must** phrase the response text so the interaction works without any widget (e.g. options are also listed in prose). A user on a plain-text channel loses nothing essential.
- **Unknown widget types must be ignored.** Clients render the types they know and **must** skip the rest; new widget types are therefore never protocol breaks. The type registry is versioned in this spec, not negotiated at runtime.
- **Widgets are producer-built, never LLM-emitted.** Widgets enter the envelope only through runtime producers; free-form LLM output **must not** become a widget.
- **Size clamps.** Runtimes **must** clamp per-widget and per-envelope sizes; an oversized widget **must** be dropped whole, never truncated (a partial widget is worse than none — the text fallback is always complete on its own). Reference defaults: 4096 bytes per widget, 8 widgets and 16384 combined bytes per envelope, 25 options per `options` widget.

### 9.3 Widget type registry (v1)

| Type | Purpose | Status |
|------|---------|--------|
| `options` | Clarification with choices — pick, don't type | v1 |
| `action_link` | Send the user somewhere external — credential portal, OAuth consent, dashboard | v1 |
| `mcp_resource` | Gateway passthrough of an MCP App / UI resource returned by an external MCP server — relayed verbatim, rendered by capable clients only | reserved for a future version |

**`options`** fields: `type`, `id` (runtime-assigned; the reply-path key), `prompt` (short question), `options` (list of `{value, label}`; an entry without a `value` is dropped, a missing `label` falls back to the value), `multi` (boolean; always `false` in v1).

**`action_link`** fields: `type`, `id`, `label`, `url`, `hint` (optional). The `url` **must** be `http(s)` — anything else **must** yield no widget.

**`mcp_resource`** is untrusted external content: the runtime relays it and **must not** execute or interpret it.

### 9.4 `action_link` provenance

An `action_link` URL **must not** be LLM-fabricated. Every URL enters a widget through a producer that records its source, and the only admissible sources are:

1. formation config — a declared `links:` entry (§9.1),
2. a tool result,
3. a trigger payload.

The LLM may *select* among provenanced URLs; it can never mint one into a widget. (Prose URLs in `text` remain what they are today — it is the elevated, clickable affordance that demands provenance.)

### 9.5 The reply path (`ui_response`)

The runtime stays **stateless** — no widget state is stored server-side; a widget `id` is meaningful only within the conversation's own history. The client replies with a normal next message plus an optional structured hint:

```jsonc
{
  "message": "runtime",                                        // always present, always sufficient
  "ui_response": {"id": "ui_7f3a", "value": "muxi-ai/runtime"} // optional hint
}
```

- `message` alone is always sufficient — a client may render options as plain text and let the user type; the LLM disambiguates as usual.
- `ui_response` is a **hint** that makes the choice machine-certain. For a clarification-produced `options` widget, a hint whose `id` matches the asking widget and whose `value` is one of the offered options **must** pin the selection deterministically — no re-interpretation.
- An unknown or stale `id`, or a value not among the offered options, **must** be ignored — the message stands alone. Ignoring is silent (never an error): the hint is advisory by construction.

### 9.6 Transport

- **REST:** `ui` appears on the final response object (subject to the absent-when-empty rule, §9.2).
- **SSE:** a dedicated `ui` event (`event: ui`, data `{"ui": [...]}`) emitted at end of turn — after the text stream, before the terminal done event. Clients render affordances after text completes.
- **Channels (Slack/Telegram/email transformers):** a transformer that does not render widgets natively simply ignores `ui` — the text fallback *is* the channel experience.

---

## 10. Artifacts

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

## 11. Self-improvement (`tuning:` + `MUXI.md`)

A formation improves itself by reading its own logs: one scheduled in-runtime loop digests operational activity, distills behavioral learnings, and curates `MUXI.md` — a bounded markdown file of operational guidance injected into every turn's context beside the soul. **On by default**: an absent block means the loop runs with the defaults below.

The loop **never** edits formation configuration. Anything requiring a deployment (yaml changes, plan upgrades, new tools) may only surface as prose recommendations to a human. Configuration stays static until restart.

### 11.1 `tuning:` block

```yaml
tuning:
  active: true          # default true -- the whole loop's off switch
  interval_hours: 24    # positive number; one loop pass per interval
  auto_apply: true      # false: revisions await human review (PENDING-MUXI.md)
```

Rules:
- **Closed key set** — exactly these three keys; unknown keys **must** fail the load.
- `active` and `auto_apply` are strict booleans; `interval_hours` is a positive number (booleans rejected where numbers are expected). All validation is fail-fast at load, never a tuning-time surprise.
- Boolean shorthand: `tuning: false` ≡ `{active: false}`; `tuning: true` ≡ the defaults.
- The loop's internals — what it observes (event capture, log digestion, benchmark-style probes) and how it distills — are runtime behavior, deliberately **not** configuration. They introduce no schema surface beyond this block.

### 11.2 Formation learnings (`MUXI.md`)

`MUXI.md` is the formation's file of learned operational guidance (routing habits, tool quirks, cost hotspots) — formation-owned, git-trackable, and hand-editable: a developer may write it by hand on day one and get value with no loop involved. Discovery mirrors the soul document (§2.1.1):

1. `MUXI.md` next to the formation file
2. `muxi.md` next to the formation file

Contract:
- **Injected verbatim** (no templating) into every turn's context wherever the soul is injected, so it **must** stay concise and general.
- **Bounded**: 32KB maximum, enforced at every write surface — an oversize revision is rejected, never truncated.
- **Hand edits take effect on the next turn**, without a restart; runtime writes land on the discovered file (canonical name `MUXI.md` when creating).
- **Privacy**: the file is injected into every user's context; runtimes **must** prevent loop-written revisions from carrying user identifiers or message content. Operational specifics (tool names, models, time windows) are the point and are not restricted.
- Under `auto_apply: false` the loop writes its suggested next version to **`PENDING-MUXI.md`** (a sibling, never injected); review is a diff of the two files. Accepting promotes pending to live; dismissing discards it. How acceptance is surfaced (commands, API, chat widgets) is runtime UX, not schema.

---

## 12. Secrets and environment variables

- Secrets are referenced as: `${{ secrets.NAME }}`
- Environment variables as: `${{ env.VAR }}`

Concrete storage and resolution are runtime-defined, but the syntax is standard.

---

## 13. Init hook

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

## 14. Extensions

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

## 15. Backward compatibility

- Patch/minor releases are backward compatible.
- Major releases may break compatibility and must include migration notes.

See `versioning.md`.
