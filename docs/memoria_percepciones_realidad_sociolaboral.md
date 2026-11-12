# Percepciones sobre racismo y realidad sociolaboral en España (CIS 3536)

**Autor/a:** Alejandro Rodríguez Peña  
**Módulo:** Data Analysis · Bootcamp de Data Science  
**Fecha:** 12 de noviembre de 2026  
**Tipo de proyecto:** descriptivo, exploratorio y estadístico. Sin Machine Learning ni afirmaciones causales.

> **Nota de alcance:** este documento organiza la información de trabajo proporcionada para el proyecto. Las cifras externas y los resultados de hipótesis deben cotejarse con los ficheros, tablas y publicaciones primarias enlazadas antes de su difusión. Los resultados del proyecto CIS ya calculados en el repositorio se identifican en el apartado correspondiente; cifras de análisis adicionales aquí reseñadas requieren reproducir el script actualizado.

## 1. Propósito de esta memoria

La memoria complementa una presentación oral de hasta 15 minutos. Registra las fuentes, decisiones metodológicas, técnicas, dificultades y límites que no caben en las diapositivas. No pretende demostrar causalidad, etiquetar moralmente a personas o grupos, ni convertir percepciones declaradas en diagnósticos objetivos. Los resultados del bloque CIS son descriptivos y asociativos.

## 2. Preguntas de investigación

El proyecto plantea dos preguntas relacionadas:

1. ¿Qué distancia hay entre cómo se perciben las personas y cómo perciben a la sociedad en materia de racismo? (CIS 3536).
2. ¿Qué distancia hay entre algunas creencias frecuentes sobre inmigración y los registros o estadísticas oficiales? (INE, Seguridad Social, Sanidad, Interior y otras fuentes).

El propósito es poner la percepción declarada y los datos oficiales uno al lado del otro, haciendo explícitas sus diferencias de población, periodo y unidad de medida. No se pretende decir a la audiencia qué debe pensar. La distancia entre percepciones y registros constituye un objeto de análisis relevante para el debate público, las políticas y la convivencia.

### Fuente principal

CIS, Barómetro de diciembre de 2025, Estudio 3536: 4.017 entrevistas telefónicas CATI a población adulta de 18 años o más, con ponderación nacional `PESO`. Las preguntas centrales son P12_1 (autopercepción), P12_2 (percepción de la sociedad), además de P11, P10, PAISNAC, EDAD, ESCIDEOL y ESTUDIOS.

## 3. Fuentes utilizadas

| Bloque | Fuente y periodo | Indicadores recogidos en el material | Documentación indicada |
|---|---|---|---|
| Percepciones | CIS 3536, diciembre 2025 | P12_1, P12_2, P11, P10, PAISNAC, EDAD, ESCIDEOL, ESTUDIOS, PESO | Microdato, libro de códigos y tabla de faltantes tras limpieza |
| Mercado laboral | INE, EPA 1T 2026 | Actividad: 68,49% extranjeros frente a 57,21% españoles; paro: 17,23% frente a 9,5%; variación de activos: +65.800 y −4.600 | Nota de prensa del 27/04/2026 y tabla 65300 de INEbase |
| Afiliación | Seguridad Social, marzo 2026 | 3.210.759 afiliados extranjeros; 14,4% del total, dato desestacionalizado | Nota de prensa y fichero «Afiliados por nacionalidad - Extranjeros último día - 2026» |
| Sanidad | Ministerio de Sanidad, 2026 | Comparaciones de visitas a Atención Primaria, uso de medicamentos y enfermedades crónicas por origen | Informe *Estado de salud y uso del sistema sanitario por la población migrante en España* |
| Exclusión y precariedad | INE ECV/AROPE 2025; SEPE 2025 | AROPE global 25,7%; temporalidad 45,94%; parcialidad femenina 20,20%; paro extranjero 14,51% | Notas de prensa e informes/tablas oficiales |
| Delitos de odio | Ministerio del Interior, 2025 | 934 hechos por racismo/xenofobia (+16,1%); 38,6% del total registrado | Informe anual de delitos de odio |
| Contexto | Consejo Económico y Social, Informe 01/2025 | Participación 78% frente a 74%; cerca del 20% de población activa y empleo; valoración de su papel demográfico | *La realidad migratoria en España: Prioridades para las políticas públicas*, pp. 12, 15 y 32 |

**Regla de documentación visual:** cada tabla y gráfico debe incluir fuente completa, definición de la base, n sin ponderar e indicación de la ponderación usada. Las cifras de esta tabla son las transcritas en el material de partida; verificar denominadores, definiciones, fechas y tablas originales antes de presentarlas como definitivas.

## 4. Preparación y limpieza

### Selección y recodificación

De las 169 variables originales del CIS 3536 se seleccionan como dataset maestro: `REGISTRO`, `PESO`, `EDAD`, `ESCIDEOL`, `ESTUDIOS`, `PAISNAC`, `P10`, `P11`, `P12_1` y `P12_2`.

