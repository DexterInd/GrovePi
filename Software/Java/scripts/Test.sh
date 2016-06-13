#/usr/bin/env bash
# $ JAVA_OPTS='-Dconfig=default' Java/bin/runTest.sh
cd ./bin; sudo java $JAVA_OPTS -classpath .:classes:/opt/pi4j/lib/'*' Test