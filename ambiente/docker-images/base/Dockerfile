FROM phusion/baseimage

MAINTAINER Adolfo De Unánue <adolfo.deunanue@itam.mx>

ENV REFRESHED_AT 2016-02-27


## Actualizamos
RUN \
    apt-get -qq update; apt-get upgrade -y -qq; \
    apt-get install -y -qq wget curl git jq; \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

## Arreglamos el LOCALE
RUN echo "es_MX.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen es_MX.utf8 \
    && /usr/sbin/update-locale LANG=es_MX.UTF-8 \
    && dpkg-reconfigure locales

# JAVA
ENV JAVA_HOME /usr/jdk1.8.0_31
ENV PATH $PATH:$JAVA_HOME/bin
RUN curl -sL --retry 3 --insecure \
  --header "Cookie: oraclelicense=accept-securebackup-cookie;" \
  "http://download.oracle.com/otn-pub/java/jdk/8u31-b13/server-jre-8u31-linux-x64.tar.gz" \
  | gunzip \
  | tar x -C /usr/ \
  && ln -s $JAVA_HOME /usr/java \
  && rm -rf $JAVA_HOME/man

ENV MAVEN_VERSION=3.3.3

ENV MAVEN_HOME=/usr/local/maven

ENV PATH $PATH:/usr/bin/mvn

## Instalamos Maven
RUN mkdir -p ${MAVEN_HOME} \
    && curl -sSL -o /Maven-${MAVEN_VERSION}.tar.gz http://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz \
    && tar zxf /Maven-${MAVEN_VERSION}.tar.gz -C /usr/local \
    && rm -f /Maven-${MAVEN_VERSION}.tar.gz \
    && mv /usr/local/apache-maven-${MAVEN_VERSION}/* ${MAVEN_HOME} \
    && ln -s /usr/local/maven/bin/mvn /usr/bin/mvn \
## Limpiamos
    && rm -fr /usr/local/apache-maven-${MAVEN_VERSION}



CMD ["/bin/bash"]
