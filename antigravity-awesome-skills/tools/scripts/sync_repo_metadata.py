#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys

from update_readme import configure_utf8_output, find_repo_root, load_metadata, update_readme


ABOUT_DESCRIPTION_RE = re.compile(r'"description"\s*:\s*"([^"]*)"')


def update_package_description(base_dir: str, metadata: dict, dry_run: bool) -> bool:
    package_path = os.path.join(base_dir, "package.json")
    with open(package_path, "r", encoding="utf-8") as file:
        content = file.read()

    new_description = (
        f"{metadata['total_skills_label']} agentic skills for Claude Code, Gemini CLI, "
        "Cursor, Antigravity & more. Installer CLI."
    )
    updated_content = ABOUT_DESCRIPTION_RE.sub(
        f'"description": "{new_description}"', content, count=1
    )

    if updated_content == content:
        return False

    if dry_run:
        print(f"[dry-run] Would update package description in {package_path}")
        return True

    with open(package_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(updated_content)
    print(f"✅ Updated package description in {package_path}")
    return True


def print_manual_github_about(metadata: dict) -> None:
    description = (
        f"{metadata['total_skills_label']} curated SKILL.md files for Claude Code, "
        "Cursor, Gemini CLI, Codex, Copilot, and Antigravity."
    )
    print("\nManual GitHub repo settings update:")
    print(f"- About description: {description}")
    print("- Suggested topics: claude-code, cursor, gemini-cli, codex-cli, github-copilot, antigravity")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize repository metadata across README and package.json."
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview updates without writing files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = find_repo_root(os.path.dirname(__file__))
    metadata = load_metadata(base_dir)

    print("Repository metadata")
    print(json.dumps(metadata, indent=2))

    readme_metadata = update_readme(dry_run=args.dry_run)
    package_updated = update_package_description(base_dir, metadata, args.dry_run)
    print_manual_github_about(readme_metadata)

    if args.dry_run and not package_updated:
        print("\n[dry-run] No package.json description changes required.")

    return 0


if __name__ == "__main__":
    configure_utf8_output()
    sys.exit(main())
