#!/usr/bin/env python
import os, argparse
from subprocess import call

SS_CMD = "tools/smartsprites-0.2.8/smartsprites%s --css-files %s" # script extension, input style file
STYLE_FILE = "style/style.css"
YUI_JAR = "tools/yuicompressor-2.4.7.jar"
YUI_CMD = "java -jar %s -o %s %s" # jarfile, output file, input file
CLOSURE_JAR = "tools/closure-compiler/compiler.jar"
CLOSURE_CMD = "java -jar %s --js %s --js_output_file %s" # jarfile, input file, outputfile

def compress_files(root):
    s = os.path.splitext
    j = os.path.join
    for path, subdirs, files in os.walk(root):
        for name in files:
            file = j(path, name)
            filename, ext = s(file)
            dest = filename + ".min" + ext

            # Check this isn't already a minified version of the file, then compress
            if ".min" != s(filename)[1]:
                if ".css" == ext: compress_css(file, dest)
                elif ".js" == ext: compress_js(file, dest)


def generate_sprites():
    ext = ".cmd"
    if os.name == "posix":
      ext = ".sh"
    call(SS_CMD % (ext, STYLE_FILE), shell=True)
    

def compress_js(file, dest):
    print("Compiling %s..." % file)
    call(CLOSURE_CMD % (CLOSURE_JAR, file, dest), shell=True)


def compress_css(file, dest):
    print("Minifying %s..." % file)
    call(YUI_CMD % (YUI_JAR, dest, file), shell=True)

parser = argparse.ArgumentParser(description='Compress media resources.')
parser.add_argument('--include', required=True, help="the resources to include in the operation. 'css', 'js' or 'all'. css includes sprite generation")
args = parser.parse_args()

if args.include == 'all' or args.include == 'css':
    print("\nGenerating sprites and styles...")
    generate_sprites()

    print("\nMinifying css resources...")
    compress_files("style/")

if args.include == 'all' or args.include == 'js':
    print("\nCompiling JavaScript...")
    compress_files("js/")

