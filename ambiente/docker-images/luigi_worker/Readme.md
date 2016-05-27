# Luigi Worker

Este Dockerfile instala la imagen de Luigi Worker


´´´ python
FROM python:3.4-slim

ENV LUIGI_HOME /etc/luigi

RUN apt-get update

RUN apt-get install -y build-essential git curl libpq-dev

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir  $LUIGI_HOME

## Variables de ambiente
ENV JAVA_HOME /usr/jdk1.8.0_31
ENV PATH $PATH:$JAVA_HOME/bin
ENV SPARK_VERSION 1.6.0
ENV HADOOP_VERSION 2.6
ENV PY4J_VERSION 0.9
ENV SPARK_PACKAGE spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION
ENV SPARK_HOME /usr/$SPARK_PACKAGE
ENV PATH $PATH:$SPARK_HOME/bin
ENV SPARK_CONF_DIR=/opt/conf/spark
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$SPARK_HOME/python/lib/py4j-$PY4J_VERSION-src.zip:$SPARK_HOME/libexec/python:$SPARK_HOME/libexec/python/build:$PYTHONPATH

## Descargamos Java8
RUN curl -sL --retry 3 --insecure \
  --header "Cookie: oraclelicense=accept-securebackup-cookie;" \
  "http://download.oracle.com/otn-pub/java/jdk/8u31-b13/server-jre-8u31-linux-x64.tar.gz" \
  | gunzip \
  | tar x -C /usr/ \
  && ln -s $JAVA_HOME /usr/java \
  && rm -rf $JAVA_HOME/man

## Descargamos Apache Spark
RUN curl -sL --retry 3 \
  "http://d3kbcqa49mib13.cloudfront.net/$SPARK_PACKAGE.tgz" \
  | gunzip \
  | tar x -C /usr/ \
  && ln -s $SPARK_HOME /usr/spark

## Variables para el usuario
ENV DPA_USER dpa_worker
ENV DPA_UID 1000

## Creamos al usuario que ejecuta el worker en el grupo `users`
RUN useradd -m -s /bin/bash -N -u $DPA_UID $DPA_USER

ADD .boto /home/$DPA_USER/.boto
ADD .boto /etc/boto.cfg

RUN chown $DPA_USER:users /home/$DPA_USER/.boto

WORKDIR /home/$DPA_USER

## Clonamos el repositorio
RUN git clone https://github.com/jaradricc/Trump.git

WORKDIR /home/$DPA_USER/Trump/pipeline

CMD [ "/bin/sh",  "-c", "while true; do echo hello world; sleep 1; done"]

´´´

Podemos observar que este código realiza las siguientes tareas

* Instala paqueterías de algebra lineal, entre otras
* Instala los paquetes de python que necestiamos
* Define varialbes de ambiente
* Instala JAVA
* Instala Spark
* Crea varaibles para el usuario
* Crea al usuario qeu ejecuta el worker en el grupo users
* Generamos archivo .boto
* Clonamos el repositorio



El archivo .boto debe contener la siguiente información:

´´´python
[Credentials]
aws_access_key_id = ACCESS_KIV52_KEY_ID
aws_secret_access_key = SECRET_ENYq86s_ACCESS_KEY

[Boto]
debug = 2
num_retries = 10
´´´
El archivo debe ser creado en la misma carepta en donde se encuentra el Dockerfile de luigiworker.

Finalmente, agregamos la llave para que pueda descargar nuestro repo de github y creamos el comando que queremos que este luigi worker empiece a ejecutar.

Por ahora este luigi worker estará imprimiendo en pantalla el mensaje "Hola mundo" cada segundo.

Se planea qeu cada uno de los luigi workers estarán ligados al luigi master con el comando links en el docker-compose.
