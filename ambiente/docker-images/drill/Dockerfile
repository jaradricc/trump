FROM dpa/base

MAINTAINER Adolfo De Unánue <adolfo.deunanue@itam.mx>


## Variables de ambiente
ENV DRILL_VERSION 1.6.0
ENV DRILL_HOME /opt/drill
ENV PATH $PATH:$DRILL_HOME/bin

## Descarga de Apache Drill
RUN curl -sL --retry 3 \
    "http://apache.mesi.com.ar/drill/drill-${DRILL_VERSION}/apache-drill-${DRILL_VERSION}.tar.gz" \
    | gunzip \
    | tar x -C /opt/ \
    && ln -s /opt/apache-drill-1.6.0 $DRILL_HOME

## Obtenemos el JAR para AWS S3

RUN wget http://bitbucket.org/jmurty/jets3t/downloads/jets3t-0.9.3.zip && \
    unzip jets3t-0.9.3.zip && \
    rm jets3t-0.9.3.zip

RUN cp jets3t-0.9.3/jars/jets3t-0.9.3.jar $DRILL_HOME/jars/3rdparty

RUN sed -i '/jets3t/d' $DRILL_HOME/bin/hadoop-excludes.txt

## Copiamos archivos de configuración
COPY conf/ $DRILL_HOME/conf/

## Copiamos archivos de ejecución
COPY start.sh start.sh
RUN chmod +x start.sh

## Logs
RUN mkdir -p ${DRILL_HOME}/log/
RUN touch ${DRILL_HOME}/log/drillbit.out

## Cliente web
EXPOSE 8047

CMD ["drill-embedded"]
