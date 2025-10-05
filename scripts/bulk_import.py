#!/usr/bin/env python3
"""Bulk import memories from text files or JSON backups."""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def import_from_json(file_path: Path, base_url: str, api_key: str | None = None) -> int:
    """
    Import memories from JSON export file.

    Args:
        file_path: Path to JSON file
        base_url: Cognio server URL
        api_key: Optional API key for authentication

    Returns:
        Number of memories imported
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    memories = data.get("memories", [])
    if not memories:
        logger.warning("No memories found in JSON file")
        return 0

    headers = {"X-API-Key": api_key} if api_key else {}
    imported = 0
    duplicates = 0

    for memory in memories:
        try:
            response = requests.post(
                f"{base_url}/memory/save",
                json={
                    "text": memory["text"],
                    "project": memory.get("project"),
                    "tags": memory.get("tags", []),
                },
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            if result.get("duplicate"):
                duplicates += 1
                logger.debug(f"Duplicate: {memory['text'][:50]}...")
            else:
                imported += 1
                logger.info(f"Imported: {result['id']}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to import memory: {e}")
            continue

    logger.info(f"Import complete: {imported} new, {duplicates} duplicates")
    return imported


def import_from_text(
    file_path: Path, base_url: str, project: str | None = None, api_key: str | None = None
) -> int:
    """
    Import memories from plain text file.

    Each non-empty line becomes a separate memory.
    Lines starting with # are treated as comments and skipped.

    Args:
        file_path: Path to text file
        base_url: Cognio server URL
        project: Optional project name
        api_key: Optional API key for authentication

    Returns:
        Number of memories imported
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    headers = {"X-API-Key": api_key} if api_key else {}
    imported = 0
    duplicates = 0

    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        try:
            response = requests.post(
                f"{base_url}/memory/save",
                json={"text": line, "project": project, "tags": ["imported"]},
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            if result.get("duplicate"):
                duplicates += 1
                logger.debug(f"Line {line_num}: Duplicate")
            else:
                imported += 1
                logger.info(f"Line {line_num}: Imported {result['id']}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Line {line_num}: Failed to import - {e}")
            continue

    logger.info(f"Import complete: {imported} new, {duplicates} duplicates")
    return imported


def import_from_markdown(
    file_path: Path, base_url: str, project: str | None = None, api_key: str | None = None
) -> int:
    """
    Import memories from Markdown file.

    Extracts text from Markdown sections and imports each section as a memory.
    Sections are delimited by horizontal rules (---).

    Args:
        file_path: Path to Markdown file
        base_url: Cognio server URL
        project: Optional project name
        api_key: Optional API key for authentication

    Returns:
        Number of memories imported
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by horizontal rules
    sections = [s.strip() for s in content.split("---") if s.strip()]

    headers = {"X-API-Key": api_key} if api_key else {}
    imported = 0
    duplicates = 0

    for idx, section in enumerate(sections, 1):
        # Skip title section
        if section.startswith("# Memory Export"):
            continue

        # Extract text (skip metadata lines)
        lines = section.split("\n")
        text_lines = [
            line
            for line in lines
            if line
            and not line.startswith("##")
            and not line.startswith("**Project**:")
            and not line.startswith("**Tags**:")
            and not line.startswith("**Created**:")
        ]

        if not text_lines:
            continue

        text = "\n".join(text_lines).strip()

        try:
            response = requests.post(
                f"{base_url}/memory/save",
                json={"text": text, "project": project, "tags": ["imported"]},
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            if result.get("duplicate"):
                duplicates += 1
                logger.debug(f"Section {idx}: Duplicate")
            else:
                imported += 1
                logger.info(f"Section {idx}: Imported {result['id']}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Section {idx}: Failed to import - {e}")
            continue

    logger.info(f"Import complete: {imported} new, {duplicates} duplicates")
    return imported


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Bulk import memories into Cognio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import from JSON export
  %(prog)s backup.json

  # Import from text file with project
  %(prog)s notes.txt --project LEARNING

  # Import from Markdown export
  %(prog)s memories.md --format markdown

  # Import with API key
  %(prog)s data.json --api-key your-secret-key

  # Import to custom server
  %(prog)s backup.json --url http://remote-server:8080
        """,
    )

    parser.add_argument("file", type=Path, help="File to import (JSON, TXT, or MD)")
    parser.add_argument(
        "--format",
        choices=["json", "text", "markdown", "auto"],
        default="auto",
        help="Input format (default: auto-detect from extension)",
    )
    parser.add_argument("--project", help="Project name for imported memories")
    parser.add_argument("--url", default="http://localhost:8080", help="Cognio server URL")
    parser.add_argument("--api-key", help="API key for authentication")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Check file exists
    if not args.file.exists():
        logger.error(f"File not found: {args.file}")
        return 1

    # Auto-detect format
    format_type = args.format
    if format_type == "auto":
        suffix = args.file.suffix.lower()
        if suffix == ".json":
            format_type = "json"
        elif suffix == ".md":
            format_type = "markdown"
        elif suffix in [".txt", ".text"]:
            format_type = "text"
        else:
            logger.error(f"Cannot auto-detect format for {suffix} files. Use --format option.")
            return 1

    logger.info(f"Importing from {args.file} (format: {format_type})")

    # Check server is reachable
    try:
        response = requests.get(f"{args.url}/health", timeout=5)
        response.raise_for_status()
        logger.info(f"Connected to Cognio server at {args.url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot connect to Cognio server: {e}")
        return 1

    # Import based on format
    try:
        if format_type == "json":
            imported = import_from_json(args.file, args.url, args.api_key)
        elif format_type == "text":
            imported = import_from_text(args.file, args.url, args.project, args.api_key)
        elif format_type == "markdown":
            imported = import_from_markdown(args.file, args.url, args.project, args.api_key)
        else:
            logger.error(f"Unsupported format: {format_type}")
            return 1

        if imported > 0:
            logger.info(f"Successfully imported {imported} memories")
            return 0
        else:
            logger.warning("No new memories imported")
            return 0

    except Exception as e:
        logger.error(f"Import failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
