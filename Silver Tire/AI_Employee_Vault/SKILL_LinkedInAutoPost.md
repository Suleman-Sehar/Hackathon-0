# SKILL_LinkedInAutoPost

**Objective:** Generate business post and publish via Playwright MCP.

**Trigger:** Command like "Post to LinkedIn: [topic]"

**Steps:**
1. Generate post text (professional, engaging, <280 chars, hashtags)
2. Call linkedin_post.py with message
3. Update Dashboard.md: "LinkedIn post published: [summary]"
4. Log in Logs/[date].md

**Safety:** Max 1 post/day, human review drafts first.
