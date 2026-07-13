# Knowledge directory

This directory contains **domain knowledge files** that agents can reference for context-aware responses.

## Purpose

Knowledge files provide agents with specialized information about your domain, products, policies, or any other reference material. When enabled, agents can retrieve relevant context from these files to enhance their responses.

## Supported formats

> [!IMPORTANT]
> Specific file format support is implementation-dependent. We recommend runtimes support at minimum: plain text (`.txt`), Markdown (`.md`), HTML (`.html`), and PDF - as well as recursive directory scanning.

At the moment, **MUXI Stack** (the reference implementation) supports:

- **Documents**: PDF, Word (`.docx`), PowerPoint (`.pptx`), Excel (`.xlsx`)
- **Text**: Plain text (`.txt`), Markdown (`.md`), HTML (`.html`)
- **Images**: PNG, JPEG, GIF, WebP (with automatic text extraction)
- **Data**: CSV, JSON, XML
- **Directories**: Containing multiple files of any supported type

## Usage

Reference knowledge sources in agent configurations (`.afs` or `.yaml`):

```yaml
knowledge:
  enabled: true
  sources:
    - path: "knowledge/faq/"
      description: "Frequently asked questions"
    - path: "knowledge/products.txt"
      description: "Product catalog information"
```

## Path rules

- All paths must be **relative** to the formation root
- Absolute paths (`/...`) are rejected
- Parent traversal (`..`) is rejected
- This ensures formations remain self-contained and portable

## Remote sources

Sources may declare a `url` instead of a `path`. Supported schemes: `http(s)://`, `s3://`, `gs://`, `az://`, `rsync://`, `rsync+ssh://`, `ftp://`, `sftp://`, `file://`.

```yaml
knowledge:
  enabled: true
  sources:
    - url: "s3://my-bucket/docs/*.pdf"
      description: "Product documentation"
      auth:
        type: aws
        access_key: "${{ secrets.AWS_ACCESS_KEY }}"
        secret_key: "${{ secrets.AWS_SECRET_KEY }}"
      schedule: "@daily"    # optional re-sync (cron or alias); needs the scheduler
```

Remote content is **mirrored, then ingested**: each source syncs into a runtime-owned local cache (never into the formation directory, which may be read-only) and the ordinary local pipeline runs on the mirror. A failing sync never blocks formation startup or chat — per-file failures keep the previously synced copy.

See [SCHEMA_GUIDE.md](../SCHEMA_GUIDE.md#knowledge-configuration-knowledge) for the full field reference: per-scheme auth types, `include`/`exclude` filters, size limits, archive extraction (`extract:`), and retry policy.

## Organization tips

- Group related content in subdirectories (e.g., `knowledge/faq/`, `knowledge/docs/`)
- Use descriptive filenames
- Keep files focused on specific topics for better retrieval

## Notes

- Knowledge is automatically cached and re-parsed only when sources change
