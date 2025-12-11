# Agent Formation Project Charter

## Mission

The Agent Formation project provides a **vendor-neutral, declarative configuration standard** for AI agents and multi-agent systems. Our mission is to enable portable, interoperable agent definitions that can be validated consistently and run on any compliant runtime.

## Scope

### In scope

- **Agent Formation Schema (AFS)**: Core schema definitions for formations, agents, MCP tool servers, and A2A services.
- **Specification documents**: Normative text describing schema behavior, versioning, and extension mechanisms.
- **Conformance fixtures**: Valid and invalid test cases for validator implementations.
- **Reference tooling**: Validator library, linter CLI, and editor extensions.
- **Mappings**: Documentation mapping Agent Formation concepts to other agent ecosystems.

### Out of scope

- Specific runtime implementations (e.g., MUXI Runtime is a separate project).
- Proprietary or commercial extensions.
- Agent behavior, safety, or alignment policies (those are implementation concerns).

## Principles

1. **Portability**: Schemas must be implementable by any runtime without vendor lock-in.
2. **Neutrality**: The core standard must not favor any specific vendor or implementation.
3. **Backward compatibility**: No breaking changes within a major version line.
4. **Simplicity**: Common use cases should be easy; advanced features should be possible.
5. **Transparency**: All decisions are made in the open with community input.

## Governance

The project follows a lazy consensus model with maintainer oversight. See `GOVERNANCE.md` for details on roles, decision-making, and voting procedures.

## Intellectual property

All contributions are made under the Apache License 2.0. Contributors must sign off their commits per the Developer Certificate of Origin (DCO).

## Community

- **Code of Conduct**: All participants must follow `CODE_OF_CONDUCT.md`.
- **Contributing**: See `CONTRIBUTING.md` for how to participate.
- **Security**: Report vulnerabilities per `SECURITY.md`.

## Relationship to Linux Foundation

Agent Formation is intended to be contributed to the Linux Foundation. Upon acceptance, governance and IP policies will align with Linux Foundation requirements.
