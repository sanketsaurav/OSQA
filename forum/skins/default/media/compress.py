#!/usr/bin/env python
import os, argparse
from subprocess import call

STYLE_SRC_DIR = "style.src/"
STYLE_DEST_DIR = "style/"
JS_SRC_DIR = "js.src/"
JS_DEST_DIR = "js/"

SS_CMD = "tools/smartsprites-0.2.8/smartsprites%s --css-files %s" # script extension, input style file
SPRITE_SRC_FILE = "style.src/style.css"

JUICER = "juicer"
JUICER_CSS_CMD = "%s merge -f -c none -o %s %s" # script, output file, input file 
JUICER_JS_CMD = '%s merge -m closure_compiler -s -f -a "--create_source_map %s --source_map_format=V3" -o %s %s' # script, source map output file, output file, input file 

def which(program):
    """
    Determine whether a given program is available on the system path.

    From http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def empty_directory(directory):
    print "Emptying directory %s..." % directory
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def check_dependencies():
    if which(JUICER) is None:
      print("Juicer not found on path. Refer to README.md for dependency details.") 


def compress_files(root):
    s = os.path.split
    se = os.path.splitext
    j = os.path.join
    for path, subdirs, files in os.walk(root):
        for name in files:
            full_path = j(path, name)
            parent, file = s(full_path)
            filename, ext = se(file)

            # Check this isn't already a minified version of the file, then compress
            if ".min" != s(filename)[1]:
                if ".css" == ext: compress_css(full_path, STYLE_DEST_DIR + file)
                elif ".js" == ext: compress_js(full_path, JS_DEST_DIR + file)


def generate_sprites():
    ext = ".cmd"
    if os.name == "posix":
      ext = ".sh"
    call(SS_CMD % (ext, SPRITE_SRC_FILE), shell=True)
    

def compress_js(file, dest):
    print("Compiling %s..." % file)
    map_file = dest + ".map"
    call(JUICER_JS_CMD % (JUICER, map_file, dest, file), shell=True)

    # Write the source map header
    with open(dest, "a") as jsfile:
        jsfile.write("//@ sourceMappingURL=%s" % map_file)


def compress_css(file, dest):
    print("Minifying %s..." % file)
    call(JUICER_CSS_CMD % (JUICER, dest, file), shell=True)

parser = argparse.ArgumentParser(description="Compress media resources.")
parser.add_argument("--include", required=True, help="the resources to include in the operation. 'css', 'js' or 'all'. css includes sprite generation")
args = parser.parse_args()

check_dependencies()

if args.include == "all" or args.include == "css":
    print("\nGenerating sprites and styles...")
    generate_sprites()

    print("\nMinifying css resources...")
    empty_directory(STYLE_DEST_DIR)
    compress_files(STYLE_SRC_DIR)

if args.include == "all" or args.include == "js":
    print("\nCompiling JavaScript...")
    empty_directory(JS_DEST_DIR)
    compress_files(JS_SRC_DIR)

