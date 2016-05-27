

### Flume

La descarga de tweets se realiza por medio de Apache Flume versión 1.6.0, el cual reside en su propio Docker y se encarga de obtener los tweets y almacenarlos en un bucket de Amazon S3. Esta versión de Flume soporta la API de Streaming de Twitter, el cual provee con un _source_ Twitter con las propiedades necesarias para configurar la API con las credenciales. Amazon S3 utiliza un sistema de archivos de Hadoop y Flume provee una configuración destinada para este tipo de _sink_ o sumidero. Además, se definió un canal de tipo _memory_ que mantiene una cola de mensajes en memoria. Aquí se muestra un extracto del archivo de configuración de Flume que establece estas características.

```
TwitterAgent.sources = Twitter
TwitterAgent.channels = MemChannel
TwitterAgent.sinks = s3hdfs
```

De manera predeterminada este source almacena múltiples tweets en un archivo Avro, pero nuestras necesidades requerían los tweets en formato JSON. Para hacer este cambio se requiere modificar el tipo del source, el cual sigue siendo Twitter pero soportado por otra librería. Esta libreria la obtuvimos de una versión personalizada de Flume de Cloudera que contiene las librerias necesarías para realizar la descarga en JSON, la cual puede ser consultada en [Github](https://github.com/cloudera/cdh-twitter-example). Al final la configuración del _source_ de Flume quedó como sigue:

```
TwitterAgent.sources.Twitter.type = com.cloudera.flume.source.TwitterSource
TwitterAgent.sources.Twitter.consumerKey = <twitter-consumer-key>
TwitterAgent.sources.Twitter.consumerSecret = <twitter-consumer-secret>
TwitterAgent.sources.Twitter.accessToken = <twitter-access-token>
TwitterAgent.sources.Twitter.accessTokenSecret = <twitter-access-token-secret>
TwitterAgent.sources.Twitter.keywords = @realdonaldtrump,#Trump,#trump
```
La última línea de código establece las palabras que utilizará la API de Twitter para identificar qué tweets va a descargar, los cuales corresponden a la cuenta de Twitter de Donald Trump y dos hashtags.

Otra parte importante es definir las características del sumidero de Flume. El siguiente bloque muestra las características de este.

```
TwitterAgent.sinks.s3hdfs.type = hdfs
TwitterAgent.sinks.s3hdfs.hdfs.path = s3n://<aws-access-key-id>:<aws-secret-access-key>@<bucket>/%m-%d-%h
TwitterAgent.sinks.s3hdfs.hdfs.fileType = DataStream
TwitterAgent.sinks.s3hdfs.hdfs.filePrefix = tweets
TwitterAgent.sinks.s3hdfs.hdfs.fileSuffix = .json
TwitterAgent.sinks.s3hdfs.hdfs.writeFormat = Text
TwitterAgent.sinks.s3hdfs.hdfs.rollCount = 0
TwitterAgent.sinks.s3hdfs.hdfs.rollSize = 0
TwitterAgent.sinks.s3hdfs.hdfs.batchSize = 100
TwitterAgent.sinks.s3hdfs.hdfs.useLocalTimeStamp = true
TwitterAgent.sinks.s3hdfs.hdfs.maxOpenFiles = 5
```
Esto define las propiedades del sumidero, como el tipo del sistema de archivos, la ruta al bucket de S3 junto con el patrón para la generación de carpetas, el formato de los archivos, el tamaño de cada archivo, entre otras. Los datos faltantes de la ruta al bucket se extraen el ambiente.

Por último, se establecieron las capacidades del canal de Flume con la siguiente configuración.

```
TwitterAgent.channels.MemChannel.capacity = 10000
TwitterAgent.channels.MemChannel.transactionCapacity = 1000
TwitterAgent.channels.MemChannel.type=memory
```

Esta configuración se almacena en el archivo `twitter.conf` y se establece la siguiente línea en el comando de la imagen de Docker de Flume dentro del Docker Compose.
```
flume-ng agent -n TwitterAgent -c /usr/flume/apache-flume-1.6.0-bin/conf -f /home/flume/twitter.conf -Dflume.root.logger=INFO,console
```

## Requerimientos del ambiente.
En general, se levanta utilizando el Docker Compose, sin embargo vários componentes requieren que exista la imágen dpa/base la cual se construye con el comando:
```bash
docker build --force-rm -t dpa/base docker-images/base
```
Después de eso, el ambiente puede construirse con el comando:
```bash
docker-compose build --force-rm
```

## Ejecución :
Se levanta el Docker Compose con:
```bash
docker-compose up -d
```
Después, nos conectamos a luigi_worker con:
```bash
docker exec -it ambiente_luigi_worker_1 /bin/bash
```
lo cual nos devuelve el prompt en bash de luigi worker.

Podemos conectarnos (para probar línea por línea) al pyspark con:
```bash
pyspark --master spark://master:7077 --packages com.amazonaws:aws-java-sdk-pom:1.10.34,org.apache.hadoop:hadoop-aws:2.6.0
```
