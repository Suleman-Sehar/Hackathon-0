# Sub-Folder Structure Guide

Organized sub-folders for better categorization and retrieval.

---

## 📁 Plans/

Strategic documents organized by type.

```
Plans/
├── roadmaps/          # Long-term strategic roadmaps
│   └── roadmap_q2-2026_active_v2.md
├── projects/          # Specific project plans
│   └── project_website-redesign_draft_v1.md
├── features/          # Feature specifications
│   └── feature_user-auth_approved_v3.md
├── research/          # Research documents & findings
│   └── ai-trends-analysis_2026.md
└── ideas/             # Brainstorming & future concepts
    └── ai-summarizer-concept.md
```

### Usage Rules
| Sub-folder | When to Use | Retention |
|------------|-------------|-----------|
| `roadmaps/` | Quarterly/annual planning | Keep active + 4 quarters |
| `projects/` | Multi-week initiatives | Archive to Done/ when complete |
| `features/` | Feature specs & requirements | Keep while feature is active |
| `research/` | Investigation & analysis | Keep indefinitely |
| `ideas/` | Early-stage concepts | Review monthly, prune stale |

---

## 📁 Logs/

Activity records organized by log type.

```
Logs/
├── activity/          # General activity logs
│   └── activity_2026-02-22_to_2026-02-28.log
├── errors/            # Error reports & stack traces
│   └── error_2026-02-20.log
├── runs/              # Script execution logs
│   └── run_watcher_2026-02-22.log
└── audits/            # Security & compliance audits
    └── audit_2026-02-01_to_2026-02-28.csv
```

### Usage Rules
| Sub-folder | When to Use | Retention |
|------------|-------------|-----------|
| `activity/` | Daily operations | 90 days rolling |
| `errors/` | Any error or exception | 1 year |
| `runs/` | Script executions | 30 days |
| `audits/` | Compliance & security | 2 years |

### Log Rotation
- **Daily**: New error logs created each day with errors
- **Weekly**: Activity logs span Monday-Sunday
- **Monthly**: Audit logs cover full calendar month

---

## 📁 Done/

Completed work organized by year and archive.

```
Done/
├── 2026/              # Current year completions
│   ├── Q1/
│   │   ├── 2026-02-22_completed_contract-final.pdf
│   │   └── 2026-03-15_completed_campaign-results.xlsx
│   ├── Q2/
│   ├── Q3/
│   └── Q4/
└── archive/           # Historical reference (older than 2 years)
    ├── 2024/
    └── 2025/
```

### Usage Rules
| Sub-folder | When to Use | Access Pattern |
|------------|-------------|----------------|
| `2026/` | Current year completions | Frequent reference |
| `2026/Q1/` | Quarterly sub-divisions | Organize by completion date |
| `archive/` | Items > 2 years old | Rare reference |

### Quarterly Organization
Files in year folders are further organized by quarter:
- **Q1**: Jan-Mar → `Done/2026/Q1/`
- **Q2**: Apr-Jun → `Done/2026/Q2/`
- **Q3**: Jul-Sep → `Done/2026/Q3/`
- **Q4**: Oct-Dec → `Done/2026/Q4/`

---

## 🔄 Automated Routing Rules

Scripts should use these routing rules:

| Source | Condition | Destination |
|--------|-----------|-------------|
| Inbox/ | File detected | → Needs_Action/ |
| Needs_Action/ | Marked complete | → Done/2026/Q{N}/ |
| Plans/projects/ | Status = "complete" | → Done/2026/Q{N}/ |
| Logs/errors/ | Age > 365 days | → Done/archive/ |
| Logs/activity/ | Age > 90 days | Delete |

---

## 📋 Quick Reference

| Folder | Sub-folders | Purpose |
|--------|-------------|---------|
| `Plans/` | roadmaps, projects, features, research, ideas | Strategic docs |
| `Logs/` | activity, errors, runs, audits | Activity records |
| `Done/` | {year}/{quarter}, archive | Completed work |

---

*Created: 2026-02-22 | Version: 1.0*
