# SKILL_MetadataManager

**Version:** 1.0
**Created:** 2026-02-24
**Category:** System Utility
**Priority:** High

---

## Overview

Manages file metadata tracking across the AI Employee vault, maintaining an index of all files, their status, priorities, and tags for quick search and dashboard stats.

---

## Responsibilities

1. **Index Creation** - Maintain `metadata_index.json` with all vault files
2. **Auto-Tagging** - Extract tags from file content and naming
3. **Priority Tracking** - Track P1/P2/P3 priorities across plans
4. **Dashboard Stats** - Provide stats for Dashboard.md updates
5. **File Lifecycle** - Track file movement between folders

---

## Metadata Index Structure

```json
{
  "version": "1.0",
  "last_updated": "2026-02-24T10:30:00",
  "files": [
    {
      "path": "Plans/PLAN_20260222_AcmeCorp.md",
      "type": "plan",
      "priority": "P1",
      "tags": ["enterprise", "onboarding"],
      "created": "2026-02-22",
      "status": "active",
      "tasks_total": 5,
      "tasks_completed": 2
    }
  ],
  "stats": {
    "total_files": 15,
    "active_plans": 3,
    "p1_count": 2,
    "p2_count": 1,
    "p3_count": 0
  }
}
```

---

## Workflow

### Step 1: Scan Vault Directories
- Scan all vault folders: Inbox, Needs_Action, Plans, Done, Logs
- Identify new/modified files since last scan
- Extract file metadata (name, path, modified date)

### Step 2: Parse File Content
- Read file frontmatter (YAML between `---`)
- Extract: type, priority, tags, status, created date
- For plans: count tasks and completed tasks

### Step 3: Update Index
- Add new files to `metadata_index.json`
- Update modified files
- Archive completed/deleted files
- Update stats section

### Step 4: Provide Stats
- Return counts for Dashboard.md
- Support queries by tag, priority, type
- Generate summary reports

---

## Usage

### Python Import
```python
from scripts.util_metadata-manager_v1.0 import MetadataManager

manager = MetadataManager()
manager.scan_vault()
stats = manager.get_stats()
```

### Manual Trigger
```bash
python scripts/util_metadata-manager_v1.0.py --scan
```

### Auto-Trigger
- After file processing (SKILL_ProcessInboxFile)
- After plan completion
- Daily at 11 PM (scheduler)

---

## File Types Tracked

| Type | Location | Description |
|------|----------|-------------|
| plan | Plans/ | Action plans with tasks |
| inbox | Inbox/ | Raw incoming files |
| action | Needs_Action/ | Pending action items |
| done | Done/ | Completed work |
| log | Logs/ | Activity logs |
| skill | AI_Employee_Vault/ | Agent skill definitions |

---

## Priority Levels

| Level | Label | Color | Auto-Trigger |
|-------|-------|-------|--------------|
| P1 | Urgent | 🔴 | Immediate human review |
| P2 | High | 🟡 | Next batch processing |
| P3 | Normal | 🟢 | Standard queue |

---

## Tag Extraction Rules

1. **From filename**: `PLAN_AcmeCorp_Onboarding` → tags: `acme-corp`, `onboarding`
2. **From frontmatter**: `tags: [invoice, billing]` → tags: `invoice`, `billing`
3. **From content**: Keywords like "urgent", "asap" → tag: `urgent`

---

## Error Handling

| Error | Action |
|-------|--------|
| Index corrupted | Backup and rebuild from vault scan |
| File unreadable | Log error, skip file, continue |
| Permission denied | Log warning, skip file |

---

## Related Skills

- `SKILL_ProcessInboxFile` - Calls after file processing
- `SKILL_DashboardUpdater` - Provides stats for dashboard
- `SKILL_FileMover` - Updates index on file moves

---

## Success Criteria

- [ ] All vault files indexed
- [ ] Stats accurate and current
- [ ] Dashboard reflects index data
- [ ] Search by tag/priority works
- [ ] Index updated on file changes
