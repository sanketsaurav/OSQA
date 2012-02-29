#!/bin/bash

# Compress all js and style files, replacing existing minified versions
# Must be executed from the media directory

wd=$PWD

echo "Generating CSS sprite image..."
cd tools/smartsprites-0.2.8
./smartsprites.sh --css-files $wd/style/style.css
cd $wd
echo

echo "Compressing JavaScript and CSS resources..."
for i in `find js/ style/ -type f \( -name '*.js' -o -name '*.css' \) ! -name '*.min.*'`
do
  # From http://stackoverflow.com/questions/965053/extract-filename-and-extension-in-bash
  filename="${i##*/}"                      # Strip longest match of */ from start
  dir="${i:0:${#i} - ${#filename}}"        # Substring from 0 thru pos of filename
  base="${i%.[^.]*}"                       # Strip shortest match of . plus at least one non-dot char from end
  ext="${i:${#base} + 1}"                  # Substring from len of base thru end

  filename=${base}.min.${ext}
  echo "Compressing $i to $filename"
  java -jar tools/yuicompressor-2.4.7.jar -o $filename $i
done
