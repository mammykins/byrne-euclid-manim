from __future__ import annotations

import argparse
import logging

from byrne_euclid.rendering import SCENE_REGISTRY, render_scene


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a single Byrne-Euclid scene")
    parser.add_argument("scene", help="Scene class name")
    parser.add_argument("--quality", "-q", default="m", choices=["l", "m", "h", "p", "k"])
    parser.add_argument("--format", "-f", default="mp4", choices=["mp4", "gif", "png"])
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args()
    if args.scene not in SCENE_REGISTRY:
        available = ", ".join(sorted(SCENE_REGISTRY))
        raise SystemExit(f"Unknown scene '{args.scene}'. Available scenes: {available}")

    destination = render_scene(args.scene, quality=args.quality, output_format=args.format)
    logging.info("Rendered %s to %s", args.scene, destination)


if __name__ == "__main__":
    main()
