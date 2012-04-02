The skin media directory contains static media files including images, stylesheets and JavaScript.

Resource Optimisation
-------------
JavaScript compilation, CSS minification, file merging and sprite generation is automated. Execute compress.py after any change to css, js or image files included in the sprite.

The '.src' directories are where original js and css files are stored. The compression process flattens any directory structure and outputs the 'live' files to the non-suffixed directories, after emptying the directories.

Requirements
-------------
Juicer must be installed:

http://cjohansen.no/en/ruby/juicer_a_css_and_javascript_packaging_tool
https://github.com/cjohansen/juicer

With the following dependencies:

* YUI Compressor
* Closure Compiler
* JSLint 

Handy guice for dependencies on Ubuntu:

http://blog.moonflare.com/2011/10/25/installing-ruby-1-9-2-and-gems-on-ubuntu-11-10/

Additional tools used by the script are in the tools directory:

* Smart Sprites tool - http://csssprites.org/
