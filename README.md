# EDA Racismo y contranarrativa

Análisis exploratorio del Barómetro CIS 3536 (diciembre de 2025) sobre la distancia entre la autopercepción del racismo y la percepción de la sociedad española. Incluye una presentación HTML navegable, memoria breve, notebook y código reproducible.

## Resultados principales

- Media ponderada de autopercepción: **1,79/10**.
- Media ponderada atribuida a la sociedad: **5,24/10**.
- Brecha descriptiva: **3,45 puntos** (base válida n=3.913).
- La brecha aparece en los perfiles por sexo, edad, ingresos, ideología y estudios.

La encuesta recoge percepciones declaradas; no mide directamente actitudes o conductas discriminatorias. Se añaden contrastes exploratorios ponderados para ideología, edad y redes, sexo e ingresos controlando ideología. Son aproximados: no modelan todo el diseño complejo del CIS ni prueban causalidad.

## Estructura

- `src/main.py`: limpieza, ponderación, agrupaciones y gráficos SVG.
- `src/data/raw/3536_etiq.csv`: microdatos anonimizados con etiquetas de respuesta.
- `src/data/resultados_ponderados.csv`: tabla agregada que genera el script.
- `src/data/hipotesis_ponderadas.json`: resultados detallados de los cuatro contrastes.
- `src/main.ipynb`: recorrido resumido del análisis.
- `presentation/index.html`: presentación para público no técnico; navega con flechas del teclado.
- `presentation/assets/`: gráficos recreados desde el microdato y dos gráficos CIS de referencia facilitados para el proyecto.
- `docs/memoria.md`: memoria del proyecto y limitaciones.
- `docs/fuentes_datos.md`: procedencia y alcance de las fuentes.
- `docs/Ficha_Tecnica_CIS_3536.pdf`: ficha técnica usada.
- `docs/202601_IMV_Altas_acumuladas.xlsx`: fuente complementaria de altas iniciales acumuladas del IMV; no contiene desglose por nacionalidad.

## Ejecutar

Requiere Python 3.10+.

```bash
python -m pip install -r requirements.txt
python src/main.py --data src/data/raw/3536_etiq.csv
```

Abre `presentation/index.html` en un navegador. Para presentar, utiliza las flechas izquierda/derecha o los botones.

## Fuentes

- CIS, [estudio 3536: Barómetro de diciembre de 2025](https://www.cis.es/es/w/avance-de-resultados-del-estudio-3536-bar%C3%B3metro-de-diciembre-2025-).
- CIS, [ficha técnica del estudio](https://www.cis.es/documents/20117/13695327/FT3536.pdf/d4b82017-c271-d011-6f8d-012d68f7d8bd?t=1770303151042&version=1.0).
- Cifras externas en la diapositiva 14: [EPA 3T 2026 · INE](https://www.ine.es/dyngs/Prensa/EPA3T26.htm), [informe de población migrante · Ministerio de Sanidad](https://www.sanidad.gob.es/gabinete/notasPrensa.do?id=6924), [dosier IMV · Seguridad Social](https://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/cbe2fda1-3ac7-4bc8-a5ec-06c178839e11/0e716715-d290-4745-a74a-28cc1c3bc9ea/e221487c-d047-45cb-b862-8615b69f3ad4). El Excel incluido es un acumulado distinto y no sustenta el porcentaje por nacionalidad.

## Tecnologías

Python, pandas, NumPy, SciPy, statsmodels, Matplotlib, Jupyter y HTML/CSS/JavaScript.
