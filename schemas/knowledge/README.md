# Knowledge directory

This directory contains **domain knowledge files** that agents can reference for context-aware responses.

## Purpose

Knowledge files provide agents with specialized information about your domain, products, policies, or any other reference material. When enabled, agents can retrieve relevant context from these files to enhance their responses.

## Supported formats

- Plain text (`.txt`)
- Markdown (`.md`)
- Directories containing multiple files

## Usage

Reference knowledge sources in agent configurations:

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

## Organization tips

- Group related content in subdirectories (e.g., `knowledge/faq/`, `knowledge/docs/`)
- Use descriptive filenames
- Keep files focused on specific topics for better retrieval

## Notes

- Knowledge is automatically cached and re-parsed only when sources change
- Remote sources (S3, HTTP) are planned for a future release
