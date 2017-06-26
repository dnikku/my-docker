#!/bin/sh

# @see https://github.com/gustavonalle/yarn-docker/blob/master/Dockerfile

HADOOP_BUILD=$(dirname "$(readlink -f "$0")")

MY_USER=$1
HADOOP_VERSION=${2:'2.7.3'}
HADOOP_HOME=/home/$MY_USER/hadoop-${HADOOP_VERSION}

PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

set -ex

echo "
export HADOOP_HOME=/home/$MY_USER/hadoop
export PATH=\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin:\$PATH" >> /etc/profile.d/hadoop-path.sh

cd /home/$MY_USER


if [ ! -f $HADOOP_BUILD/hadoop-$HADOOP_VERSION.tar.gz ]; then
    wget "http://www-us.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz"
else
    mv $HADOOP_BUILD/hadoop-$HADOOP_VERSION.tar.gz .
fi

tar -xzf hadoop-$HADOOP_VERSION.tar.gz
ln -s hadoop-$HADOOP_VERSION hadoop
rm -rf hadoop/share/doc hadoop-$HADOOP_VERSION.tar.gz

mkdir -p $HADOOP_HOME/etc/hadoop
echo "my-hd-master" > $HADOOP_HOME/etc/hadoop/masters
#echo "my-hd-master\nmy-hd-slave" > $HADOOP_HOME/etc/hadoop/slaves

cp $HADOOP_BUILD/core-site.xml $HADOOP_HOME/etc/hadoop/
cp $HADOOP_BUILD/yarn-site.xml $HADOOP_HOME/etc/hadoop/
cp $HADOOP_BUILD/mapred-site.xml $HADOOP_HOME/etc/hadoop/
cp $HADOOP_BUILD/hadoop-env.sh $HADOOP_HOME/etc/hadoop/ && chmod +x $HADOOP_HOME/etc/hadoop/hadoop-env.sh

chown -R $MY_USER:$MY_USER hadoop-$HADOOP_VERSION
