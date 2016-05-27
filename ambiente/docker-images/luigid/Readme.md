
# Luigi

Este código nos va a generar la imagen de luigid y levantar el contenedor, dejándolo activo con el puerto 8082. En particular en el Dockerfile de la imagen de luigid podemos ver que instala python e instala los paquetes que necesitamos.

Como le asignamos el puerto 8082 a luigid, quiere decir que si nos vamos a la liga http://0.0.0.0:8082 en nuestro navegador podemos ver la interfaz de luigi que nos muestra la manera en cómo se están ejecutando los distintos tasks en los diferentes workes y un resumen de cuántos ya finalizaron, cuáles están pendientes y cuáles están corriendo en ese instante.
