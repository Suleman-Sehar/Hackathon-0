# SKILL_HumanApproval

## Objective
Route sensitive or high-impact actions to human review by creating pending approval files in the `Pending_Approval/` folder, ensuring critical decisions receive proper oversight.

## Step-by-Step Instructions

1. **Identify Actions Requiring Approval**
   - Financial transactions above threshold
   - External communications to new contacts
   - System configuration changes
   - Content publishing to public platforms
   - Any action flagged by other skills as "sensitive"

2. **Create Approval Request File**
   - Generate timestamped file in `Pending_Approval/` folder
   - Naming convention: `YYYYMMDD_HHMMSS_<ActionType>.md`
   - Include structured content:
     ```markdown
     # Approval Request

     ## Requested Action
     [Clear description of what will be done]

     ## Reason/Context
     [Why this action is needed]

     ## Impact Assessment
     - Risk Level: [Low/Medium/High]
     - Affected Systems: [List]
     - Reversible: [Yes/No]

     ## Proposed Details
     [Specific parameters, recipients, content, etc.]

     ## Recommended By
     [AI Agent name / Skill that generated this]

     ## Approval Status
     - [ ] Pending
     - [ ] Approved
     - [ ] Rejected

     ## Approved By: ________________
     ## Date: ________________
     ## Notes: ________________
     ```

3. **Notify Human Supervisor**
   - Send notification (email, Slack, etc.) about pending approval
   - Include file location and urgency level

4. **Monitor for Decision**
   - Watch for file movement to `Approved/` or `Rejected/`
   - Update internal task queue based on decision

5. **Execute or Archive**
   - If approved: Trigger the requested action skill
   - If rejected: Move to `Rejected/` with notes, log reason

## How to Trigger

- **Automatic:** Other skills call this skill when sensitivity threshold is exceeded
- **Manual:** Run command `skill: "SKILL_HumanApproval"` with action details
- **Policy-Based:** Configured rules auto-trigger for specific action types

## Integration Points

- Called by `SKILL_SendEmailMCP` for new external contacts
- Called by `SKILL_LinkedInAutoPost` for sensitive topics
- Called by any skill with `requires_approval: true` flag
