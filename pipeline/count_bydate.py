import re
import sys

import locale

import datetime

from random import random

from operator import add

import pyspark
from pyspark import SparkContext
from pyspark.sql import HiveContext
from pyspark.sql import Row
from pyspark.conf import SparkConf

from pyspark.sql.functions import lag
from pyspark.sql import Window
from pyspark.sql import functions as F

import numpy as np
from pyspark.sql.types import *
import calendar

import json

if __name__ == "__main__":
    print ("Iniciada la tarea de spark")
    sc = SparkContext()
    sqlCtx = HiveContext(sc)

    sqlCtx.read.json(sys.argv[1])\
                    .registerTempTable('tweets')


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

    print ("Terminada la tarea de spark")
    sc.stop()
