FROM busybox

RUN mkdir -p /data/bd \
             /data/models \
             /data/reports \
             /data/tmp

RUN chown -R root:users /data
RUN chmod -R g+rwx /data

VOLUME ["/data"]
