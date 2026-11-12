# EDA Racismo y contranarrativa

Análisis exploratorio del Barómetro CIS 3536 (diciembre de 2025) sobre la distancia entre la autopercepción del racismo y la percepción de la sociedad española. Incluye una presentación HTML navegable, memoria breve, notebook y código reproducible.

## Resultados principales

- Media ponderada de autopercepción: **1,79/10**.
- Media ponderada atribuida a la sociedad: **5,24/10**.
- Brecha descriptiva: **3,45 puntos** (base válida n=3.913).
- La brecha aparece en los perfiles por sexo, edad, ingresos, ideología y estudios.

La encuesta recoge percepciones declaradas; no mide directamente actitudes o conductas discriminatorias. Las diferencias presentadas son descriptivas, sin inferencia causal ni contraste de significación entre grupos.

## Estructura

- `src/main.py`: limpieza, ponderación, agrupaciones y gráficos SVG.
- `src/data/raw/3536_etiq.csv`: microdatos anonimizados con etiquetas de respuesta.
- `src/data/resultados_ponderados.csv`: tabla agregada que genera el script.
- `src/main.ipynb`: recorrido resumido del análisis.
- `presentation/index.html`: presentación para público no técnico; navega con flechas del teclado.
- `presentation/assets/`: gráficos recreados desde el microdato y dos gráficos CIS de referencia facilitados para el proyecto.
- `docs/memoria.md`: memoria del proyecto y limitaciones.
- `docs/fuentes_datos.md`: procedencia y alcance de las fuentes.
- `docs/Ficha_Tecnica_CIS_3536.pdf`: ficha técnica usada.

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
- Cifras externas en la diapositiva final: [EPA 3T 2026 · INE](https://www.ine.es/dyngs/Prensa/EPA3T26.htm), [informe de población migrante · Ministerio de Sanidad](https://www.sanidad.gob.es/gabinete/notasPrensa.do?id=6924), [estadísticas del IMV · Seguridad Social](https://www.seg-social.es/wps/wcm/connect/wss/9d6df71d-1589-4b8d-990a-03cb323d5d4c/202605%2BCOMPLETO%2BDossier%2Bcomunidad%2Baut%C3%B3noma%2By%2Bprovincia.pdf?CACHEID=ROOTWORKSPACE.Z18_81D21J401P5L40QTIT61G41000-9d6df71d-1589-4b8d-990a-03cb323d5d4c-pWmQLz4&CONVERT_TO=linktext&MOD=AJPERES).

## Tecnologías

Python, pandas, NumPy, Matplotlib, Jupyter y HTML/CSS/JavaScript.
