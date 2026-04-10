from __future__ import annotations

import json
import logging
from pathlib import Path

from byrne_euclid.curriculum import (
    build_manifest,
    load_mapping_entries,
    render_curriculum_preview_markdown,
    render_curriculum_showcase_markdown,
)

logger = logging.getLogger(__name__)

DEMO_MAPPING_PATH = Path("curriculum/demo_curriculum_preview.yaml")
DEMO_ENRICHMENT_PATH = Path("curriculum/demo_curriculum_enrichment.json")
DEMO_MANIFEST_PATH = Path("curriculum/demo_curriculum_manifest.json")
DEMO_MAPPING_DOC_PATH = Path("docs/demo_curriculum_mapping.md")
DEMO_SHOWCASE_DOC_PATH = Path("docs/demo_curriculum_showcase.md")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    entries = load_mapping_entries(DEMO_MAPPING_PATH)
    enrichment_data = json.loads(DEMO_ENRICHMENT_PATH.read_text())
    manifest = build_manifest(entries, oak_data=enrichment_data)

    write_json(DEMO_MANIFEST_PATH, manifest)
    write_text(DEMO_MAPPING_DOC_PATH, render_curriculum_preview_markdown(manifest))
    write_text(
        DEMO_SHOWCASE_DOC_PATH,
        render_curriculum_showcase_markdown(manifest, title="Demo curriculum showcase"),
    )

    logger.info("Wrote demo manifest to %s", DEMO_MANIFEST_PATH)
    logger.info("Wrote demo mapping document to %s", DEMO_MAPPING_DOC_PATH)
    logger.info("Wrote demo showcase document to %s", DEMO_SHOWCASE_DOC_PATH)


if __name__ == "__main__":
    main()