- En P12_1, P12_2 y ESCIDEOL, los códigos 98 y 99 se convierten en ausentes cuando representan NS/NC.
- En P11, los códigos 8 y 9 se tratan como NS/NC.
- Se conserva ESCIDEOL 8 y 9 como posiciones válidas de la escala, según la decisión documentada en el libro de códigos; no se confunden con NS/NC.
- Se deriva `brecha = P12_2 − P12_1` solo con ambas respuestas válidas. La base informada es n = 3.913.
- Se derivan grupos de edad (cinco tramos), ideología (izquierda 1–4, centro 5–6, derecha 7–10 y no se ubica), educación (cuatro niveles), `p11_binario` y `p10_binario`.

`PAISNAC2`, país específico de nacimiento, se descarta para comparaciones por país: el material informa unos 230 casos distribuidos en más de 30 países, con celdas de 2 a 10 casos. Se conserva `PAISNAC` como distinción agregada España/extranjero para análisis de control si resulta metodológicamente pertinente.

### Ponderación

Se utiliza `PESO` para estimaciones agregadas y contrastes y se informa el n no ponderado junto a los resultados. No se usa `PESOCCAA`, porque el análisis es nacional y no se presentan estimaciones por comunidad autónoma. La ponderación no sustituye el modelado de estratos y conglomerados del diseño muestral.

## 5. Análisis descriptivo

El plan contempla distribuciones ponderadas de la brecha, P12_1, P12_2, P11 (con denominador del total y de usuarios de redes), P10 y PAISNAC. También prevé medias de brecha por ideología, edad, educación, P10 y P11 binario, acompañadas del n válido no ponderado por celda.

Los gráficos deben mostrar medias o proporciones ponderadas con intervalos de confianza del 95% estimados con un procedimiento documentado. No presentar intervalos como basados en diseño complejo si no se incorporaron estratos y unidades primarias. En la versión actual del análisis CIS, la media ponderada de autopercepción es 1,79/10 y la media atribuida a la sociedad 5,24/10, con diferencia descriptiva de 3,45 puntos (n válido = 3.913). La memoria no debe confundir este resultado con los análisis de P10/P11 adicionales si todavía no se han reproducido.

## 6. Hipótesis y contrastación

Se indica que el nivel de significación se fijó en α = 0,05 antes de examinar p-valores y que se planteó α = 0,025 en contrastes múltiples de una misma variable dependiente mediante Bonferroni. La regla es: p < α, rechazar H0; p ≥ α, no rechazar H0. No rechazar H0 no equivale a probarla verdadera, y el p-valor no es la probabilidad de que H0 sea cierta.

| Hipótesis | Prueba indicada | Resultado transcrito | Decisión indicada |
|---|---|---|---|
| H1. Ideología → brecha | ANOVA WLS | F = 207,87; p < 0,001; η² = 0,099 | Rechazar H0 |
| H2. Edad → recuerdo de contenido en redes | Chi-cuadrado ponderada | χ² = 25,99; gl = 4; p < 0,001; V = 0,084 | Rechazar H0 |
| H3. Educación → P12_1 y brecha | ANOVA WLS | p < 0,001 | Rechazar H0 |
| H4. P10/P11 → P12_2 | Welch t ponderado | p < 0,001 en ambos | Rechazar H0 |

El material propone η² para H1/H3, V de Cramér para H2 y d de Cohen para H4; este último queda pendiente de cálculo/documentación. Los resultados previamente reproducidos en el repositorio para H1, H2, sexo e ingresos controlando ideología son: H1 F(2, 3.774) = 207,87; H2 χ²(4) = 25,99; sexo t ≈ 9,97; ingresos F(2, 3.800) = 45,02. H3/H4 y tamaños de efecto deben cotejarse con la versión actual del código antes de incorporarse como resultados confirmados.

Los contrastes ponderados disponibles son aproximaciones: el microdato plano no permite modelar completamente el diseño CATI con estratificación y conglomerados. La tabla ponderada de H2 trata sumas de pesos como frecuencias, por lo que su p-valor es indicativo. Se recomienda reportar tamaños de efecto e intervalos solo cuando su cálculo y método sean reproducibles.

## 7. Fact-checking de afirmaciones

El bloque de fact-checking organiza siete afirmaciones (M1–M7), cada una con fuente primaria, definición operacional y estado (completo, parcial, cualitativo o fuera de alcance). La afirmación «delinquen más» (M6) se excluye por limitaciones metodológicas y éticas. El material también deja el bullying fuera del análisis porque no encontró una fuente oficial que lo desagregue por origen migrante.

La conclusión de cada mito debe ser proporcional a la fuente: actividad laboral no equivale a empleo; titular del IMV no equivale a persona beneficiaria del hogar; el número de hechos registrados por Interior no mide todos los incidentes ni permite inferir propensiones por nacionalidad; los resultados sanitarios requieren revisar poblaciones, indicadores y método. El balance fiscal neto no debe afirmarse sin especificar horizonte y metodología.

