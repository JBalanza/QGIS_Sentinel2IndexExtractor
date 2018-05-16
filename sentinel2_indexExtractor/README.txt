<html>
<body>
<p class="MsoNormal">Una vez instalada la herramienta para lanzarla, deberemos
irnos a <i style="mso-bidi-font-style:normal">Complementos&gt;Sentinel-2 Index
Extractor&gt;Extract VI for Sentinel-2 data</i>.</p>

<p class="MsoNormal" align="center" style="text-align:center"><v:shapetype id="_x0000_t202" coordsize="21600,21600" o:spt="202" path="m,l,21600r21600,l21600,xe">
 <v:stroke joinstyle="miter">
 <v:path gradientshapeok="t" o:connecttype="rect">
</v:path></v:stroke></v:shapetype><v:shape id="_x0000_s1028" type="#_x0000_t202" style="position:absolute;
 left:0;text-align:left;margin-left:239.65pt;margin-top:82.2pt;width:18.55pt;
 height:19.9pt;z-index:3" filled="f" stroked="f" strokecolor="red"><br></v:shape></p>
  <!--[endif]-->
<v:shape id="_x0000_s1026" type="#_x0000_t202" style="position:absolute;
 left:0;text-align:left;margin-left:244.9pt;margin-top:41.55pt;width:18.55pt;
 height:19.9pt;z-index:1" filled="f" stroked="f" strokecolor="red"><br></v:shape><v:shape id="_x0000_s1027" type="#_x0000_t202" style="position:absolute;
 left:0;text-align:left;margin-left:230.4pt;margin-top:65.05pt;width:18.55pt;
 height:19.9pt;z-index:2" filled="f" stroked="f" strokecolor="red"><v:textbox><br></v:textbox></v:shape>

<p class="MsoNormal">La ventana inicial está compuesta por las siguientes partes:</p>

<p class="MsoListParagraphCxSpFirst" style="margin-left:49.65pt;mso-add-space:
auto;text-indent:-18.0pt;mso-list:l0 level1 lfo2"><!--[if !supportLists]--><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Times New Roman&quot;"><span style="mso-list:Ignore">1.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->La ruta donde se encuentra almacenado el fichero
comprimido (.zip) que contiene todas las imágenes y bandas de sentinel-2. Es el
fichero que se descarga directamente de la plataforma de imágenes Sentinel. Dicho fichero deberá tener los siguientes
requisitos:</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:108.0pt;mso-add-space:
auto;text-indent:-108.0pt;mso-text-indent-alt:-9.0pt;mso-list:l0 level3 lfo2"><!--[if !supportLists]--><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Times New Roman&quot;"><span style="mso-list:Ignore"><span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span>i.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->Ser un producto de Sentinel-2</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:108.0pt;mso-add-space:
auto;text-indent:-108.0pt;mso-text-indent-alt:-9.0pt;mso-list:l0 level3 lfo2"><!--[if !supportLists]--><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Times New Roman&quot;"><span style="mso-list:Ignore"><span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span>ii.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->Ser un producto de nivel 2A (producto ya
corregido atmosféricamente).</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:49.65pt;mso-add-space:
auto;text-indent:-18.0pt;mso-list:l0 level1 lfo2"><!--[if !supportLists]--><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Times New Roman&quot;"><span style="mso-list:Ignore">2.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->Nombre de la capa 'Shape' que se puede usar para
generar los índices sólo del área contenida en ese shape. Si se deja en blanco
se generarán los índices para todo el área.</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:49.65pt;mso-add-space:
auto;text-indent:-18.0pt;mso-list:l0 level1 lfo2"><!--[if !supportLists]--><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Times New Roman&quot;"><span style="mso-list:Ignore">3.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->Alternativamente se pueden guardar los
resultados en un fichero CSV que contiene por columnas los siguientes datos:</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:108.0pt;mso-add-space:
auto;text-indent:-108.0pt;mso-text-indent-alt:-9.0pt;mso-list:l0 level3 lfo2"><!--[if !supportLists]--><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Times New Roman&quot;"><span style="mso-list:Ignore"><span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span>i.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->Ubicación en las coordenadas WGS84 / UTM eje X</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:108.0pt;mso-add-space:
auto;text-indent:-108.0pt;mso-text-indent-alt:-9.0pt;mso-list:l0 level3 lfo2"><!--[if !supportLists]--><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Times New Roman&quot;"><span style="mso-list:Ignore"><span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span>ii.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->Ubicación en las coordenadas WGS84 / UTM eje Y</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:108.0pt;mso-add-space:
auto;text-indent:-108.0pt;mso-text-indent-alt:-9.0pt;mso-list:l0 level3 lfo2"><!--[if !supportLists]--><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-bidi-font-family:&quot;Times New Roman&quot;"><span style="mso-list:Ignore"><span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span>iii.<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->Valor del índice previo al remuestreo que se
efectúa para convertir un valor en el rango de salida al rango [0,255].</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:108.0pt;mso-add-space:
auto"><o:p>&nbsp;</o:p></p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:0cm;mso-add-space:auto">Una
vez ingresados todos los datos, podremos elegir tantos índices como queramos.</p>

