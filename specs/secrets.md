# Secrets specification

This document defines how Formation handles secrets storage and interpolation.

---

## Overview

Formation uses **encrypted secrets files** to keep sensitive configuration separate from YAML files. This allows formation files to be safely shared and version controlled while keeping API keys, tokens, and credentials secure.

---

## File structure

Every formation directory may contain:

| File | Purpose | Git |
|------|---------|-----|
| `secrets` | Template listing secret keys (KEY=) | Commit |
| `secrets.enc` | Encrypted key-value store | Commit |
| `.key` | Encryption key (Fernet) | **Never commit** |

```
my-formation/
├── formation.yaml    # Safe to share
├── secrets           # Template (KEY= lines)
├── secrets.enc       # Encrypted values
└── .key              # Encryption key (gitignore!)
```

---

## Encryption algorithm

Formation uses **Fernet symmetric encryption** (from the `cryptography` library / `fernet-go`).

### Fernet properties

- **Algorithm**: AES-128-CBC with PKCS7 padding
- **Authentication**: HMAC-SHA256
- **Key size**: 256 bits (32 bytes, base64-encoded)
- **IV**: 128 bits, randomly generated per encryption

### Key generation

```
key = base64url(random_bytes(32))
```

The key is stored in `.key` with restrictive permissions (`0600`).

### Encryption process

1. Serialize secrets as JSON: `{"KEY": "value", ...}`
2. Encrypt with Fernet: `fernet.encrypt(json_bytes, key)`
3. Write ciphertext to `secrets.enc`

### Decryption process

1. Read ciphertext from `secrets.enc`
2. Decrypt with Fernet: `fernet.decrypt(ciphertext, key)`
3. Parse JSON to recover key-value map

---

## Secrets template file

The `secrets` file is a plain-text template listing all secret keys without values:

```
OPENAI_API_KEY=
GITHUB_TOKEN=
DATABASE_URL=
```

This file:
- Can be committed to git (no sensitive data)
- Documents which secrets the formation requires
- Is auto-updated when secrets are added/removed

---

## Referencing secrets in YAML

Use the `${{ secrets.NAME }}` syntax:

```yaml
llm:
  api_keys:
    openai: "${{ secrets.OPENAI_API_KEY }}"

mcp:
  - id: github
    env:
      GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}"
```

### Interpolation rules

- Pattern: `${{ secrets.NAME }}` (whitespace flexible)
- Names are case-insensitive during lookup but normalized to `UPPER_SNAKE_CASE`
- Missing secrets cause a validation/runtime error
- Interpolation happens at formation load time

### Name normalization

Secret names are normalized to uppercase with underscores:

| Input | Normalized |
|-------|------------|
| `my-api-key` | `MY_API_KEY` |
| `openai_key` | `OPENAI_KEY` |
| `GitHubToken` | `GITHUB_TOKEN` |

---

## Security considerations

### What to commit

| File | Commit? | Reason |
|------|---------|--------|
| `formation.yaml` | Yes | No secrets (uses interpolation) |
| `secrets` | Yes | Keys only, no values |
| `secrets.enc` | Yes | Encrypted, safe if key is protected |
| `.key` | **No** | Compromises all secrets |

### Best practices

1. **Add `.key` to `.gitignore`** immediately
2. **Backup `.key` securely** (password manager, vault)
3. **Use restrictive permissions** (`chmod 600 .key`)
4. **Never hardcode secrets** in YAML files
5. **Rotate secrets regularly** by updating `secrets.enc`

### Key loss

If `.key` is lost, `secrets.enc` cannot be decrypted. Recovery requires:
1. Delete both `.key` and `secrets.enc`
2. Regenerate the key
3. Re-enter all secret values

---

## Runtime behavior

At formation load time:

1. Locate `secrets.enc` and `.key` in formation directory
2. Decrypt secrets into memory
3. Scan YAML for `${{ secrets.NAME }}` patterns
4. Replace patterns with decrypted values
5. **Never log or expose** decrypted values

---

## Example workflow

### Initialize secrets

```bash
# Creates .key and empty secrets.enc
muxi secrets init
```

### Add a secret

```bash
# Prompts for value (avoids shell history)
muxi secrets set OPENAI_API_KEY

# Or provide directly
muxi secrets set OPENAI_API_KEY "sk-..."
```

### List secrets

```bash
# Show keys only
muxi secrets list

# Show keys and values (use with caution)
muxi secrets list --with-values
```

### Sync with formation files

```bash
# Scan YAML files, add missing keys, remove unused
muxi secrets sync
```

---

## Cross-runtime compatibility

The Fernet format is implemented identically in:
- **Python**: `cryptography.fernet.Fernet`
- **Go**: `github.com/fernet/fernet-go`

This ensures formations with secrets are portable across runtime implementations.

---

## Environment variables

Formation does **not** read secrets from environment variables by default. This is intentional:

- Keeps formation files self-documenting
- Avoids accidental exposure in logs/process lists
- Ensures consistent behavior across environments

Runtimes may optionally support environment variable fallback via extensions.
