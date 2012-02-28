#!/bin/bash

# Compress all js and style files, replacing existing minified versions

for i in `find js/ style/ -type f -name '*.css' -or -name '*.js' -not -name '*.min.css' -not -name '*.min.js'`
do
  # From http://stackoverflow.com/questions/965053/extract-filename-and-extension-in-bash
  filename="${i##*/}"                      # Strip longest match of */ from start
  dir="${i:0:${#i} - ${#filename}}" # Substring from 0 thru pos of filename
  base="${i%.[^.]*}"                       # Strip shortest match of . plus at least one non-dot char from end
  ext="${i:${#base} + 1}"                  # Substring from len of base thru end

  filename=${base}.min.${ext}
  echo "Compressing $i to $filename"
  java -jar yuicompressor-2.4.7.jar -o $filename $i
done