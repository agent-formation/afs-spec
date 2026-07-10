# Coding-agent delegation

The top-level `coding:` block delegates coding tasks to an external **headless coding CLI** (Claude Code, droid, opencode, pi, ...) as fire-and-collect background work. Declaring the block registers one delegation tool (`delegate_coding` in the reference implementation) that spawns the configured CLI as a tracked subprocess and returns a job handle immediately — the chat turn never blocks, and there is **no synchronous mode**.

The standard ships the **mechanism only**: adapters are declarative content, installation/authentication/sandboxing are the developer's responsibility (the runtime only verifies the binary exists at formation load), and vendor taxonomies — permission modes, safety levels, model names — pass through opaquely.

Like `middleware/`, this directory is **not** auto-discovered: a formation-local adapter file at `coding/<name>.yaml` (or `.yml`) loads only when `coding.client:` names it, and **shadows** a bundled template of the same name — the same shadowing rule as built-in skills and channel transformers. Runtimes bundle dormant templates (reference set: `claude-code`, `droid`, `opencode`, `pi`); see `claude-code.yaml` here for the annotated canonical adapter.

## Declaration

```yaml
# formation.afs -- top-level block
coding:
  client: claude-code            # bundled or formation-local adapter template name
  model: sonnet                  # optional default model (opaque vendor namespace)
  workdirs: ["./workspace"]      # required; declared roots, must exist at load
  cleanup: delete                # delete (default) | keep
  timeout: 30m                   # per-delegation ceiling (default 30m)
  max_concurrent: 3              # default 3
  groups: []                     # allowlist; empty/absent = every group may delegate
  extra_args:                    # verbatim vendor passthrough -- YOUR safety policy
    - "--permission-mode"
    - "acceptEdits"
  env:                           # the ONLY place ${{ secrets.* }} resolves
    ANTHROPIC_API_KEY: "${{ secrets.ANTHROPIC_API_KEY }}"
```

Instead of `client:`, the adapter may be defined **inline** (escape hatch; same schema as a template file, minus `name`):

```yaml
coding:
  command: "droid"
  args:
    base: ["exec", "--output-format", "json"]
    prompt: ["{prompt}"]              # or the literal string "stdin"
    session: ["--session-id", "{id}"] # one idempotent create-or-resume flag
    # or a distinct pair (claude-code style):
    # session_new: ["--session-id", "{id}"]
    # session_resume: ["--resume", "{id}"]
    model: ["--model", "{model}"]
  output: json                        # stream-json | json | text
  parse:
    result: "$.result"
    session_id: "$.session_id"
  workdirs: ["./workspace"]
```

`client:` together with any inline adapter key (`command`, `args`, `output`, `parse`) fails formation load; so does a block with neither.

## The adapter contract

Command assembly is an **exec array, never a shell** (no injection surface):

```
command + args.base + args.model (when a model is set) + session fragment + extra_args + args.prompt (or stdin)
```

Every fragment is a non-empty list of strings containing its placeholder (`{prompt}`, `{id}`, `{model}`).

**Three session shapes** — exactly one per adapter:

| Shape | Declaration | Id acquisition |
|-------|-------------|----------------|
| Idempotent | `session:` only | Runtime-generated; one flag serves create AND resume (droid) |
| Create/resume pair | `session_new:` + `session_resume:` | Runtime-generated; distinct create and resume fragments (claude-code) |
| Captured-id | `session_resume:` only | Tool-assigned; the first run gets NO session flag and the id is captured from output via `parse.session_id` (opencode, pi) |

A captured-id adapter cannot use `output: text` and requires `parse.session_id`. Session-id capture is **first-match** — a later event carrying an unrelated root-level id must not clobber it.

**Output modes** (`output:` selects the parser; `parse.*` are dot-path selectors, the same idiom as trigger `parse:` — `$.a.b`, list indexing, negative indices):

- `stream-json` — JSONL; selectors apply per event: `result` = last non-empty match, `session_id` = first match.
- `json` — a single document on exit (with a last-parseable-line fallback for CLIs that prepend informational output).
- `text` — the full stdout is the result; `parse:` selectors with `text` fail load.

**`forbidden_extra_args`** lists flags the block's `extra_args` must not contain — the runtime sets the subprocess working directory (a fresh `<root>/<user_id>/<request_id>` directory per delegation), so the tool's own cwd/worktree flags are rejected at load.

## Rules

- **Inert when unconfigured.** No `coding:` block = no tool registered, byte-identical behavior.
- **Secrets in `env:` only.** `${{ secrets.* }}` anywhere else in the block — `extra_args` especially — or anywhere in an adapter definition fails the load with an error pointing at `env:` (argv is `ps`-visible; the environment is not).
- **Workdirs are disposable; git is the persistence layer.** Roots must exist at load; each delegation runs in a fresh runtime-created subdirectory, deleted on terminal state under `cleanup: delete`. A resumed session gets a fresh directory — conversational continuity is the vendor session id, file continuity is git.
- **Always asynchronous.** Completion re-enters the originating session as an internal request (`route_class: delegation`) through the full middleware + RBAC pipeline. Timeout kills the process group but retains the session id; `max_concurrent` overflow is a friendly tool error, not a queue.
- **`groups:` gates delegation as one unit.** Each entry must name an existing group in `groups/` when RBAC is active.

See `specs/formation.md` §7 for the normative text. Reference implementation: MUXI runtime PRs [#274](https://github.com/muxi-ai/runtime/pull/274) and [#275](https://github.com/muxi-ai/runtime/pull/275).
