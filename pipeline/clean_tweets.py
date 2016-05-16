import re
import sys

import locale

import datetime

from random import random

from operator import add

from pyspark import SparkContext
from pyspark.sql import HiveContext
from pyspark.sql import Row
from pyspark.conf import SparkConf

from pyspark.sql.functions import lag
from pyspark.sql import Window
from pyspark.sql import functions as F

if __name__ == "__main__":
    print ("Iniciada la tarea de spark")
    sc = SparkContext()
    sqlCtx = HiveContext(sc)


## Tenemos que leer archivos .avro y, una vez abierto, extraer del grupo de tweets (.json) los campos que nos interesan
    sqlCtx.read.format('com.databricks.spark.avro')\
                       .load(sys.argv[1])\
                       .registerTempTable('tweets')

    sqlCtx.sql("select State as estado, count(*) as avistamientos from avistamientos group by State")\
        .coalesce(1)\
        .write.parquet(sys.argv[2], mode='overwrite')
    print ("Terminada la tarea de spark")
    sc.stop()
