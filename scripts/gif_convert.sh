#!/usr/bin/env bash
set -euo pipefail

mkdir -p output/gif
shopt -s nullglob

mp4_files=(output/mp4/*.mp4)

if [ ${#mp4_files[@]} -eq 0 ]; then
  printf 'No MP4 files found in output/mp4/.\n'
  exit 0
fi

for mp4 in "${mp4_files[@]}"; do
  base=$(basename "$mp4" .mp4)
  printf 'Converting %s to GIF...\n' "$base"
  ffmpeg -y -i "$mp4" \
    -vf "crop=ih:ih:(iw-ih)/2:0,fps=15,scale=540:540:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" \
    -loop 0 \
    "output/gif/${base}.gif"
done

printf 'GIF output written to output/gif/.\n'
