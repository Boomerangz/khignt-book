#!/usr/bin/env python3
import os
import re

# Adjust these as needed:
CHAPTERS_DIR = "chapters"  # folder containing your Markdown chapter files
README_FILE = "README.md"  # README file to update

def get_chapter_title(file_path):
    """
    Returns the first '##' heading found in the file.
    If none is found, returns None.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Look for a line that starts with "## " (ignoring leading whitespace)
            match = re.match(r"^\s*##\s+(.*)", line)
            if match:
                return match.group(1).strip()
    return None

def main():
    chapters = []

    # List all markdown files in CHAPTERS_DIR (ignoring hidden files)
    for filename in sorted(os.listdir(CHAPTERS_DIR)):
        if filename.lower().endswith(".md"):
            file_path = os.path.join(CHAPTERS_DIR, filename)
            title = get_chapter_title(file_path)
            if not title:
                # Fallback to the filename if no heading is found
                title = os.path.splitext(filename)[0]
            chapters.append((filename, title))

    # Generate a Markdown list of chapters with links
    chapter_lines = []
    for filename, title in chapters:
        # The link will point to the file in the chapters folder.
        chapter_lines.append(f"- [{title}]({CHAPTERS_DIR}/{filename})")
    toc = "\n".join(chapter_lines)

    # Define markers to allow updating only the TOC section in README.md
    start_marker = "<!-- CHAPTERS START -->"
    end_marker = "<!-- CHAPTERS END -->"
    new_section = f"{start_marker}\n{toc}\n{end_marker}"

    # Read existing README.md content if it exists
    if os.path.exists(README_FILE):
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = ""

    # Replace the chapter list between markers if they exist; otherwise, append it.
    if start_marker in content and end_marker in content:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        new_content = pattern.sub(new_section, content)
    else:
        # Optionally, you can prepend or append the new section.
        new_content = content.strip() + "\n\n" + new_section + "\n"

    # Write out the updated README.md
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated {README_FILE} with {len(chapters)} chapter link(s).")

if __name__ == "__main__":
    main()
