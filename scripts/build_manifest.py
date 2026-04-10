from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

from byrne_euclid.curriculum import (
    build_manifest,
    load_mapping_entries,
    render_curriculum_mapping_markdown,
)

logger = logging.getLogger(__name__)


def load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        logger.info("No Oak cache found at %s; building manifest from YAML only", path)
        return None
    return json.loads(path.read_text())


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the curriculum manifest and the human-readable mapping document"
    )
    parser.add_argument(
        "--mapping",
        default="curriculum/euclid_to_oak.yaml",
        help="Path to the hand-maintained Euclid-to-curriculum YAML mapping",
    )
    parser.add_argument(
        "--oak-data",
        default="curriculum/oak_geometry_data.json",
        help="Optional Oak cache JSON used to enrich keywords and misconceptions",
    )
    parser.add_argument(
        "--output",
        default="curriculum/curriculum_manifest.json",
        help="Where to write the generated manifest JSON",
    )
    parser.add_argument(
        "--docs-output",
        default="docs/curriculum_mapping.md",
        help="Where to write the generated curriculum mapping markdown",
    )
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args()

    mapping_path = Path(args.mapping)
    oak_data_path = Path(args.oak_data)
    output_path = Path(args.output)
    docs_output_path = Path(args.docs_output)

    entries = load_mapping_entries(mapping_path)
    manifest = build_manifest(entries, oak_data=load_optional_json(oak_data_path))
    markdown = render_curriculum_mapping_markdown(manifest)

    write_json(output_path, manifest)
    write_text(docs_output_path, markdown)

    logger.info("Wrote manifest to %s", output_path)
    logger.info("Wrote curriculum mapping document to %s", docs_output_path)


if __name__ == "__main__":
    main()
