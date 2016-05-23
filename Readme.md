# Ambiente
El ambiente consta de los componentes:
* Luigi (con su luigi worker).
* Spark (con su worker).
* ~~Python para el análisis de texto~~
* ~~datalake para exponer los datos procesados a los componentes de: análisis de texto y shinny~~
* ~~Shinny para visualización de algunas estadísticas de los datos procesados.~~

## Particularidades del ambiente.
En general, se levanta utilizando el docker-compose, sin embargo Spark requiere que exista la imágen dpa/base la cual se construye con el comando:
```bash
docker build --force-rm -t dpa/base docker-images/base
```
Después de eso, el ambiente puede construirse con el comando:
```bash
docker-compose build --force-rm
```

### Probando :
levantamos el docker compose con:
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
