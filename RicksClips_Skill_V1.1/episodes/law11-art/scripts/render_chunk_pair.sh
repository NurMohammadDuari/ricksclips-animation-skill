#!/bin/bash
# Render two animatic frame-ranges in parallel, each in its own scratch episode dir
# (render.mjs races on the shared out/.puppet_cache when two processes share one episode).
# usage: render_chunk_pair.sh START1 END1 START2 END2
ROOT=/home/z/my-project/ricksclips-animation-skill/RicksClips_Skill_V1.1
EP=$ROOT/episodes/law11-zai
STILLS=$EP/out/animatic_stills
mkdir -p "$STILLS"

run() { # start end
  local a=$1 b=$2
  local dir=$ROOT/episodes/_chunk_$$_$a
  rm -rf "$dir"; mkdir -p "$dir/out"
  cp "$EP/film.json" "$dir/"
  cp -r "$EP/sets" "$dir/"
  cp -r "$EP/cast" "$dir/"
  cp -r "$EP/out/plan" "$dir/out/"
  node "$ROOT/templates/threejs_film/render.mjs" "$dir/film.json" \
       --frames "$(seq -s, $a $b)" --stills-dir "$STILLS" >> "/tmp/chunk_${a}.log" 2>&1
  local rc=$?
  rm -rf "$dir"
  return $rc
}

run "$1" "$2" & p1=$!
run "$3" "$4" & p2=$!
wait $p1; r1=$?
wait $p2; r2=$?
echo "pair $1-$2(rc=$r1) / $3-$4(rc=$r2): $(ls "$STILLS" | wc -l) stills total"
