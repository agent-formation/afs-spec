# Skills Directory

This directory contains agent skills following the [Agent Skills specification](https://agentskills.io/specification).

## Structure

```
skills/
├── example-skill/
│   ├── SKILL.md          # Required: YAML frontmatter + instructions
│   ├── scripts/          # Optional: executable code
│   ├── references/       # Optional: additional documentation
│   └── assets/           # Optional: templates, resources
└── another-skill/
    └── SKILL.md
```

## Usage

Skills must be explicitly declared in the formation or agent configuration:

```yaml
# formation.afs - public skills (all agents)
skills:
  - example-skill

# agents/my-agent.afs - private skills (this agent only)
skills:
  - another-skill
```

## Creating a Skill

1. Create a directory with your skill name (lowercase, hyphens)
2. Add a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: my-skill
description: What this skill does and when to use it
---

# My Skill

Instructions for the agent...
```

3. Optionally add `scripts/`, `references/`, or `assets/` subdirectories

## Community Skills

You can copy skills from [anthropics/skills](https://github.com/anthropics/skills) directly into this directory.
