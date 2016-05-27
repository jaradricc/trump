
# Luigi

En esta sección trataremos a detalle el archivo *etl.py* que utiliza Luigi y los respectivos *Luigi_workers*

Una vez que Flume ha guardado los archivos JSON en el bucket de S3, el siguiente paso consiste en el procesamiento de la información, es decir, nos interesa extraer los atributos de valor para nuestro análisis. En parituclar, este análisis lo podemos dividir en dos grandes tareas:

* El procesamiento de la información para el modelo
* Estadísticas descriptivas de la información


## procesamiento de la información

Dado que el alcance de este proyecto pretende realizar un modelo de procesamiento de lenguaje natural, necestamos los 140 caracteres que conforman cada tweet. Para ello utilizarmos herramientas como Spark para realizar el query que nos permita extraer dicho atributo.

En primer lugar es necesario acceder al bucket para la lectura de la información; no debemos olvidar que en el archivo .boto y el archivo .env, ubicados en la imagen de lugi worker y en el docker-compose respectivamente, se deben encontrar nuestras llaves de amazaón que nos permitan entrar al bucket.

Una vez leidos los datos, podemos hacer el query que extraiga el texto del tweet.

## Estadísticas descriptivas de la información

Las siguientes tareas de las que se debe encargar Luigi, consisten en obtener resumenes que nos permitan darnos una idea de la evolución de los tweets en el tiempo, así como el comportamiento de los usarios y los trendingn topics. Por esta razón se divide en tres tareas adicionales para luigi:

* El sumarizado de tweets y Retweets por día
* El conteo de hastags, para darnos una idea de los trending topics
* El conteo de publicaciones por usuario

## Distribución de la información

Los archivos fueron copiados en carpetas en donde Python y el Shiny puedan observar para realizar sus respectivas tareas.
