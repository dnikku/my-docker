#!/bin/sh

JAVA_HOME=/usr/lib/jvm/default-jvm
PATH=$JAVA_HOME/bin:$PATH

echo "
export JAVA_HOME=/usr/lib/jvm/default-jvm
export PATH=$JAVA_HOME/bin:\$PATH" >> /etc/profile.d/java-path.sh

apk add --update openjdk8
