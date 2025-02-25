#!/usr/bin/env python3
import os
import re

# Adjust these as needed:
CHAPTERS_DIR = "chapters"      # Folder containing your Markdown chapter files
MKDOCS_FILE = "mkdocs.yml"     # MkDocs configuration file to create/update
SITE_NAME = "My Awesome Book"  # Change to your book's title

def get_chapter_title(file_path):
    """
    Returns the first heading (starting with '#' or '##') found in the file.
    Falls back to the filename (without extension) if no heading is found.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^\s*#+\s+(.*)", line)
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
                title = os.path.splitext(filename)[0]
            chapters.append((filename, title))

    # Generate the navigation section for MkDocs config
    nav_lines = []
    for filename, title in chapters:
        nav_lines.append(f"  - {title}: {CHAPTERS_DIR}/{filename}")

    nav_content = "\n".join(nav_lines)

    # Create the mkdocs.yml content with the readthedocs theme
    mkdocs_config = f"""site_name: {SITE_NAME}
nav:
{nav_content}

theme:
  name: readthedocs
"""

    # Write out the updated mkdocs.yml file
    with open(MKDOCS_FILE, "w", encoding="utf-8") as f:
        f.write(mkdocs_config)

    print(f"Updated {MKDOCS_FILE} with {len(chapters)} chapter(s).")

if __name__ == "__main__":
    main()
