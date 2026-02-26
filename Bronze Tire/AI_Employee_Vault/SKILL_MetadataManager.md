# SKILL: Metadata Manager

**Version:** 1.0  
**Created:** 2026-02-22  
**Category:** Data Management  
**Priority:** High

---

## Overview

This skill manages metadata for all files in the vault using a dual-layer approach:
1. **Sidecar files** (`.meta.json`) - Per-file metadata
2. **Central index** (`metadata_index.json`) - Searchable database of all files

---

## Metadata Schema

### Sidecar File Structure (`filename.meta.json`)

```json
{
  "file_id": "unique-uuid-or-hash",
  "filename": "original_filename.md",
  "path": "/relative/path/to/file.md",
  "created": "2026-02-22T10:30:00Z",
  "modified": "2026-02-22T14:45:00Z",
  "size_bytes": 1024,
  "type": "plan|task|log|note|document",
  "priority": "P1|P2|P3|P4",
  "status": "pending|in_progress|completed|archived",
  "assignee": "person_name",
  "category": "contract|bug|meeting|report|feature|general",
  "tags": ["tag1", "tag2"],
  "due_date": "2026-02-28",
  "source": "/path/to/original/file.md",
  "related_files": ["/path/to/related1.md", "/path/to/related2.md"],
  "custom": {}
}
```

### Central Index Structure (`metadata_index.json`)

```json
{
  "version": "1.0",
  "last_updated": "2026-02-22T14:45:00Z",
  "statistics": {
    "total_files": 100,
    "by_priority": {"P1": 5, "P2": 10, "P3": 80, "P4": 5},
    "by_status": {"pending": 30, "completed": 70},
    "by_category": {"contract": 10, "bug": 20, "meeting": 15}
  },
  "files": [
    {
      "file_id": "abc123",
      "filename": "file.md",
      "path": "/Needs_Action/file.md",
      "priority": "P1",
      "status": "pending",
      "tags": ["urgent", "review"]
    }
  ],
  "tags": ["urgent", "review", "contract"],
  "assignees": ["alice", "bob"],
  "plans": [...],
  "tasks": [...]
}
```

---

## Workflow

### Step 1: Create/Update Sidecar
When a file is created or modified:
1. Check if `.meta.json` sidecar exists
2. Create or update metadata fields
3. Extract tags from content (frontmatter or inline)
4. Set timestamps

### Step 2: Update Central Index
1. Read all sidecar files
2. Aggregate statistics
3. Update file listings
4. Rebuild tag/assignee indexes
5. Write to `metadata_index.json`

### Step 3: Query & Search
Support queries by:
- Priority: `priority:P1`
- Status: `status:pending`
- Assignee: `assignee:alice`
- Category: `category:contract`
- Tags: `tag:urgent`
- Date range: `created:2026-02-20..2026-02-28`

---

## API Functions

### Python Module (`util_metadata-manager.py`)

```python
# Create metadata for a file
meta = MetadataManager.create_sidecar("/path/to/file.md")

# Update metadata
meta.update({"status": "completed", "assignee": "alice"})
meta.save()

# Search files
results = MetadataManager.search("priority:P1 status:pending")

# Get statistics
stats = MetadataManager.get_statistics()

# Get files by tag
files = MetadataManager.get_by_tag("urgent")

# Get files by assignee
files = MetadataManager.get_by_assignee("alice")
```

---

## Integration Points

| Skill | Integration |
|-------|-------------|
| `SKILL_ProcessInboxFile` | Creates sidecar when processing inbox files |
| `SKILL_InboxWatcher` | Tags files with detected priority/category |
| `SKILL_DashboardUpdater` | Reads stats from metadata_index.json |
| `SKILL_TaskExecutor` | Updates task status in sidecar files |

---

## File Naming for Sidecars

```
original_file.md → original_file.md.meta.json
```

Sidecars live next to their parent files in the same directory.

---

## Automation Rules

| Trigger | Action |
|---------|--------|
| New file in Inbox | Create sidecar with `status: new` |
| File moved to Needs_Action | Update sidecar with priority, assignee |
| Plan created | Link source file in `related_files` |
| Task completed | Update `status: completed`, add completion date |
| File archived to Done | Update `status: archived` |

---

## Example Sidecar File

```json
{
  "file_id": "acme-onboarding-20260222",
  "filename": "PLAN_20260222_AcmeCorpOnboarding.md",
  "path": "/Plans/projects/PLAN_20260222_AcmeCorpOnboarding.md",
  "created": "2026-02-22T10:00:00Z",
  "modified": "2026-02-22T10:00:00Z",
  "size_bytes": 2048,
  "type": "plan",
  "priority": "P1",
  "status": "active",
  "assignee": "unassigned",
  "category": "client",
  "tags": ["onboarding", "enterprise", "acme-corp"],
  "due_date": "2026-02-28",
  "source": "/Done/2026/20260222_client_onboarding_acme.md",
  "related_files": [],
  "task_count": 5,
  "custom": {
    "client_name": "Acme Corp",
    "budget": "$5000/month",
    "contact": "John Smith"
  }
}
```

---

## Success Criteria
- [ ] Every file has a corresponding `.meta.json` sidecar
- [ ] Central index updated within 5 seconds of changes
- [ ] Search returns results in <100ms
- [ ] Statistics accurately reflect vault state
- [ ] All skills integrate with metadata system

---

## Related Skills
- `SKILL_ProcessInboxFile` - Processes incoming files
- `SKILL_DashboardUpdater` - Updates dashboard with stats
- `SKILL_FileMover` - Handles file organization
