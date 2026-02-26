# SKILL: Process Inbox File

**Version:** 1.0  
**Created:** 2026-02-22  
**Category:** Inbox Processing  
**Priority:** High

---

## Overview

This skill processes incoming files from the `/Needs_Action/` folder by analyzing content, creating actionable plans, and archiving completed work.

---

## Workflow

### Step 1: Read /Needs_Action/
- Scan `/Needs_Action/` directory for unprocessed files
- Read each file's content fully
- Identify file type (text, code, data, etc.)
- Extract key information:
  - Subject/Topic
  - Action items
  - Deadlines (if any)
  - Priority indicators

### Step 2: Summarize Content
- Create a concise summary (3-5 bullet points)
- Identify the core purpose of the file
- Note any dependencies or related files
- Flag urgent items requiring immediate attention

### Step 3: Create Plan.md
- Generate a new plan file in `/Plans/projects/` or `/Plans/`
- Naming convention: `PLAN_[YYYYMMDD]_[Topic].md`
- Include sections:
  - **Overview:** Brief description
  - **Summary:** From Step 2
  - **Tasks:** Actionable items with priorities
  - **Timeline:** Deadlines if applicable
  - **Status:** Pending/In Progress/Completed
  - **Source:** Link to original file location

### Step 4: Move to /Done/
- Move processed file from `/Needs_Action/` to `/Done/[YYYY-MM]/`
- Use naming convention: `[YYYYMMDD]_original_filename.md`
- Update any internal links if necessary
- Log the move action in `/Logs/activity/`

### Step 5: Update Dashboard
- Increment "Pending Tasks" count if new tasks created
- Add new plan to "Today's Priorities" section
- Update "Last Updated" timestamp to current date
- Log skill execution in `/Logs/runs/`

---

## File Naming Conventions

| Location | Pattern | Example |
|----------|---------|---------|
| Plans | `PLAN_[YYYYMMDD]_[Topic].md` | `PLAN_20260222_ClientOnboarding.md` |
| Done | `[YYYYMMDD]_[original].md` | `20260222_meeting_notes.md` |
| Logs | `[YYYY-MM-DD].md` | `2026-02-22.md` |

---

## Example Output

### Plan.md Template
```markdown
# PLAN: [Topic Name]

**Created:** YYYY-MM-DD
**Status:** Active
**Source:** /Needs_Action/[original_file.md]

---

## Summary
- Key point 1
- Key point 2
- Key point 3

---

## Tasks
### Task 1: [Description]
- **Priority:** P1/P2/P3
- **Status:** Pending
- **Due:** [Date if applicable]

---

## Progress
- [ ] Task 1: [Description]

**Total:** X tasks | **Completed:** 0 | **Pending:** X
```

---

## Error Handling

| Error | Action |
|-------|--------|
| File unreadable | Log to `/Logs/errors/`, move to `/Inbox/` for manual review |
| No clear action items | Summarize and archive to `/Done/archive/` |
| Duplicate file | Log warning, skip processing |

---

## Related Skills
- `SKILL_InboxWatcher` - Monitors inbox for new files
- `SKILL_FileMover` - Handles file organization
- `SKILL_DashboardUpdater` - Updates main dashboard

---

## Success Criteria
- [ ] All files in `/Needs_Action/` processed
- [ ] Plans created for actionable items
- [ ] Files archived correctly in `/Done/`
- [ ] Dashboard reflects current state
- [ ] Actions logged appropriately
