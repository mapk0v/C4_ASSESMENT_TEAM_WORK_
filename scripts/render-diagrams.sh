#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

plantuml_jar="${1:-${PLANTUML_JAR:-$project_root/plantuml.jar}}"
if [[ ! -f "$plantuml_jar" ]]; then
  echo "ERROR: PlantUML JAR not found: $plantuml_jar" >&2
  echo "Usage: bash scripts/render-diagrams.sh /absolute/path/to/plantuml.jar" >&2
  exit 2
fi

for dir in LR1 LR2 LR3 LR4 src; do
  if [[ ! -d "$dir" ]]; then
    echo "ERROR: Required directory is missing: $dir" >&2
    exit 2
  fi
done

# Include only project diagrams. Vendored C4 macros are not standalone diagrams.
mapfile -d '' diagrams < <(
  find LR1 LR2 LR3 LR4 src -type f -name '*.puml' ! -path 'LR4/vendor/*' -print0 | sort -z
)
if (( ${#diagrams[@]} == 0 )); then
  echo "ERROR: No PlantUML diagrams found" >&2
  exit 2
fi

mkdir -p "$project_root/docs/images"
# Also works in restricted local environments where the system /tmp is not writable.
java_temp_option="-Djava.io.tmpdir=$project_root/docs/images"

echo "Validating ${#diagrams[@]} PlantUML diagrams..."
failures=0
for diagram in "${diagrams[@]}"; do
  echo "CHECK $diagram"
  if ! java "$java_temp_option" -jar "$plantuml_jar" -DRELATIVE_INCLUDE=1 -checkonly "$diagram"; then
    echo "::error file=$diagram::PlantUML syntax validation failed"
    failures=$((failures + 1))
  fi
done
if (( failures > 0 )); then
  echo "ERROR: $failures diagram(s) failed. No images were generated." >&2
  exit 1
fi

echo "Rendering PNG and SVG..."
for diagram in "${diagrams[@]}"; do
  output_dir="$project_root/docs/images/$(dirname "$diagram")"
  mkdir -p "$output_dir"
  java "$java_temp_option" -jar "$plantuml_jar" -DRELATIVE_INCLUDE=1 -tpng -o "$output_dir" "$diagram"
  java "$java_temp_option" -jar "$plantuml_jar" -DRELATIVE_INCLUDE=1 -tsvg -o "$output_dir" "$diagram"
done

png_count="$(find docs/images -type f -name '*.png' | wc -l)"
svg_count="$(find docs/images -type f -name '*.svg' | wc -l)"
echo "SUCCESS: validated ${#diagrams[@]} diagrams; generated $png_count PNG and $svg_count SVG files."
