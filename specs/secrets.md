# Secrets specification

This document defines how Agent Formation handles secrets interpolation in formation files.

---

## Overview

Formation files reference secrets using a standard syntax. This allows formation files to be safely shared and version controlled while keeping API keys, tokens, and credentials secure.

> [!IMPORTANT]
> How secrets are stored, encrypted, and managed is implementation-defined. This specification only defines the interpolation syntax and behavioral requirements.

---

## Secrets syntax

Reference secrets in formation files using:

```yaml
key: "${{ secrets.SECRET_NAME }}"
```

### Examples

```yaml
llm:
  api_keys:
    openai: "${{ secrets.OPENAI_API_KEY }}"

mcp:
  - id: github
    env:
      GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}"

server:
  api_keys:
    admin_key: "${{ secrets.ADMIN_API_KEY }}"
```

---

## Interpolation rules

### Pattern matching
- Pattern: `${{ secrets.NAME }}` (whitespace inside braces is flexible)
- The `$` prefix is required
- Double braces `{{` and `}}` are required

### Name normalization
Secret names SHOULD be normalized to uppercase with underscores:

| Input | Normalized |
|-------|------------|
| `my-api-key` | `MY_API_KEY` |
| `openai_key` | `OPENAI_KEY` |
| `GitHubToken` | `GITHUB_TOKEN` |

### Resolution timing
- Secrets MUST be interpolated at formation load time
- Missing secrets MUST cause a validation or runtime error
- Runtimes MUST NOT proceed with unresolved secret references

---

## User credentials

In addition to formation-wide secrets, Agent Formation supports per-user credentials:

```yaml
key: "${{ user.credentials.SERVICE_NAME }}"
```

### Differences from secrets

| Aspect | Secrets | User Credentials |
|--------|---------|------------------|
| Scope | Formation-wide | Per-user |
| Loading | At initialization | On-demand |
| Isolation | Shared | User-isolated |

### Example

```yaml
mcp_servers:
  - id: "github"
    auth:
      type: "bearer"
      token: "${{ user.credentials.github }}"
```

---

## Security requirements

Runtimes implementing Agent Formation MUST:

1. **Never log or expose** decrypted secret values
2. **Never include** secrets in error messages or stack traces
3. **Interpolate in memory** — never write decrypted values to disk
4. **Isolate user credentials** — one user's credentials must never be accessible to another

Runtimes SHOULD:

1. Support secure secret storage (encrypted at rest)
2. Provide CLI tooling for secret management
3. Support environment variable fallback (optional)

---

## Portability

Formation files using `${{ secrets.NAME }}` syntax are portable across any AFS-compliant runtime. The runtime is responsible for providing the secret values through its own storage mechanism.

Common implementation approaches include:
- Encrypted file storage (e.g., `secrets.enc`)
- External secret managers (HashiCorp Vault, AWS Secrets Manager)
- Environment variables
- Platform-specific credential stores

---

## Best practices

1. **Use descriptive names**: `OPENAI_API_KEY` not `KEY1`
2. **Never commit secrets**: Formation files should only contain references, not values
3. **Document required secrets**: List all required secrets in your README
4. **Rotate regularly**: Update secrets periodically for security

---

## Implementations

- [**MUXI Stack**](https://github.com/muxi-ai/muxi) — Reference implementation using Fernet-encrypted file storage
