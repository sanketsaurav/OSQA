#!/bin/sh

#
# Add extra JVM options here
#
OPTS="-Xms64m -Xmx256m"
basedir=`dirname "$0"`
java $OPTS -Djava.ext.dirs=$basedir/lib org.carrot2.labs.smartsprites.SmartSprites "$@"
