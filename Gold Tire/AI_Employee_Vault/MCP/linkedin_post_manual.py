"""
LinkedIn Post Generator - Manual Mode
Reads approved post and displays it for manual copy-paste to LinkedIn.
"""
from pathlib import Path

def main():
    approved_dir = Path("Approved/LinkedIn")
    
    if not approved_dir.exists():
        print("No Approved/LinkedIn folder found.")
        return
    
    files = list(approved_dir.glob("*.md"))
    if not files:
        print("No approved posts found.")
        return
    
    # Read first approved file
    content = files[0].read_text()
    
    # Extract post content (skip the # LinkedIn Post header and footer)
    lines = content.split("\n")
    post_lines = []
    started = False
    
    for line in lines:
        if line.startswith("# LinkedIn Post"):
            started = True
            continue
        if started and line.startswith("---"):
            break
        if started:
            post_lines.append(line)
    
    post_text = "\n".join(post_lines).strip()
    
    print("=" * 60)
    print("LINKEDIN POST READY FOR MANUAL POSTING")
    print("=" * 60)
    print()
    print(post_text)
    print()
    print("=" * 60)
    print("INSTRUCTIONS:")
    print("1. Copy the text above")
    print("2. Go to linkedin.com")
    print("3. Click 'Start a post'")
    print("4. Paste and publish")
    print("5. Run this script again to mark as done")
    print("=" * 60)

if __name__ == "__main__":
    main()
