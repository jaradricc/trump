FROM r-base:latest



COPY ./requirements.R /root/requirements.R
WORKDIR /root

RUN Rscript requirements.R

COPY ./App/ /root

CMD ["/bin/sh"]
