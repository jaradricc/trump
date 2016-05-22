FROM dpa/base

MAINTAINER Luis C. Cruz <luiscruz.2908@gmail.com> 

ENV REFRESHED_AT 2015-05-01
ENV DEBIAN-FRONTEND noninteractive

USER root

RUN apt-get install apt-transport-https

## Descargando el paquete de configuración de Cloudera
RUN wget -P /tmp -c http://archive.cloudera.com/cdh5/one-click-install/trusty/amd64/cdh5-repository_1.0_all.deb

## Instalando Hadoop de modo Pseudo Distribuido
RUN dpkg -i /tmp/cdh5-repository_1.0_all.deb \
&& apt-get update \
&& apt-get -y install hadoop-conf-pseudo

## Instala Flume
RUN apt-get -y install flume-ng 

RUN mkdir /usr/flume

ENV JAVA_OPTS="-Xms1000m -Xmx5000m -Dcom.sun.management.jmxremote"

RUN mkdir /home/flume/
RUN mkdir /home/flume/source/
RUN mkdir /home/flume/sink/

COPY twitter.conf /home/flume/
ADD flume-sources-1.0-SNAPSHOT.jar /
ADD .env .env
RUN export TEMP1=$(grep AWS_ACCESS_KEY_ID .env | cut -d'=' -f 2) && export TEMP2=$(grep AWS_SECRET_ACCESS_KEY .env | cut -d'=' -f 2) && sed -i "s/\(TwitterAgent.sinks.s3hdfs.hdfs.path *= *\).*/\1s3n:\/\/$TEMP1:$TEMP2@lcruz-tweets\/%m-%d-%H\//" /home/flume/twitter.conf

## Download custom cloudera flume source
RUN cp flume-sources-1.0-SNAPSHOT.jar /usr/lib/flume-ng/lib/flume-sources-1.0-SNAPSHOT.jar
RUN mkdir /var/lib/flume-ng/plugins.d/
RUN mkdir /var/lib/flume-ng/plugins.d/twitter-streaming/
RUN mkdir /var/lib/flume-ng/plugins.d/twitter-streaming/lib/
RUN cp flume-sources-1.0-SNAPSHOT.jar /var/lib/flume-ng/plugins.d/twitter-streaming/lib/flume-sources-1.0-SNAPSHOT.jar






