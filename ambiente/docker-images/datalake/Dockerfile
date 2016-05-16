FROM busybox

RUN mkdir -p /datalake \
             /datalake/tmp

RUN chown -R root:users /datalake
RUN chmod -R g+rwx /datalake

VOLUME ["/datalake"]