## 8. Dificultades y decisiones

1. **Códigos de ideología:** se auditó el libro de códigos y se mantuvieron 8 y 9 como posiciones válidas, separándolos de NS/NC.
2. **País específico con bajo n:** se descartó `PAISNAC2` para análisis por país y se reservó la categoría agregada `PAISNAC`.
3. **Contrastes con pesos:** se declararon como aproximaciones, dado que no se modela todo el diseño complejo. Se acompañan con tamaños del efecto cuando se pueden reproducir.
4. **Comparaciones múltiples:** se plantea Bonferroni para dos pruebas sobre la misma dependiente o, en su defecto, interpretar como exploratorio.
5. **Datos ausentes del CIS:** afiliación, gasto sanitario y delitos de odio se consultan en fuentes oficiales separadas, sin fusionarlas con el microdato.
6. **Bullying:** se omite por falta de fuente oficial comparable con desglose por origen migrante.

## 9. Interpretación, límites y alcance

### Qué puede sostenerse, con cautela

- En el CIS 3536, la sociedad se sitúa por encima de la autopercepción media de racismo; la diferencia descriptiva es 3,45 puntos.
- La brecha está asociada con ideología en los contrastes reproducidos; H2 sugiere una asociación pequeña entre edad y recuerdo de exposición a contenido ofensivo o violento en redes.
- La información oficial externa permite contextualizar empleo, afiliación, sanidad, precariedad y delitos registrados si se respetan sus definiciones y periodos.

### Qué no puede sostenerse con estos datos

- Que una variable cause la brecha o la exposición a contenido.
- Que la tasa de actividad demuestre que las personas extranjeras “trabajan más”; mide participación en el mercado laboral, no empleo efectivo.
- Que la brecha demuestre quién es racista o constituya una medida objetiva del racismo social.
- Que la nacionalidad cause criminalidad, o que una estadística de hechos registrados permita esa inferencia.
- Un balance fiscal neto universal sin metodología, ámbito y horizonte temporal.

Otras limitaciones: deseabilidad social; percepción distinta del significado de “racismo”; celdas pequeñas; datos recientes sujetos a revisión; una sola oleada para el análisis principal; tests múltiples; incertidumbre no ajustada al diseño completo. Las asociaciones deben describirse como tales. La percepción declarada es un dato social válido, pero no sustituye medidas de discriminación observada o experiencias individuales.

## 10. Reproducibilidad y estructura de trabajo

El desarrollo debe organizarse con código Python reproducible. La estructura prevista es `src/main.py` para limpieza, recodificación, exploración, contrastes y gráficos; `src/data/` para datos permitidos y salidas derivadas; `src/notebooks/` para pruebas exploratorias; `src/utils/` para funciones auxiliares; y `src/main.ipynb` como recorrido resumido. El microdato del CIS no debe redistribuirse si su licencia o condiciones no lo permiten.

Entorno indicado: Python 3.x, pandas, NumPy, Matplotlib, seaborn, statsmodels y SciPy. El script debe documentar rutas, codificaciones, denominadores y variables generadas. Para que las cifras sean auditables, guardar tablas de faltantes, resultados agregados, estadísticos, grados de libertad, p-valores exactos, tamaños de efecto y notas de limitación.

## 11. Conclusión

El proyecto no resuelve el debate sobre inmigración y racismo. Aporta una forma de contrastar percepciones declaradas con indicadores oficiales y de describir la distancia entre ambas capas de evidencia. En la encuesta CIS 3536 existe una brecha marcada entre la autopercepción y la percepción atribuida a la sociedad; esa brecha varía entre perfiles analizados. Los registros externos ayudan a comprobar afirmaciones concretas, siempre que se respeten las definiciones, las poblaciones y los periodos de referencia.

El posicionamiento ético del trabajo es explícito: dar relato a una minoría habitualmente silenciada, cuestionar discursos deshumanizantes y no contribuir a la desinformación. Para sostenerlo, la práctica analítica debe buscar fuentes primarias, verificar los datos, ponderar adecuadamente, comunicar incertidumbre y no afirmar más de lo que los resultados permiten.

## Fuentes citadas

- CIS, [Estudio 3536, Barómetro de diciembre de 2025](https://www.cis.es/es/w/avance-de-resultados-del-estudio-3536-bar%C3%B3metro-de-diciembre-2025-).
- INE, EPA 1T 2026, ECV/AROPE 2025 e INEbase, tabla 65300. Consultar nota y tablas originales antes de difundir cifras.
- Seguridad Social, afiliación de extranjeros, marzo de 2026.
- Ministerio de Sanidad, *Estado de salud y uso del sistema sanitario por la población migrante en España* (2026).
- Ministerio del Interior, Informe anual de delitos de odio (2025).
- SEPE, Informe del mercado de trabajo (2025).
- Consejo Económico y Social, *La realidad migratoria en España: Prioridades para las políticas públicas*, Informe 01/2025.
