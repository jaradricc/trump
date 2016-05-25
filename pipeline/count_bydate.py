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



if __name__ == "__main__":
    print ("Iniciada la tarea de spark")
    sc = SparkContext()
    sqlCtx = HiveContext(sc)

    sqlCtx.read.json(sys.argv[1])\
                    .registerTempTable('tweets')

    def clean_date(date):
        month_num ={v: "%02d" % (k,) for k,v in enumerate(calendar.month_abbr)}
        day =  date.split(' ')[2]
        month = month_num[date.split(' ')[1]]
        year = date.split(' ')[5]
        new_date = month + '/' + day + '/' + year
        return new_date

    sqlCtx.registerFunction('clean_date', clean_date, StringType())

    def create_ReTweet(text):
        if ('RT' in text):
            retweet = 1
        else:
            retweet = 0
        return retweet

    def create_Tweet(text):
        if ('RT' not in text):
            tweet = 1
        else:
            tweet = 0
        return tweet

    sqlCtx.registerFunction('create_ReTweet', create_ReTweet, IntegerType())
    sqlCtx.registerFunction('create_Tweet', create_Tweet, IntegerType())

    fechas3 = sqlCtx.sql('select  clean_date(created_at)  as created_at,\
                text,\
                create_ReTweet(text) as Retweet, \
                create_Tweet(text) as Tweet \
                from tweets')

    fechas3.registerTempTable('fechas3')

    sqlCtx.sql('select  created_at,  sum(Retweet) as Retweets, sum(Tweet) as Tweets\
        from fechas3\
        group by created_at ')\
        .toPandas()\
        .to_json(sys.argv[2])

    print ("Terminada la tarea de spark")
    sc.stop()
