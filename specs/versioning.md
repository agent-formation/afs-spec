# Versioning policy

Agent Formation follows semantic versioning: **MAJOR.MINOR.PATCH**

Every formation file includes:

```yaml
schema: "MAJOR.MINOR.PATCH"
```

---

## Patch releases (x.y.Z)

Patch releases:
- Fix schema bugs or ambiguities.
- Improve docs or fixtures.
- Tighten validation without breaking valid files.

No user-visible breakage expected.

---

## Minor releases (x.Y.z)

Minor releases may add:
- new optional fields
- new schema blocks
- new fixture families

They must remain backward compatible with previous minor versions in the same major line.

---

## Major releases (X.y.z)

Major releases may:
- rename required fields
- remove or restructure blocks
- change meanings in a non-compatible way

Requirements:
- published migration guide
- updated conformance fixtures
- validators support old→new conversion where feasible

---

## Compatibility commitment

- v0.x: allowed to evolve quickly, but avoid breaking changes when possible.
- v1.0+: no breaking changes without major bump.

---

## Deprecation process

1. Mark field/block as deprecated in spec and schema description.
2. Keep it valid for at least one minor line.
3. Remove only in the next major release.
