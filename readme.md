# Proyecto de Análisis de Mortalidad en Colombia 2019

**Autores:**  
Ana María García Arias y Diana Carolina González Díaz

**Asignatura:**  
Aplicaciones I – Maestría en Inteligencia Artificial

**Universidad La Salle**

**Fecha:**  
Mayo 2025

---

## **Introducción**

Este proyecto presenta una aplicación web interactiva para el análisis de la mortalidad en Colombia durante 2019, desarrollada con **Python** y las librerías **Dash** y **Plotly**.

El **enfoque de desarrollo** se basa en:

- **Python** como lenguaje de backend, para el procesamiento de datos, agrupaciones y cálculo de estadísticas con **pandas**.  
- **Dash** como framework ligero que, sobre Flask y React, expone funciones de Python directamente en componentes web (gráficos, controles, tablas).  
- **Plotly** para crear visualizaciones ricas e interactivas (zoom, hover, filtros en vivo) sin escribir JavaScript.  

De esta manera, cada callback en el servidor de Dash recibe los inputs (dropdowns, botones) y devuelve una figura o un layout actualizado, logrando una experiencia de usuario fluida y reactiva.

**Objetivos del proyecto:**

1. **Recopilar y preparar los datos.**  
   Se partió de tres fuentes en Excel:  
   - “Datos de Mortalidad”  
   - “Códigos de Causa de Muerte”  
   - “Divipola” (división político-administrativa)  

   Estos archivos se cargan y limpian con **pandas**, generando CSV y un GeoJSON optimizados para la app. El detalle del procesamiento está en el notebook [GeneracionArchivosProcesados.ipynb](./GeneracionArchivosProcesados.ipynb).

2. **Visualizar patrones descriptivos.**  
   Usando **Plotly** dentro de Dash, se generan varios componentes interactivos:
   - Mapa coroplético de muertes por departamento  
   - Gráficos de líneas mensuales  
   - Barras horizontales y apiladas  
   - Histograma por rango de edad  
   - Gráfico circular y tablas dinámicas  

3. **Desplegar la aplicación.**  
   Finalmente, la app se publica en la nube con Render, garantizando acceso público y despliegue continuo al hacer push en GitHub.

---
## Desarrollo de la Aplicación Web

La aplicación se construyó siguiendo una **arquitectura modular** centrada en la separación de responsabilidades y la escalabilidad. En lugar de un único archivo monolítico, dividimos la lógica en pequeños módulos independientes, cada uno encargado de una parte específica de la interfaz y de sus interacciones. Un archivo orquestador principal (`app.py`) actúa como punto de entrada, gestionando la navegación entre los distintos módulos y registrando sus callbacks.

**Puntos clave de la metodología:**

- **Modularidad**  
  Cada sección de la aplicación reside en su propio archivo dentro de la carpeta `paginas/`. Esto facilita entender, mantener y extender funcionalidades sin afectar al resto del proyecto.

- **Orquestador central**  
  El archivo `app.py` importa los layouts y registra los callbacks de todos los módulos. A través de un mecanismo de enrutamiento sencillo, detecta la ruta actual en el navegador y despliega la página correspondiente. Añadir o quitar secciones se limita a editar este orquestador.

- **Consistencia visual**  
  Todos los módulos comparten estilos definidos de antemano (fondo negro, controles y botones en fucsia, tipografía y tamaños coherentes). Esto garantiza una experiencia de usuario uniforme y un “look & feel” profesional en toda la app.

- **Callbacks aislados**  
  Cada módulo expone su propia función de registro de callbacks, de modo que cada filtro o visualización se actualiza de forma independiente, evitando interferencias.

- **Escalabilidad y reutilización**  
  Incorporar nuevos informes o secciones implica sólo crear un nuevo módulo con su layout y callbacks, importarlo y registrarlo en `app.py`. Los controles y estilos comunes se reutilizan, minimizando la duplicación.

### Estructura de Módulos
```
paginas/
├─ portada.py             # Página de bienvenida con información del proyecto
├─ mapa.py                # Mapa coroplético de muertes por departamento
├─ muertePorMes.py        # Serie de tiempo de muertes mensuales
├─ CiudadesMasViolentas.py# Top 5 municipios más violentos
├─ IndiceMortalidad.py    # Ciudades con menor índice de mortalidad (pie chart)
├─ HistogramaMortalidad.py# Distribución de muertes por rango de edad
├─ TablaCausasMuertes.py  # Tabla de las 10 principales causas de muerte
└─ MuertesPorSexo.py      # Barras apiladas de muertes por sexo y departamento
```

### Cómo interactúa el usuario en cada sección:

**Portada:** Presentación del proyecto y botón “Informe” para iniciar el recorrido.

![Portada](assets\Portada.jpg)

**Página 1 - Mapa:**  

