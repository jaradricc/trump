# coding: utf-8

import os

import json

import datetime

import logging
logging.config.fileConfig('dpa_logging.conf')
logger = logging.getLogger('dpa.pipeline.etl')

import luigi
from luigi import configuration, LocalTarget
from luigi.s3 import S3Target, S3Client, S3FlagTarget, ReadableS3File
from luigi.contrib.spark import SparkSubmitTask, PySparkTask
import luigi.postgres


from pyspark import SparkContext
from pyspark.sql import HiveContext
from pyspark.sql import Row
from pyspark.conf import SparkConf

# from test import HolaMundoTask
# import test_spark


class AllTasks(luigi.WrapperTask):
    sighting_date = luigi.DateParameter(default = datetime.date.today())
    """
    Las WrapperTask ahorran el método output()
    Si se usa una clase normal, el pipeline siempre marcará error
    """
    def requires(self):
        # yield tweetsToDatabase(sighting_date = self.sighting_date)
        yield Tweets_String(sighting_date = self.sighting_date)
        yield Top_Users(sighting_date = self.sighting_date)

class ReadContainer(luigi.ExternalTask):
    def output(self):
        return luigi.s3.S3Target(configuration.get_config().get('etl','bucket')+'/05-19-20/')

class Top_Users(SparkSubmitTask):
    sighting_date = luigi.DateParameter()
    def requires(self):
        return ReadContainer()

    @property
    def name(self):
        return 'Top_Users'

    def app_options(self):
        return [self.input().path, self.output().path]

    @property
    def app(self):
        return 'top_users.py'


    def output(self):
        return luigi.file.LocalTarget('/home/dpa_worker/dashboard/{}{}{}top_users.json'.format(self.sighting_date.year,
                                                                                self.sighting_date.month,
                                                                                self.sighting_date.day))



class Tweets_String(SparkSubmitTask):
    sighting_date = luigi.DateParameter()
    bucket = configuration.get_config().get('etl','bucket')
    def requires(self):
        return ReadContainer()

    @property
    def name(self):
        return 'Tweets_String'

    def app_options(self):
        return [self.input().path, self.output().path]

    @property
    def app(self):
        return 'tweets_string.py'


    def output(self):
        return luigi.file.LocalTarget('/home/dpa_worker/model_data/{}{}{}tweets.json'.format(self.sighting_date.year,self.sighting_date.month,self.sighting_date.day))



if __name__ == '__main__':
    luigi.run()
