#!/bin/bash
# Segment-encode law11 frames: each call encodes one 440-frame segment (~15s of work).
# usage: mux_seg.sh <start> <end_exclusive>
set -e
FR=/home/z/my-project/ricksclips-animation-skill/law11_frames
SEG=/home/z/my-project/ricksclips-animation-skill/law11_segments
mkdir -p "$SEG"
LO=$1; HI=$2
N=$((HI-LO))
ffmpeg -y -v warning -framerate 30 -start_number $LO -i "$FR/f_%05d.png" -frames:v $N \
  -c:v libx264 -preset veryfast -pix_fmt yuv420p -crf 20 -r 30 \
  "$SEG/seg_$(printf '%03d' $LO).mp4"
echo "segment $LO-$HI done: $(ls -la "$SEG/seg_$(printf '%03d' $LO).mp4" | awk '{print $5}') bytes"
