# SKILL_LinkedInPost

## Objective

Generate professional business posts and automatically publish them to LinkedIn using Playwright browser automation.

## Step-by-Step Instructions

1. **Receive Post Request**
   - Read post topic/theme from `Needs_Action/` or `Approved/LinkedIn/` folder
   - Extract key points, hashtags, and any media references
   - Verify post has business value (per Company Handbook rules)

2. **Generate Post Content**
   - Craft engaging professional content (280-1300 characters optimal)
   - Include relevant hashtags (3-5 recommended)
   - Add call-to-action if appropriate
   - Format with line breaks for readability
   - Ensure content aligns with business value guidelines

3. **Prepare Playwright Script**
   - Launch browser with persistent context (user_data_dir = "linkedin_session")
   - Navigate to `linkedin.com`
   - Check if already logged in (session persistence)
   - If not logged in, wait for manual login (first time only)

4. **Execute Post Publication**
   - Click "Start a post" button on homepage
   - Insert generated content into post composer
   - Attach media if specified (images, documents)
   - Click "Post" to publish
   - Wait for confirmation that post was published

5. **Confirm and Log**
   - Verify post was published successfully
   - Capture post URL if available
   - Log activity in `Dashboard.md` under "LinkedIn Posts Today"
   - Move request file to `Done/` folder
   - Update metadata index if configured

## How to Trigger

- **Automatic:** New file appears in `Approved/LinkedIn/` folder with approved marker
- **Manual:** Run command `skill: "SKILL_LinkedInPost"` with post parameters
- **Scheduled:** Weekly/monthly recurring posts configured in scheduler

## Prerequisites

- LinkedIn credentials stored securely in vault (for first-time login)
- Playwright installed: `pip install playwright`
- Browser binaries installed: `playwright install chromium`
- Session folder created: `linkedin_session/`

## Safety Rules

- Only post business value content (per Company Handbook)
- Never post sensitive company information
- Always log posts in Dashboard
- Require approval for controversial or high-impact topics

## Integration Points

- Called by `SKILL_HumanApproval` for sensitive topics
- Logs to `Dashboard.md` LinkedIn Posts Today section
- Uses `Silver Tire/mcp/linkedin_post.py` script for automation
