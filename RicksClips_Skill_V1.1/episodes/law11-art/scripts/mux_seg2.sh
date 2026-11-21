#!/bin/bash
set -e
FR=/home/z/my-project/ricksclips-animation-skill/art_frames
SEG=/home/z/my-project/ricksclips-animation-skill/art_segments
mkdir -p "$SEG"
LO=$1; HI=$2
N=$((HI-LO))
ffmpeg -y -v warning -framerate 30 -start_number $LO -i "$FR/f_%05d.png" -frames:v $N \
  -c:v libx264 -preset veryfast -pix_fmt yuv420p -crf 20 -r 30 \
  "$SEG/seg_$(printf '%05d' $LO).mp4" &
FPID=$!
for i in $(seq 1 190); do sleep 1; ps -p $FPID >/dev/null 2>&1 || break; done
sleep 2; kill -9 $FPID 2>/dev/null || true
wait $FPID 2>/dev/null || true
ls -la "$SEG/seg_$(printf '%05d' $LO).mp4" | awk '{print "segment", $LO, $5, "bytes"}'