El mapa coroplético presenta la distribución de muertes por departamento en Colombia, utilizando una escala de color que va de amarillo claro (menos muertes) a rojo intenso (más muertes). El usuario puede seleccionar filtros de sexo y causa de muerte mediante menús desplegables, y los resultados se actualizan en tiempo real, permitiendo explorar visualmente las regiones con mayor incidencia de mortalidad.

**Interpretación**

La primera impresión es que Antioquia (o la región central) muestra la mayor concentración de muertes (rojo intenso), seguida de departamentos como Santander, Cundinamarca y Valle del Cauca con tonos amarillos más oscuros (indicando cifras intermedias). Gran parte del país aparece en blanco o amarillo muy claro, lo que sugiere que esos departamentos presentaron relativamente pocas muertes en 2019. Al aplicar los filtros de sexo o causa, podríamos ver cómo cambian esos patrones—por ejemplo, si las muertes por homicidio se concentran en determinadas regiones o si hay diferencias marcadas entre masculino y femenino.

![Mapa](assets\Mapa.jpg)

**Página 2 -Muertes por Mes** 

En esta ventana el usuario encuentra una serie de tiempo que muestra el total de muertes ocurridas en cada mes del año. Los dropdowns permiten filtrar por sexo, hora del día y manera de muerte, actualizando dinámicamente la línea. La gráfica usa marcadores y líneas para resaltar los puntos mensuales, sobre un fondo oscuro que facilita la lectura de la curva. Al pie, un botón “Volver al Mapa” regresa al análisis geográfico.

**Interprretación**

Se aprecia un bache pronunciado en febrero, donde las muertes caen a su nivel más bajo (cerca de 18 000), seguido de un repunte en marzo. A partir de marzo, la tendencia es al alza, alcanzando un pico en julio y otro aún mayor en diciembre (más de 21 500 muertes). Este patrón sugiere factores estacionales o eventos (por ejemplo, fenómenos climáticos, festividades o brotes epidémicos) que modifican la mortalidad mensual. Aplicando los filtros se podría investigar, por ejemplo, si esta caída en febrero corresponde a menos accidentes de tránsito o si difiere entre masculino y femenino.

![Muertes Por Mes](assets\MuertesPorMes.jpg)

**Página 3 - Ciudades más violentas**

Aquí se muestra un gráfico de barras horizontales destacando las cinco ciudades con mayor número de muertes por homicidio. En la parte superior están los filtros de mes y sexo, capaces de recalcular en tiempo real las barras. Cada barra tiene un color que va de verde (menos muertes) a rojo (más muertes), y la escala de colores aparece a la derecha. En la esquina superior derecha hay botones de Volver (regresa a la sección anterior) y Siguiente (avanza al siguiente módulo).

**Interpretación**

Sorprende que ciudades menos pobladas —como Florencia y Armenia— encabecen la lista de homicidios, con cifras de alrededor de 5 500 muertes. Esto sugiere un índice de violencia muy alto en estas localidades, superando incluso a grandes urbes. La estrecha diferencia entre los valores de las cinco primeras indica que el problema de homicidios está bastante distribuido en varios municipios. Al cambiar filtros (por ejemplo seleccionando solo masculino o un mes específico), podríamos revelar si estos picos corresponden a episodios concretos o si la violencia es persistente a lo largo del año.

![Muertes Por Mes](assets\CiudadesViolentas.jpg)

**Página 4 - Top Ciudades con menor indice Mortalidad**

En este módulo se presenta un gráfico circular que destaca las diez ciudades con el menor número absoluto de muertes durante 2019. Arriba, los filtros de mes y sexo permiten recalcular el gráfico dinámicamente. Cada porción del pastel corresponde a una ciudad y su porcentaje respecto al total de muertes filtrado. Los botones “Volver” y “Siguiente” facilitan la navegación entre secciones.

**Interpretación**

El pastel muestra que todas las ciudades listadas tienen valores muy cercanos (cada una representa alrededor del 10 %), lo que indica que el límite entre la décima y la undécima posición es muy estrecho. Ciudades como Aldana, Chitaraque y Belén de los Andaquíes aparecen con secciones de color vibrante, señalando que, aunque su mortalidad es baja en términos absolutos, son representativas cuando se normaliza al subconjunto más pequeño. Este gráfico sugiere que existe un grupo homogéneo de municipios con índices bajos de mortalidad, probablemente por su baja población o condiciones locales de baja exposición a riesgos. Al filtrar por sexo o mes, podríamos descubrir si en alguno de esos lugares hay picos atípicos o si la baja mortalidad se mantiene estable.

![Indice Menor Mortalidad](assets\IndiceMenorMortalidad.jpg)

**Página 5 - Top 10 principales causas de muerte en Colombia**

Aquí se presenta una tabla dinámica con las diez causas de muerte más frecuentes durante 2019, mostrando el código CIE-10, la descripción de la causa y el total de casos. Arriba, los filtros de mes, sexo y municipio permiten acotar el subconjunto de datos y recalcular al instante la lista. Debajo de la tabla, los botones “Volver” y “Siguiente” facilitan la navegación a los módulos anterior y siguiente.