<p class="MsoNormal" align="center" style="text-align:center"><i style="mso-bidi-font-style:
normal"><o:p>&nbsp;</o:p></i></p>

<p class="MsoNormal">Una vez seleccionados todos los índices que necesitemos y al
pulsar la tecla 'OK', nos saldrá el mensaje que deberemos de Aceptar para
proseguir con la ejecución. Dicho mensaje es un aviso de que el programa podría
tardar largo tiempo en realizar los cálculos puesto que son tareas muy pesadas.
A modo de avisar al usuario de que no cierre el programa debido a la tardanza
de éste en generar los resultados .</p>

<p class="MsoNormal">Una vez calculados los índices espectrales, se habrán
producido los siguientes recursos:</p>

<p class="MsoListParagraphCxSpFirst" style="margin-left:49.65pt;mso-add-space:
auto;text-indent:-18.0pt;mso-list:l1 level1 lfo1"><!--[if !supportLists]--><span style="font-family:Symbol;mso-fareast-font-family:Symbol;mso-bidi-font-family:
Symbol"><span style="mso-list:Ignore">·<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->Los índices convertidos a imágenes en la pestaña
de capas.&nbsp;</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:49.65pt;mso-add-space:
auto;text-indent:-18.0pt;mso-list:l1 level1 lfo1"><!--[if !supportLists]--><span style="font-family:Symbol;mso-fareast-font-family:Symbol;mso-bidi-font-family:
Symbol"><span style="mso-list:Ignore">·<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->Las imágenes almacenadas en el mismo directorio
donde se encuentra el producto Sentinel-2 de origen (el comprimido .zip)</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:49.65pt;mso-add-space:
auto;text-indent:-18.0pt;mso-list:l1 level1 lfo1"><!--[if !supportLists]--><span style="font-family:Symbol;mso-fareast-font-family:Symbol;mso-bidi-font-family:
Symbol"><span style="mso-list:Ignore">·<span style="font:7.0pt &quot;Times New Roman&quot;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</span></span></span><!--[endif]-->El fichero CSV (si se ha seleccionado) con los
datos del índice espectral en la misma ruta que las imágenes y el fichero
comprimido original.</p>

<p class="MsoListParagraphCxSpMiddle" style="margin-left:49.65pt;mso-add-space:
auto"><o:p>&nbsp;</o:p></p>

<p class="MsoNormal">Para hacer uso de la funcionalidad de <i style="mso-bidi-font-style:
normal">'Shape</i>'<i style="mso-bidi-font-style:normal"> </i>deberemos generar
una nueva capa de archivo 'Shape' como se muestra a continuación:</p>

<p class="MsoNormal" align="center" style="text-align:center"><span style="mso-fareast-language:ES;mso-no-proof:yes"><v:shape id="Imagen_x0020_14" o:spid="_x0000_i1028" type="#_x0000_t75" style="width:393pt;height:183.75pt;
 visibility:visible;mso-wrap-style:square" o:bordertopcolor="black" o:borderleftcolor="black" o:borderbottomcolor="black" o:borderrightcolor="black">
 <v:imagedata src="file:///C:\Users\JAVIER\AppData\Local\Temp\msohtmlclip1\01\clip_image005.png" o:title="" cropbottom="40664f" cropright="35600f">
 <w:bordertop type="single" width="6">
 <w:borderleft type="single" width="6">
 <w:borderbottom type="single" width="6">
 <w:borderright type="single" width="6">
</w:borderright></w:borderbottom></w:borderleft></w:bordertop></v:imagedata></v:shape><v:shape id="Imagen_x0020_17" o:spid="_x0000_i1027" type="#_x0000_t75" style="width:393pt;height:223.5pt;visibility:visible;mso-wrap-style:square" o:bordertopcolor="black" o:borderleftcolor="black" o:borderbottomcolor="black" o:borderrightcolor="black">
 <v:imagedata src="file:///C:\Users\JAVIER\AppData\Local\Temp\msohtmlclip1\01\clip_image006.png" o:title="" croptop="17463f" cropbottom="16846f" cropleft="24273f" cropright="10403f">
 <w:bordertop type="single" width="6">
 <w:borderleft type="single" width="6">
 <w:borderbottom type="single" width="6">
 <w:borderright type="single" width="6">
