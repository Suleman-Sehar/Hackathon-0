# SKILL_GmailWatcher

## Objective
Monitor the `Needs_Action` folder for new Gmail-related files, analyze incoming requests, and generate a structured `Plan.md` document outlining the required actions.

## Step-by-Step Instructions

1. **Scan Needs_Action Folder**
   - Check `Needs_Action/` directory for new files
   - Identify files containing Gmail-related content (subject lines, sender info, email body)

2. **Parse Email Content**
   - Extract sender name and email address
   - Extract subject line
   - Extract email body/purpose
   - Identify urgency level and required response type

3. **Generate Plan.md**
   - Create `Plan.md` in the same folder or `Pending_Approval/`
   - Structure:
     ```markdown
     # Action Plan

     ## Email Summary
     - From: [sender]
     - Subject: [subject]
     - Priority: [High/Medium/Low]

     ## Required Actions
     1. [Action item 1]
     2. [Action item 2]

     ## Recommended Response
     [Draft response or action notes]

     ## Status
     - [ ] Awaiting Approval
     - [ ] Ready to Execute
     ```

4. **Log Activity**
   - Record processed file in `Dashboard.md` or activity log
   - Mark original file as processed

## How to Trigger

- **Automatic:** File watcher detects new file in `Needs_Action/` folder
- **Manual:** Run command `skill: "SKILL_GmailWatcher"` or execute the GmailWatcher script
- **Scheduled:** Set interval check (e.g., every 5 minutes) for new emails
