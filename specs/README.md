# Formation specifications

This directory contains the normative specification documents for the Formation standard.

## Documents

| File | Description |
|------|-------------|
| `formation.md` | Core Formation standard - components, structure, extension mechanism |
| `versioning.md` | Semantic versioning policy and compatibility guarantees |
| `secrets.md` | Secrets encryption, storage, and interpolation |

## Relationship to schemas

- **Specs** (this directory) define *what* the standard means and *how* it behaves.
- **Schemas** (`/formation`) provide *templates* and *field references* for implementation.

Specs are normative; schemas are the concrete expression of those specs.

## Contributing

When proposing changes:

1. Update the relevant spec document
2. Update corresponding schema templates in `/formation`
3. Add conformance fixtures (when `tests/` is available)
4. Follow the versioning policy in `versioning.md`