</w:borderright></w:borderbottom></w:borderleft></w:bordertop></v:imagedata></v:shape></span></p>

<p class="MsoNormal" align="center" style="text-align:center">El nombre de la capa que se elija será el identificador que
se usará para añadir en el campo de <i>Shape</i>
de la herramienta.<br></p>

<p class="MsoNormal">Una vez creado, iremos generando los puntos que conforman
nuestra área hasta un mínimo de 3 puntos. La herramienta generará el índice
para el área cuadrada mínima que sea capaz de incluir al área formada por los
puntos del <i style="mso-bidi-font-style:normal">Shape.<o:p></o:p></i></p>

<p class="MsoNormal">Para generar los puntos seleccionaremos la opción conmutar
edición y generar punto.</p>

<p class="MsoNormal" align="center" style="text-align:center"><v:shapetype id="_x0000_t32" coordsize="21600,21600" o:spt="32" o:oned="t" path="m,l21600,21600e" filled="f">
 <v:path arrowok="t" fillok="f" o:connecttype="none">
 <o:lock v:ext="edit" shapetype="t">
</o:lock></v:path></v:shapetype><v:shape id="_x0000_s1031" type="#_x0000_t32" style="position:absolute;
 left:0;text-align:left;margin-left:252.45pt;margin-top:290.75pt;width:28.5pt;
 height:4.5pt;flip:x;z-index:6" o:connectortype="straight" strokecolor="red">
 <v:stroke endarrow="block">
</v:stroke></v:shape><v:shape id="_x0000_s1030" type="#_x0000_t32" style="position:absolute;
 left:0;text-align:left;margin-left:238.95pt;margin-top:50.75pt;width:5.25pt;
 height:49.5pt;flip:x y;z-index:5" o:connectortype="straight" strokecolor="red">
 <v:stroke endarrow="block">
</v:stroke></v:shape><v:shape id="_x0000_s1029" type="#_x0000_t32" style="position:absolute;
 left:0;text-align:left;margin-left:202.2pt;margin-top:50.75pt;width:5.25pt;
 height:49.5pt;flip:y;z-index:4" o:connectortype="straight" strokecolor="red">
 <v:stroke endarrow="block">
</v:stroke></v:shape><span style="mso-fareast-language:ES;mso-no-proof:yes"><v:shape id="Imagen_x0020_20" o:spid="_x0000_i1026" type="#_x0000_t75" style="width:194.25pt;height:313.5pt;
 visibility:visible;mso-wrap-style:square" o:bordertopcolor="black" o:borderleftcolor="black" o:borderbottomcolor="black" o:borderrightcolor="black">
 <v:imagedata src="file:///C:\Users\JAVIER\AppData\Local\Temp\msohtmlclip1\01\clip_image007.png" o:title="" cropbottom="20737f" cropright="49932f">
 <w:bordertop type="single" width="6">
 <w:borderleft type="single" width="6">
 <w:borderbottom type="single" width="6">
 <w:borderright type="single" width="6">
</w:borderright></w:borderbottom></w:borderleft></w:bordertop></v:imagedata></v:shape></span></p>

<p class="MsoNormal" align="center" style="text-align:center">Ahora podremos pinchar en cualquier área del mapa y generará
nuestro punto, nos pedirá que a cada punto que generemos le asignemos un
identificador, éste puede ser el que quiera escoger el usuario y no tiene
importancia real en nuestro módulo, a modo de ejemplo nosotros les iremos
asignando el 1,2,3 etc.<br></p>

<p class="MsoNormal">Una vez egresados los puntos podremos ingresar el nombre del
<i style="mso-bidi-font-style:normal">Shape</i> en la herramienta y ésta
calculará los índices elegidos sólo para esa área.</p>

<p class="MsoNormal"><span style="mso-fareast-language:ES;mso-no-proof:yes"><v:shape id="Imagen_x0020_23" o:spid="_x0000_i1025" type="#_x0000_t75" style="width:430.5pt;
 height:327.75pt;visibility:visible;mso-wrap-style:square" o:bordertopcolor="black" o:borderleftcolor="black" o:borderbottomcolor="black" o:borderrightcolor="black">
 <v:imagedata src="file:///C:\Users\JAVIER\AppData\Local\Temp\msohtmlclip1\01\clip_image008.png" o:title="" cropbottom="2465f" cropright="18956f">
 <w:bordertop type="single" width="6">
 <w:borderleft type="single" width="6">
 <w:borderbottom type="single" width="6">
 <w:borderright type="single" width="6">
</w:borderright></w:borderbottom></w:borderleft></w:bordertop></v:imagedata></v:shape></span></p>

<p class="MsoNormal" align="center" style="text-align:center"><br></p>
</body>
</html>