**Interpretación**

La causa principal es el infarto agudo de miocardio (I219), con más de 615 000 casos, muy por encima de la segunda—la EPOC con infección respiratoria (~149 000). Esto subraya que las enfermedades cardiovasculares dominan la mortalidad en Colombia. Además, llama la atención la presencia de neumonías (J189) y tumores malignos (estómago, bronquios, mama), reforzando la relevancia de los sistemas respiratorio y digestivo en la carga de enfermedad. El filtro por municipio podría revelar variaciones locales, por ejemplo si en zonas rurales las infecciones respiratorias superan a los infartos, o si algunos municipios registran picos de homicidios codificados como “X954”.

![Top 10 Causas de Muerte](assets\Top_10_Causas_de_Muerte.jpg)

**Página 6 - Muertes por Rangos de edad**

Esta pantalla muestra un histograma de muertes agrupadas en rangos quinquenales (0–4, 5–9, …, 85+). Los filtros de mes y sexo en la parte superior permiten segmentar la población y recalcular la altura de las barras en tiempo real. Cada barra, pintada en un rosa suave sobre fondo oscuro, representa el conteo de muertes en ese rango de edad. Por debajo, los botones “Volver” y “Siguiente” mantienen la navegación intuitiva.

**Interpretación**

Se observa que el rango 65–69 es donde el conteo de muertes alcanza su pico más alto (~32), seguido de 45–49 y 85+. Los grupos intermedios (30–34, 35–39, 50–54) presentan valores moderados, mientras que los extremos (0–4, 5–9) son más bajos, como era de esperar en poblaciones infantiles. Este patrón confirma que la mortalidad aumenta con la edad, con un punto de inflexión marcado en la sexta y séptima década, posiblemente ligado a enfermedades crónicas más prevalentes en adultos mayores. Filtrando por sexo o mes se puede identificar si los picos se deben a factores estacionales o a diferencias biológicas entre hombres y mujeres.

![Muertes por edad](assets\MuertePorEdad.jpg)

**Página 7 - Muertes por departamento y Sexo**

En este módulo se presenta un gráfico de barras horizontales apiladas que compara, departamento a departamento, la cantidad de muertes por sexo (masculino, femenino y no definido). Arriba, un dropdown permite filtrar por manera de muerte, recalculando instantáneamente las barras. A la derecha aparece la leyenda de colores; en la parte superior derecha, los botones “Volver” (regresa al histograma) e “Inicio” (vuelve a la portada). El fondo negro y los colores vibrantes (rosa para masculino, azul para femenino) mantienen la coherencia visual del dashboard.

**Interpretación**

* Antioquia domina con creces el total de muertes, especialmente en el sexo femenino (barra rosa), seguido por Cundinamarca y Valle del Cauca.

* En departamentos pequeños (Vaupés, Guainía, etc.) las barras son casi invisibles, confirmando su baja mortalidad.

* La proporción masculina (azul) es notable pero siempre menor que la femenina en cada departamento, lo que sugiere una mayor incidencia de fallecimientos en mujeres.

* Al filtrar por una causa (por ejemplo “Homicidio” o “Natural”), se podría observar si ciertos departamentos presentan una distribución de sexo más equilibrada o si mantienen la misma brecha de género.

![Muertes por Dpto y Sexo](assets\MuertesDptoSexo.jpg)

---

## Cómo Ejecutar Localmente

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/Nany1993/App-PlotyDash.git
   cd App-PlotyDash

2. **Crear y activar un entorno virtual**
* Windows (PowerShell):

    ```bash python -m venv venv
    .\venv\Scripts\Activate.ps1 
    ```

* Windows (CMD):

    ```bash python -m venv venv
    venv\Scripts\activate.bat
    ```
* Linux/MacOS:
    ```bash python3 -m venv venv
    source venv/bin/activate
    ```

3. **Instalar dependencias**

    ``` pip install -r requirements.txt```

4. **Ejecutar la aplicación**

    ``` python app.py```

5. **Abrir en el navegador**

    Accede a:

    ``` http://127.0.0.1:8050```

6. **Navegación**

**Usa los botones “Informe”, “Volver” y “Siguiente” o cambia la URL a:**

    /mapa

    /muerte-por-mes

    /ciudades-mas-violentas

    /indice-mortalidad

    /histograma-mortalidad

    /tabla-causas

    /muertes-por-sexo

7. **Detener la aplicación**

    Presiona Ctrl+C en la terminal donde corre python app.py


## Enlaces de Proyecto

- 🔗 **Repositorio en GitHub**  
  [App-PlotyDash](https://github.com/Nany1993/App-PlotyDash)

- 🚀 **Demo en Render**  
  [https://app-plotydash.onrender.com](https://app-plotydash.onrender.com)
