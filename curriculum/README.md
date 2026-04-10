# Curriculum data

This directory holds the hand-maintained curriculum mapping and any cached Oak National Academy API responses used to enrich it.

## Files

- `euclid_to_oak.yaml` — the source-of-truth mapping from scene class to Euclid reference, national curriculum references, and draft Oak linkage
- `curriculum_manifest.json` — generated JSON manifest for programmatic consumers
- `oak_*.json` — cached Oak API responses written by `scripts/fetch_oak_curriculum.py`
- `demo_curriculum_preview.yaml` — hand-authored synthetic preview entries for demoing the final enriched output shape
- `demo_curriculum_enrichment.json` — hand-authored synthetic lesson-summary data used to enrich the demo preview
- `demo_curriculum_manifest.json` — generated JSON preview built from the synthetic demo inputs

## Attribution

Contains public sector information licensed under the Open Government Licence v3.0.

Oak National Academy content is used under the Open Government Licence. When lesson content or curriculum metadata from Oak informs downstream artefacts, include an attribution statement linking to the OGL:

- https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

## Update workflow

1. Refresh Oak cache data with `uv run --env-file .env python scripts/fetch_oak_curriculum.py` using `OAK_OPEN_API_KEY` or `OAK_API_KEY`
2. Review or adjust `curriculum/euclid_to_oak.yaml`
3. Rebuild the manifest and curriculum document with `uv run python scripts/build_manifest.py`

## Demo preview workflow

When live Oak auth is unavailable, you can still preview the final enriched shape:

1. Review or adjust `curriculum/demo_curriculum_preview.yaml`
2. Review or adjust `curriculum/demo_curriculum_enrichment.json`
3. Rebuild the demo artefacts with `uv run python scripts/build_demo_curriculum_preview.py`
