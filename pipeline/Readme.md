# Pipeline

En esta sección trataremos a detalle el archivo *etl.py* que utiliza Luigi y los respectivos *Luigi_workers*

Una vez que Flume ha guardado los archivos JSON en el bucket de S3, el siguiente paso consiste en el procesamiento de la información, es decir, nos interesa extraer los atributos de valor para nuestro análisis. En parituclar, este análisis lo podemos dividir en dos grandes tareas:

* El procesamiento de la información para el modelo
* Estadísticas descriptivas de la información


## procesamiento de la información

Dado que el alcance de este proyecto pretende realizar un modelo de procesamiento de lenguaje natural, necestamos los 140 caracteres que conforman cada tweet. Para ello utilizarmos herramientas como Spark para realizar el query que nos permita extraer dicho atributo.



En primer lugar es necesario acceder al bucket para la lectura de la información; no debemos olvidar que en el archivo .boto y el archivo .env, ubicados en la imagen de lugi worker y en el docker-compose respectivamente, se deben encontrar nuestras llaves de amazaón que nos permitan entrar al bucket.

```python
class ReadContainer(luigi.ExternalTask):
    def output(self):
        return luigi.s3.S3Target(configuration.get_config().get('etl','bucket')+'/05-19-20/')
```

Una vez leidos los datos, podemos hacer el query que extraiga el texto del tweet.

```python
sqlCtx.read.json(sys.argv[1])\
                   .registerTempTable('tweets')

   sqlCtx.sql("select id_str,favorite_count,retweet_count,text from tweets")\
       .coalesce(1)\
       .write.parquet(sys.argv[2], mode='overwrite')
   print ("Terminada la tarea de spark")
```

## Estadísticas descriptivas de la información

Las siguientes tareas de las que se debe encargar Luigi, consisten en obtener resumenes que nos permitan darnos una idea de la evolución de los tweets en el tiempo, así como el comportamiento de los usarios y los trendingn topics. Por esta razón se divide en tres tareas adicionales para luigi:

* El sumarizado de tweets y Retweets por día

```python


    test = sqlCtx.sql('select retweeted as is_rt, created_at as date from tweets').collect()



    res = dict()
    for i in test:
        aux = i.date.split()
        fecha = aux[1] + '/' + aux[2] + '/' + aux[5]
        if fecha not in res:
            if i.is_rt:
                res[fecha] = {'tweets':0,'retweets':1}
            else:
                res[fecha] = {'tweets':1,'retweets':0}
        else:
            if i.is_rt:
                res[fecha]['retweets'] += 1
            else:
                res[fecha]['tweets'] += 1


    with open(sys.argv[2],'w') as f:
        json.dump(res,f)
```
Podemo boservar que fue necesario hacer una recolección de la información de manera local pues se tenía la necesidad de procesar el formato correcto de la fecha. Inicialmente se había realizado un enfoque de funciones definidias por el usuario, sin embargo, en PySpark no fue posible de correr este tipo de funciones comparado con el contenedor de PySpark utilizado en la clase.

El outut de esta función servirá de input para la gráfica de la serie de tiempo de los Tweets y ReTweets.


* El conteo de hastags, para darnos una idea de los trending topics

Igual que en el caso anterior, no fue posible utilizar funciones utilizadas por el usuario, por lo que se tuvo que traer de manera local  para procesar la información que necesitamos. En particular se trata de un conteo de los hastagas observados en el corpus. Este servirá de output para la gráfica de Word Cloud del Shiny

```python
res = sqlCtx.sql("select entities.hashtags.text as hashtags from tweets")\
        .collect()
    hashtags = dict()
    for i in res:
        for h in i.hashtags:
            if h in hashtags:
                hashtags[h] += 1
            else:
                hashtags[h] = 1
    with open(sys.argv[2],'w') as f:
        json.dump(hashtags,f)
    print ("Terminada la tarea de spark")
```
* El conteo de publicaciones por usuario

Esta función nos ayuda a identificar qué usurios son los que más publican temas relacionados con Trump. Además es posible identificar algunso bots u organizaciones electorales que dan seguimiento a este tipo de eventos en las redes sociales.

```python
sqlCtx.read.json(sys.argv[1])\
                   .registerTempTable('tweets')

   sqlCtx.sql("select user.screen_name as user_name ,count(user.screen_name) as total from tweets group by user.screen_name order by total desc")\
       .toPandas()\
       .to_json(sys.argv[2])
   print ("Terminada la tarea de spark")
```

El output de esta función servira para el histograma de usuarios que se muestra en el Shiny

## Distribución de la información

Los archivos fueron copiados en carpetas en donde Python y el Shiny puedan observar para realizar sus respectivas tareas.


## AllTasks

Definimos cada una de estas tareas con sus respectivas dependencias en el archivo etl.

En conclusión, se dicidió hacer que las tres tareas relativas a los estadísticos descriptivos se trabajaran de manera paralela y no dependieran una de la otra, pues en ninguno de los casos se requería del output de una para iniciar la siguiente tarea, a pesar de que se pudo haber programado de tal manera que se pudiera partir del query más general e irlo reduciendo en dimensión hasta el último task.
