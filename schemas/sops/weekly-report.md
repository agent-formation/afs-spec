---
# SOP template -- the id derives from the filename stem (weekly-report).
type: sop                            # REQUIRED literal; activates SOP parsing
name: "Weekly Report"                # Optional; defaults to the file stem
description: "Compile and deliver the weekly activity report"
mode: template                       # template (deterministic) | guide (LLM); default template
tags: reporting, weekly              # Comma-separated or list; used for semantic matching
model: fast                          # Optional default model for all steps (alias or provider/model)
bypass_approval: true                # Default true
synthesis: true                      # Default true
---

# Weekly Report

Compile the weekly activity report and deliver it.

## Steps

1. **Gather activity** [agent:researcher] [mcp:github/search] [parallel]
   Collect the week's merged PRs, closed issues, and open discussions.

2. **Gather metrics** [agent:researcher] [skill:data-analysis] [parallel]
   Pull usage metrics for the week and compute deltas against last week.

3. **Draft the report** [agent:report-writer] [model:premium]
   Combine both inputs into a one-page report following the format in
   [file:templates/weekly-report-format.md]. The [model:premium] directive
   overrides the frontmatter default for this step only.

4. **Deliver** [skill:pdf-processing/render]
   Render the report to PDF and attach it to the response.
