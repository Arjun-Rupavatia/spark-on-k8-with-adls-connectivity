#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


  
# FROM ubuntu:18.04
# WORKDIR /

# USER 0

# RUN apt-get update && \
#     apt-get install -y wget
FROM openjdk:8-jre-slim
ARG spark_uid=185
WORKDIR /opt
USER 0

COPY job.py /opt
COPY main.py /opt
COPY core-site.xml /opt
COPY hadoop-env.sh /opt

RUN set -ex && \
    sed -i 's/http:\/\/deb.\(.*\)/https:\/\/deb.\1/g' /etc/apt/sources.list && \
    apt-get update && \
    ln -s /lib /lib64 && \
    apt install -y bash tini libc6 libpam-modules krb5-user libnss3 && \
    rm /bin/sh && \
    ln -sv /bin/bash /bin/sh && \
    echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su && \
    chgrp root /etc/passwd && chmod ug+rw /etc/passwd && \
    rm -rf /var/cache/apt/* && \
    apt-get install wget -y && \
    apt-get install vim -y && \
    apt-get install -y python && \
    apt-get install -y python3 python3-pip && \
    wget https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-without-hadoop.tgz && \
    wget https://dlcdn.apache.org/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz && \
    tar xvf hadoop-3.2.2.tar.gz && \
    tar xvf spark-3.1.2-bin-without-hadoop.tgz && \
    mv spark-3.1.2-bin-without-hadoop spark && \
    rm hadoop-3.2.2/etc/hadoop/hadoop-env.sh && \
    rm hadoop-3.2.2/etc/hadoop/core-site.xml && \
    cp hadoop-env.sh hadoop-3.2.2/etc/hadoop/ && \
    cp core-site.xml hadoop-3.2.2/etc/hadoop/ && \
    cp /opt/spark/kubernetes/dockerfiles/spark/entrypoint.sh /opt/

WORKDIR /opt/spark
RUN mkdir work-dir && \
    cp -a /opt/spark/kubernetes/tests/ /opt/spark/tests/
    
ENV SPARK_HOME /opt/spark
ENV HADOOP_HOME /opt/hadoop-3.2.2
ENV PATH $PATH:/opt/hadoop-3.2.2/bin:/opt/hadoop-3.2.2/sbin:/opt/spark/bin:/opt/spark/sbin
ENV SPARK_DIST_CLASSPATH /opt/hadoop-3.2.2/etc/hadoop:/opt/hadoop-3.2.2/share/hadoop/common/lib/*:/opt/hadoop-3.2.2/share/hadoop/common/*:/opt/hadoop-3.2.2/share/hadoop/hdfs:/opt/hadoop-3.2.2/share/hadoop/hdfs/lib/*:/opt/hadoop-3.2.2/share/hadoop/hdfs/*:/opt/hadoop-3.2.2/share/hadoop/mapreduce/lib/*:/opt/hadoop-3.2.2/share/hadoop/mapreduce/*:/opt/hadoop-3.2.2/share/hadoop/yarn:/opt/hadoop-3.2.2/share/hadoop/yarn/lib/*:/opt/hadoop-3.2.2/share/hadoop/yarn/*:/opt/hadoop-3.2.2/share/hadoop/tools/lib/*

WORKDIR /opt/spark/work-dir
RUN chmod g+w /opt/spark/work-dir
ENTRYPOINT [ "/opt/entrypoint.sh" ]
USER ${spark_uid}



# Before building the docker image, first build and make a Spark distribution following
# the instructions in http://spark.apache.org/docs/latest/building-spark.html.
# If this docker file is being used in the context of building your images from a Spark
# distribution, the docker build command should be invoked from the top level directory
# of the Spark distribution. E.g.:
# docker build -t spark:latest -f kubernetes/dockerfiles/spark/Dockerfile .

# WORKDIR /


