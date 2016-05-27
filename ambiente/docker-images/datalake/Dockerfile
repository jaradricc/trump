FROM busybox
RUN mkdir /test

RUN mkdir -p /datalake \
             /datalake/tmp

RUN chown -R root:users /datalake
RUN chmod -R g+rwx /datalake

ADD 2016523top_hashtags.json /datalake/2016523top_hashtags.json

ADD 2016523top_users.json /datalake/2016523top_users.json

ADD dates_prueba.csv /datalake/dates_prueba.csv 


VOLUME ["/datalake"]
