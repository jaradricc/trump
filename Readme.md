# Ambiente
El ambiente consta de los componentes:
* Luigi (con su luigi worker).
* Spark (con su worker).
* Postgres.

## Particularidades del ambiente.
En general, se levanta utilizando el docker-compose, sin embargo Spark requiere que exista la imágen dpa/base la cual se construye con el comando:
```bash
docker build --force-rm -t dpa/base docker-images/base
```
