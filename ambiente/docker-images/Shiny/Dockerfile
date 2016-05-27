FROM r-base:latest


COPY ./App/ /root
COPY ./requirements.R /root/requirements.R
WORKDIR /root

RUN Rscript requirements.R

CMD ["/bin/sh"]
