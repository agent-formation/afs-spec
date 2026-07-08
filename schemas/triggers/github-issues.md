---
# Trigger template -- the id derives from the filename stem (github-issues).
# All keys below are optional; unknown keys are a load-time error.

name: "GitHub issue intake"          # Display-name override (defaults to the id)
type: webhook                        # Free-form type annotation (semantic only)

# Inbound channel name for source tracking. Lets proactive notifications
# route back to the user's most recent inbound channel ("last" target).
channel: github

# Model override for this trigger's turn: an llm.aliases name or a
# fully qualified provider/model string. Most-specific-wins hierarchy;
# see specs/formation.md section 4.1.
model: fast

# Payload extraction spec. Values are JSONPath-style paths ($.a.b, a.b.c,
# list indices). Extraction is best-effort: a missing path yields no value.
# Allowed keys: message, user_id, files (paths) and context (name -> path map).
parse:
  message: $.issue.title             # the user-visible message for the turn
  user_id: $.sender.login            # request identity (converted to string)
  context:                           # platform values, exposed to transformers
    repo: $.repository.full_name     # available as ${{ context.repo }}
    issue_url: $.issue.html_url

# Outbound delivery. webhook: and transformer: COMPOSE (not mutually
# exclusive):
#   webhook only      -> raw standard payload to this URL
#   transformer only  -> formatted payload to the transformer's endpoint.url
#   both              -> formatted payload to THIS webhook URL (trigger wins)
# Referencing a transformer with no URL from either side is a load error.
transformer: slack                   # transformers/slack.yaml or bundled template
webhook: "${{ secrets.OPS_SLACK_WEBHOOK }}"
---

A new GitHub issue arrived in ${{ data.repository.full_name }}.

Title: ${{ data.issue.title }}
Body: ${{ data.issue.body }}

Triage the issue: classify it (bug, feature, question), assess severity,
and produce a two-sentence summary with a recommended next action.
