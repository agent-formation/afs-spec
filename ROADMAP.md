# Roadmap

This roadmap outlines the path from early adoption to a stable v1.0 Formation standard.

---

## Current status

- Formation schemas are in **v0.x** (active iteration).
- MUXI is the current reference implementation.
- The standard is designed for cross-runtime adoption.

---

## v0.x goals (now)

- Clarify and tighten core fields.
- Expand conformance fixtures.
- Improve validator UX and error messages.
- Finalize extension mechanism in the spec.
- Publish mappings for other agent ecosystems.

Deliverables:

- `specs/formation.md`
- `specs/versioning.md`
- `specs/secrets.md`
- `tests/fixtures`
- Formation validator library (multi-language)
- Formation linter CLI
- VS Code extension (autocomplete, validation, snippets)
- `mappings/*.md`

---

## v1.0 goals (stability)

- Freeze the **core** standard.
- Guarantee no breaking changes without major version bump.
- Provide a clear migration guide from late v0.x.

`v1.0` scope:

- Formation file shape
- Agent definitions
- MCP server declarations
- A2A service declarations
- Knowledge + secrets blocks
- Extensions surface (namespaced)

---

## Post v1.0 (ecosystem)

- AAIF-managed extension registry (if adoption warrants it).
- Additional language bindings for validators.
- Certification / badges for “Formation-compatible” runtimes.
