#!/bin/bash
# Render one animatic frame-range sequentially into the shared stills dir.
# usage: render_chunk.sh START END
ROOT=/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1
EP=$ROOT/episodes/law11-zai
STILLS=$EP/out/animatic_stills
A=$1; B=$2
mkdir -p "$STILLS"
DIR=$ROOT/episodes/_chunk_$$_$A
rm -rf "$DIR"; mkdir -p "$DIR/out"
cp "$EP/film.json" "$DIR/"
cp -r "$EP/sets" "$DIR/"
cp -r "$EP/cast" "$DIR/"
cp -r "$EP/out/plan" "$DIR/out/"
node "$ROOT/templates/threejs_film/render.mjs" "$DIR/film.json" \
     --frames "$(seq -s, $A $B)" --stills-dir "$STILLS" >> "/tmp/chunk_${A}.log" 2>&1
RC=$?
rm -rf "$DIR"
echo "chunk $A-$B rc=$RC: $(ls "$STILLS" | wc -l) stills total"
