#Sentinel Index Extractor
Se trata de una herramienta para el procesamiento de imagenes del satélite Sentinel-2. Este módulo de QGIS permite calcular una serie de índices espectrales del tile de Sentinel-2 seleccionado.

##Guía de uso
Para instalar la herramienta ha de comprimirse en un ZIP todo el directorio descargado o usar el ZIP que se descarga directamente uno de Github. 
Después ver [Cómo instalar un complemento en QGIS](https://docs.qgis.org/2.18/es/docs/training_manual/qgis_plugins/fetching_plugins.html)

Una vez instalada la herramienta, para lanzarla, deberemos irnos a Complementos>Sentinel-2 Index Extractor>Extract VI for Sentinel-2 data.
La ventana inicial está compuesta por las siguientes entradas:
1. La ruta donde se encuentra almacenado el fichero comprimido (.zip) que contiene todas las imágenes y bandas de sentinel-2. Es el fichero que se descarga directamente de la plataforma de imágenes Sentinel. Dicho fichero deberá tener los siguientes requisitos:
  * Ser un producto de Sentinel-2
  * Ser un producto de nivel 2A (producto ya corregido atmosféricamente).

2.[OPCIONAL] Nombre de la capa 'Shape' que se puede usar para generar los índices sólo del área contenida en ese shape. Si se deja en blanco se generarán los índices para todo el área.

3.[OPCIONAL] Alternativamente se pueden guardar los resultados en un fichero CSV que contiene por columnas los siguientes datos:
  *.Ubicación en las coordenadas WGS84 / UTM eje X
  *.Ubicación en las coordenadas WGS84 / UTM eje Y
  *.Valor del índice previo al remuestreo que se efectúa para convertir un valor en el rango de salida al rango [0,255].

Una vez introducidos todos los datos, podremos elegir tantos índices como queramos.

Al pulsar la tecla 'OK', nos saldrá el mensaje que deberemos de Aceptar para proseguir con la ejecución. Dicho mensaje es un aviso de que el programa podría tardar largo tiempo en realizar los cálculos puesto que son tareas muy pesadas. A modo de avisar al usuario de que no cierre el programa debido a la tardanza de Ã©ste en generar los resultados .

Una vez calculados los índices espectrales, se habrán producido los siguientes recursos:

1.Los índices convertidos a imágenes en la pestaña de capas. 

2.Las imágenes almacenadas en el mismo directorio donde se encuentra el producto Sentinel-2 de origen (el comprimido .zip)

3.El fichero CSV (si se ha seleccionado) con los datos del índice espectral en la misma ruta que las imágenes y el fichero comprimido original.

 

Para hacer uso de la funcionalidad de 'Shape' deberemos generar una nueva capa de archivo 'Shape' como se muestra a continuación:

El nombre de la capa que se elija será el identificador que se usará para añadir en el campo de Shape de la herramienta.

Una vez creado, iremos generando los puntos que conforman nuestra área hasta un mínimo de 3 puntos. La herramienta generará el índice para el área cuadrada mínima que sea capaz de incluir al área formada por los puntos del Shape.

Para generar los puntos seleccionaremos la opción conmutar edición y generar punto.

Ahora podremos pinchar en cualquier área del mapa y generará nuestro punto, nos pedirá que a cada punto que generemos le asignemos un identificador, Ã©ste puede ser el que quiera escoger el usuario y no tiene importancia real en nuestro módulo, a modo de ejemplo nosotros les iremos asignando el 1,2,3 etc.

Una vez egresados los puntos podremos ingresar el nombre del Shape en la herramienta y Ã©sta calculará los índices elegidos sólo para esa área.


