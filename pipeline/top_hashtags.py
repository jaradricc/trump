import re
import sys

import locale

import datetime

import json

from random import random

# from operator import add
from operator import itemgetter

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


## Tenemos que leer archivos .json y, una vez abierto, extraer del grupo de tweets (.json) los campos que nos interesan
    sqlCtx.read.json(sys.argv[1])\
                    .registerTempTable('tweets')

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
    sc.stop()
