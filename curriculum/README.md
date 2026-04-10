# Curriculum data

This directory holds the hand-maintained curriculum mapping and any cached Oak National Academy API responses used to enrich it.

## Files

- `euclid_to_oak.yaml` — the source-of-truth mapping from scene class to Euclid reference, national curriculum references, and draft Oak linkage
- `curriculum_manifest.json` — generated JSON manifest for programmatic consumers
- `oak_*.json` — cached Oak API responses written by `scripts/fetch_oak_curriculum.py`

## Attribution

Contains public sector information licensed under the Open Government Licence v3.0.

Oak National Academy content is used under the Open Government Licence. When lesson content or curriculum metadata from Oak informs downstream artefacts, include an attribution statement linking to the OGL:

- https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/

## Update workflow

1. Refresh Oak cache data with `uv run --env-file .env python scripts/fetch_oak_curriculum.py`
2. Review or adjust `curriculum/euclid_to_oak.yaml`
3. Rebuild the manifest and curriculum document with `uv run python scripts/build_manifest.py`
