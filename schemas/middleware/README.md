# Request middleware

The request middleware is how group memberships reach a formation — MUXI stores none. It is a formation-declared MCP server the runtime calls with **every** request payload after client-key auth and before any processing. It matches `user_id` to groups against whatever the organization uses (its DB, WorkOS, LDAP, a static map) and attaches them on the way out.

Unlike the other directories here, `middleware/` is **not** a formation directory: the middleware is declared as a top-level `middleware:` block in `formation.afs` (there is nothing to auto-discover). This directory documents the block and the tool payload schema.

## Declaration

```yaml
# formation.afs -- top-level, NOT under server:
rbac:
  active: auto            # auto (default) | true | false
  fallback: false         # false | <group_name>

middleware:
  # An actual MCP server. Exactly one transport:
  url: "${{ secrets.RESOLVER_URL }}"     # http
  headers:
    Authorization: "Bearer ${{ secrets.RESOLVER_TOKEN }}"
  # command: "./middleware.py"           # stdio (alternative)
  # args: ["--map", "groups.json"]
  timeout: 2s                            # the only runtime knob (default: 10s)
```

The simple case stays simple: a stdio middleware is a one-file script in the formation directory (`command: ./middleware.py`) reading a static map or the org's DB — no deployment, no service.

## The tool contract

The middleware MUST expose exactly one tool named `middleware` — request payload in, request payload out. At formation load the runtime connects, lists tools, and **fails fast** if the tool is absent or its declared schema does not match the contract.

Input schema (the request payload — note there is **no** `groups` property; declaring one fails formation load, so groups can never arrive as a caller's claim):

```json
{
  "type": "object",
  "properties": {
    "user_id":     { "type": "string" },
    "message":     { "type": "string" },
    "attachments": { "type": "array", "items": { "type": "object" } },
    "metadata":    { "type": "object" },
    "route_class": { "type": "string" }
  },
  "required": ["user_id", "message", "attachments", "metadata", "route_class"]
}
```

Output schema (same payload, plus the one field only the middleware may attach; an output schema, if declared, must match — every response is validated at runtime regardless):

```json
{
  "type": "object",
  "properties": {
    "user_id":     { "type": "string" },
    "message":     { "type": "string" },
    "attachments": { "type": "array", "items": { "type": "object" } },
    "metadata":    { "type": "object" },
    "route_class": { "type": "string" },
    "groups":      { "type": "array", "items": { "type": "string" } }
  },
  "required": ["user_id", "message", "attachments", "metadata", "route_class"]
}
```

Rules:

- The returned payload may be modified: identity mapping (rewriting `user_id`) and payload policy are permitted. `route_class` must be echoed unchanged.
- `groups` in the response is the **only** channel through which memberships enter the runtime — no request-asserted form, therefore no precedence rules.
- `route_class` identifies the origin: external routes (`chat`, `audiochat`, `trigger`, `api`) and the internal origins `heartbeat`, `scheduler`, and `delegation` (coding-delegation completion re-entry, see `schemas/coding/`). Internal requests synthesize the same payload and traverse the middleware identically — no special cases.
- Binary attachment content is base64-round-tripped (a `content_encoding: base64` marker on the attachment object).
- The middleware's only voice into the request is the returned payload; middleware wanting to persist context does so through the public API.

## Fail-closed, no caching

A middleware error, timeout, or malformed/schema-invalid response **rejects the request**. `rbac.fallback` never applies to errors — a fallback on error would let an identity-provider outage silently reassign users to the fallback group. `fallback` applies only to a clean no-groups outcome (no middleware declared, or the middleware cleanly answered "none").

The runtime never caches middleware answers: the tool is called on every request with full transformation rights. Respond fast; cache internally if you need to. The only runtime-side knob is `timeout`.

See `specs/formation.md` §5 for the normative text and `schemas/groups/` for the group file format the attached ids resolve against.
