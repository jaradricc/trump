
# Luigi

Este código nos va a generar la imagen de luigid y levantar el contenedor, dejándolo activo con el puerto 8082. En particular en el Dockerfile de la imagen de luigid podemos ver que instala python e instala los paquetes que necesitamos.


```python
FROM python:3.4-onbuild

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /etc/luigi
ADD luigi.cfg /etc/luigi/luigi.cfg

RUN mkdir /var/log/luigid
ADD logrotate.cfg /etc/logrotate.d/luigid
VOLUME /var/log/luigid

RUN mkdir /var/run/luigid
VOLUME /var/run/luigid

CMD ["/usr/local/bin/luigid"]
EXPOSE 8082

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
```

Esto nos va a generar la imagen de luigid y levantar el contenedor, dejándolo activo con el puerto 8082. En particular en el Dockerfile de la imagen de luigid podemos ver que instala python e instala los paquetes que necesitamos.


Como le asignamos el puerto 8082 a luigid, quiere decir que si nos vamos a la liga http://0.0.0.0:8082 en nuestro navegador podemos ver la interfaz de luigi que nos muestra la manera en cómo se están ejecutando los distintos tasks en los diferentes workes y un resumen de cuántos ya finalizaron, cuáles están pendientes y cuáles están corriendo en ese instante.
