# Análisis del sentimiento de tweets

## Descripción y objetivos del proyecto
Este proyecto tiene como objetivo realizar un análisis de tweets relativos a la campaña presidencial de Donald Trump desde diferentes aristas, es decir, se pretende obtener estadísticas descriptivas de los tuits que contengan @realdonaldtrump, #Trump, #trump, #Trump2016 en su cuerpo, así como realizar un modelo estadístico que nos ayude a identificar los tópicos que rodean su carrera presidencial.

A lo largo de este documento se aboradarán cada uno de estos temas, comenzando en principio por el diseño de la arquitecutra, la descripción de las componentes que conforman el cluster junto con sus respectivas tareas, así como el detalle del modelo de minería de texto que se utilizó para identificar los diversos tópicos.

## Descripción de la arquitectura

El proyecto consiste de múltiples tecnologías y componentes organizados según los lineamientos de la [Arquitectura Lambda](http://lambda-architecture.net/), la cual define una arquitectura genérica, escalable y tolerante a faltas para el procesamiento de datos en _batch_.


![Diseño Arquitectura](Readme_images/arqui.png)

Tal y como se puede observar en la gráfica anterior la arquitectura puede ser dividida en tres grandes fases:

* La lectura de la información (Flume, S3)
* Procesamiento de la información ( Luigi, Spark)
* Modelo Estadístico y Dashboard (Python, Shiny)

A continuación veremos una breve descripción de los componentes que definenen el ambiente.

## Ambiente

* Flume

[Flume](https://github.com/omisimo/trump/tree/master/ambiente/docker-images/flume)


* Luigi

[Luigi](https://github.com/omisimo/trump/tree/master/ambiente/docker-images/luigid)



* Spark

[Spark](https://github.com/omisimo/trump/tree/master/ambiente/docker-images/spark)


* Datalake

[Datalake](https://github.com/omisimo/trump/tree/master/ambiente/docker-images/datalake)


* Python


* Shiny
