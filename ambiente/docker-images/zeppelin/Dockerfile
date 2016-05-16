FROM dpa/base

MAINTAINER Adolfo De Unánue <adolfo.deunanue@itam.mx>


# Instalamos más dependencias
RUN  apt-get update \
     && apt-get install -y npm python-setuptools python-pip python-dev python-numpy --no-install-recommends \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

RUN pip install py4j

ENV ZEPPELIN_HOME /usr/local/zeppelin
ENV APACHE_SPARK_VERSION=1.6

# Descargamos Apache Zeppelin
RUN mkdir -p ${ZEPPELIN_HOME} \
	&& mkdir -p ${ZEPPELIN_HOME}/logs \
        && mkdir -p ${ZEPPELIN_HOME}/run \
        && mkdir -p ${ZEPPELIN_HOME}/data \
        && cd /usr/local \
        && git clone https://github.com/apache/incubator-zeppelin.git \
        && mv /usr/local/incubator-zeppelin/* ${ZEPPELIN_HOME} \
        && rm -fr /usr/local/incubator-zeppelin

# install and configure Zeppelin
RUN  git config --global url.https://github.com/.insteadOf git://github.com/ \
     && cd ${ZEPPELIN_HOME} \
     && mvn clean package -DskipTests

WORKDIR ${ZEPPELIN_HOME}

VOLUME [${ZEPPELIN_HOME}/notebook, ${ZEPPELIN_HOME}/logs]

EXPOSE 8080 8081 4040

CMD ["/usr/local/zeppelin/bin/zeppelin.sh"]
