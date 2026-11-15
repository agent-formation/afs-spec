# Triggers

Triggers are inbound HTTP entry points, defined as markdown files with YAML frontmatter.

- **Auto-discovered** — every `*.md` file in `triggers/` is loaded; there is no manifest entry (content/policy tier, see `specs/formation.md` §3).
- **Id from filename** — `triggers/github-issues.md` becomes trigger `github-issues`. Ids must match `^[a-zA-Z0-9_-]+$`.
- **Endpoint** — each trigger is exposed at `POST /v1/triggers/{id}`, authenticated with the formation client key (or the trigger's own `auth:` check, see below); the request then traverses the middleware + RBAC pipeline like every other route. `GET /v1/triggers` lists triggers; `GET /v1/triggers/{id}` returns metadata.

## File anatomy

```markdown
---
# All frontmatter keys are optional. Unknown keys are a load-time error.
name: "GitHub issue intake"     # display-name override
type: webhook                   # type annotation (semantic only)
channel: github                 # inbound channel name for source tracking
model: fast                     # model override: alias or provider/model
parse:                          # payload extraction (JSONPath, best-effort)
  message: $.issue.title
  user_id: $.sender.login
  files: $.attachments
  context:                      # name -> JSONPath map, exposed to transformers
    repo: $.repository.full_name
transformer: slack              # format the outbound payload (see transformers/)
webhook: https://example.com/x  # outbound delivery URL
auth: ./auth/github.py           # own auth check: script path or http(s) URL
---
Instructions for the agent, with ${{ data.* }} placeholders
referencing the inbound POST payload.
```

## Outbound composition

`webhook:` and `transformer:` **compose** — they are not mutually exclusive:

| Present | Behavior |
|---------|----------|
| `webhook:` only | Raw standard payload delivered to the webhook URL |
| `transformer:` only | Formatted payload delivered to the transformer's own `endpoint.url` |
| both | Formatted payload delivered to the trigger's `webhook:` URL (trigger URL wins) |

A trigger referencing a transformer with no URL from either side fails at formation load.

## Per-trigger auth

Providers such as Stripe or HubSpot cannot send the client key; they sign each request. `auth:` names a script (path relative to the formation directory) or an http(s) URL that receives the whole request as JSON (`trigger`, `method`, `url`, `headers`, and `body` as base64 of the exact bytes) and answers pass or fail:

| Target | Receives the JSON | Pass |
|--------|-------------------|------|
| Script | on stdin, with the runtime's environment | exit code 0 |
| URL | as a POST | any 2xx |

- A pass runs the trigger as a keyed call: the provider's JSON object becomes `data` (other bodies become `{"body": "<text>"}`), async, in its own session, with no caller-supplied user id.
- A fail, an error, a timeout or an unreachable target is answered exactly like a request without the client key.
- A caller holding the client key skips the check, which is how stored events are replayed.
- A missing or non-executable script, or a URL with no HTTP response, fails the formation load.

See `github-issues.md` in this directory for a complete annotated example, and `specs/formation.md` §2.7 for the normative text.
