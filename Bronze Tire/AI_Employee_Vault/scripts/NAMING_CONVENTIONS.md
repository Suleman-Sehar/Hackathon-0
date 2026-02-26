# File Naming Conventions

Standardized naming ensures easy sorting, searching, and automation.

---

## General Rules

1. **Use ISO 8601 dates**: `YYYY-MM-DD`
2. **Use underscores or hyphens**: `_` or `-` (be consistent)
3. **Lowercase preferred**: Avoid spaces and special characters
4. **Be descriptive**: Include context, type, and version if needed

---

## Inbox/ — Incoming Files

Files dropped here are unprocessed. Include source and date.

```
YYYY-MM-DD_source_description.ext
```

**Examples:**
- `2026-02-22_email_client-request.pdf`
- `2026-02-22_slack_team-update.txt`
- `2026-02-22_web_article-ai-trends.md`
- `2026-02-22_upload_budget-draft.xlsx`

---

## Needs_Action/ — Pending Items

Add priority level and assignee.

```
YYYY-MM-DD_priority_assignee_description.ext
```

**Priority codes:** `P1` (urgent), `P2` (high), `P3` (normal), `P4` (low)

**Examples:**
- `2026-02-22_P1_alice_contract-review.docx`
- `2026-02-21_P2_bob_bug-investigation.md`
- `2026-02-20_P3_team_meeting-notes.md`
- `2026-02-19_P4_ai_data-cleanup.csv`

---

## Plans/ — Strategic Documents

Include plan type and status.

```
plan-type_subject_status_version.ext
```

**Plan types:** `roadmap`, `project`, `feature`, `research`, `idea`

**Status:** `draft`, `active`, `on-hold`, `approved`

**Examples:**
- `roadmap_q2-2026_active_v2.md`
- `project_website-redesign_draft_v1.md`
- `feature_user-auth_approved_v3.md`
- `idea_ai-summarizer_research.md`

---

## Done/ — Completed Work

Include completion date and original reference.

```
YYYY-MM-DD_completed_original-ref.ext
```

**Examples:**
- `2026-02-22_completed_2026-02-20_contract-final.pdf`
- `2026-02-21_completed_2026-02-18_bugfix-login.md`
- `2026-02-20_completed_2026-02-15_campaign-results.xlsx`

---

## Logs/ — Activity Records

Include log type and date range.

```
log-type_YYYY-MM-DD_to_YYYY-MM-DD.ext
```

**Log types:** `activity`, `error`, `run`, `audit`

**Examples:**
- `activity_2026-02-22_to_2026-02-28.log`
- `error_2026-02-20.log`
- `run_watcher-script_2026-02-22.log`
- `audit_2026-02-01_to_2026-02-28.csv`

---

## scripts/ — Automation Code

Include script purpose and version.

```
purpose_component_vX.X.ext
```

**Examples:**
- `watcher_inbox-monitor_v1.0.py`
- `util_file-mover_v0.5.py`
- `report_weekly-summary_v2.1.py`
- `config_settings-loader_v1.0.py`

---

## Quick Reference Table

| Folder | Pattern | Example |
|--------|---------|---------|
| Inbox/ | `YYYY-MM-DD_source_desc.ext` | `2026-02-22_email_report.pdf` |
| Needs_Action/ | `YYYY-MM-DD_P#_assignee_desc.ext` | `2026-02-22_P1_alice_review.md` |
| Plans/ | `type_subject_status.ext` | `roadmap_q2_active.md` |
| Done/ | `YYYY-MM-DD_completed_orig.ext` | `2026-02-22_completed_feb20-report.xlsx` |
| Logs/ | `type_date-range.ext` | `activity_2026-02-22_to_28.log` |
| scripts/ | `purpose_component_vX.X.py` | `watcher_inbox_v1.0.py` |

---

## Automation Tags (Optional)

Add tags in filenames for script-based routing:

- `[AUTO]` — Can be auto-processed
- `[MANUAL]` — Requires human review
- `[URGENT]` — High priority flag

**Example:** `2026-02-22_[AUTO]_invoice-process.pdf`
