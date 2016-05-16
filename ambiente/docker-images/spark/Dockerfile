FROM dpa/base

MAINTAINER Adolfo De Unánue <adolfo.deunanue@itam.mx>

## Variables de ambiente
ENV SPARK_VERSION 1.6.0
ENV HADOOP_VERSION 2.6
ENV SPARK_PACKAGE spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION
ENV SPARK_HOME /usr/$SPARK_PACKAGE
ENV PATH $PATH:$SPARK_HOME/bin

## Descarga de Spark
RUN curl -sL --retry 3 \
  "http://d3kbcqa49mib13.cloudfront.net/$SPARK_PACKAGE.tgz" \
  | gunzip \
  | tar x -C /usr/ \
  && ln -s $SPARK_HOME /usr/spark

## Copiamos los archivos de configuración
## para master y worker
ADD ./conf/master/spark-defaults.conf /conf/master/spark-defaults.conf
ADD ./conf/worker/spark-defaults.conf /conf/worker/spark-defaults.conf


## Librerías de Spark-Hadoop
RUN curl -sL --retry 3 "http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.6.0/hadoop-aws-2.6.0.jar" -o $SPARK_HOME/lib/hadoop-aws-2.6.0.jar \
 && curl -sL --retry 3 "http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.7.14/aws-java-sdk-1.7.14.jar" -o $SPARK_HOME/lib/aws-java-sdk-1.7.14.jar \
 && curl -sL --retry 3 "http://central.maven.org/maven2/com/google/collections/google-collections/1.0/google-collections-1.0.jar" -o $SPARK_HOME/lib/google-collections-1.0.jar \
 && curl -sL --retry 3 "http://central.maven.org/maven2/joda-time/joda-time/2.8.2/joda-time-2.8.2.jar" -o $SPARK_HOME/lib/joda-time-2.8.2.jar

CMD /usr/spark/bin/spark-class org.apache.spark.deploy.master.Master
