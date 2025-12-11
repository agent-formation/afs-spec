# Contributing

Thanks for helping improve the Agent Formation Standard.

---

## What to contribute

We welcome contributions to:

1. **Schemas**
   - New fields that are neutral and portable.
   - Clarifications or bug fixes.
2. **Spec**
   - Explanations, examples, edge cases.
3. **Templates**
   - Better starter Formations and agents.
4. **Fixtures**
   - Valid and invalid conformance cases.
5. **Tooling**
   - Validator improvements, error messages, CI.

---

## Principles to preserve

Before proposing changes, please confirm your idea respects:

- **Portability:** the schema can be implemented by any runtime.
- **Backwards compatibility:** no breaking changes in minor/patch releases.
- **Neutrality:** no vendor-specific assumptions in the core standard.
- **Simplicity:** common cases should stay easy.

If a feature is vendor-specific, put it behind the extensions mechanism.

---

## Change process

1. **Open an issue**
   - describe the problem and proposal
   - include examples
2. **Discuss**
   - maintainers and community will help refine the approach
3. **Open a PR**
   - include schema/spec updates
   - include fixture updates
   - update docs

---

## PR checklist

Your PR should include:

- [ ] Schema updates (`schemas/**`)
- [ ] Spec updates (`specs/**`) if behavior changes
- [ ] Updated templates if relevant
- [ ] Fixtures demonstrating valid/invalid cases
- [ ] No breaking changes unless bumping major version
- [ ] Clear release notes in PR description

---

## File extensions

Agent Formation supports two file extensions:

- `.afs` — Agent Formation Schema (recommended)
- `.yaml` — Standard YAML extension

Both are fully supported. Use `.afs` for clarity in projects with multiple YAML files.

---

## Releases

- Patch: fixes, clarifications, fixture expansion.
- Minor: backward-compatible additions.
- Major: breaking changes and migration notes.

Releases are tagged and published with a changelog.

---

## Developer certificate of origin (DCO)

All contributions must be signed off.

Add this to your commit message:

```
Signed-off-by: Your Name <your@email>
```

This indicates you have the right to submit the work under Apache-2.0.
