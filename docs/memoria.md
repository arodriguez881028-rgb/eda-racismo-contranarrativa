# Memoria · EDA Racismo y contranarrativa

## 1. Problema y objetivo

El proyecto pregunta si existe una distancia entre la percepción que las personas tienen de su propio racismo y la que atribuyen a la sociedad española. El punto de partida es que las narrativas de odio pueden dominar la discusión pública y hacer que las respuestas se formulen dentro de un marco estigmatizante. El objetivo analítico es comprobar una hipótesis descriptiva con datos de encuesta y comunicar sus límites.

**Hipótesis:** la puntuación media que cada persona atribuye a la sociedad será superior a la puntuación que se atribuye a sí misma. Se explora además si la brecha aparece en perfiles sociodemográficos e ideológicos.

## 2. Datos y variables

Se usa el estudio CIS 3536, Barómetro de diciembre de 2025: 4.017 entrevistas a población de 18 o más años residente en España, realizadas por teléfono entre el 1 y el 5 de diciembre de 2025. La ficha técnica describe muestreo por cuotas con selección aleatoria de teléfonos y recomienda aplicar el coeficiente `PESO` al estimar el conjunto de la muestra.

Las variables centrales son `P12_1` (autoubicación en escala 0–10), `P12_2` (ubicación atribuida a la sociedad española), `PESO`, sexo, edad, ingresos netos del hogar, estudios y autoubicación ideológica. `N.S.` y `N.C.` se excluyen de los promedios. Para la ideología se forman tres tramos (1–4, 5–6 y 7–10); para ingresos, tres tramos (hasta 1.800 €, 1.801–3.900 € y más de 3.900 €); y estudios se agrupa en cuatro categorías CIS.

## 3. Preparación y análisis

El script lee el CSV etiquetado del CIS, convierte las respuestas de escala a valores numéricos, convierte el peso con coma decimal y calcula medias ponderadas para ambas preguntas. Los gráficos comparan esos promedios con barras agrupadas. Se guarda una tabla de medias y tamaño de muestra válido por categoría, además de gráficos SVG reutilizables en la presentación.

La presentación también incluye dos gráficas históricas aportadas para el proyecto y atribuidas al Barómetro mensual del CIS (2015–2025). Son referencias de contexto, no se vuelven a estimar ni digitalizar aquí: el microdato 3536 es una sola oleada y no contiene la serie mensual.

## 4. Resultados

La media ponderada de autopercepción es **1,79/10** y la media atribuida a la sociedad es **5,24/10**. La diferencia es **3,45 puntos**, en 3.913 casos con respuesta válida en ambas preguntas. La hipótesis se cumple en sentido descriptivo.

La brecha por sexo es de 2,96 puntos entre hombres y 3,92 entre mujeres. Por edades, oscila aproximadamente entre 3,17 y 3,84. En los bloques ideológicos, es mayor en la izquierda (4,35) y menor en la derecha (2,02), donde la autopercepción media es más alta. La sociedad se valora entre 4,76 y 5,78 según el bloque. Por ingresos y estudios también se mantiene la dirección de la brecha.

## 5. Interpretación y límites

El hallazgo es una brecha de percepción declarada: las personas sitúan a la sociedad por encima de sí mismas en una escala subjetiva. No demuestra que una persona concreta sea racista, ni estima la incidencia real de discriminación, ni explica por qué se produce la diferencia. Puede intervenir deseabilidad social, interpretación de la escala o distintas ideas sobre qué significa racismo.

Se contrasta H0: diferencia media ponderada P12_2–P12_1 = 0 mediante un Wald aproximado con tamaño efectivo de Kish: z = 49,01; p < 0,001; IC95% aproximado [3,31; 3,59]. La prueba respalda que la brecha media es mayor que cero, pero no incorpora estratos/PSU ni estima la varianza compleja del diseño CIS. Por tanto, no debe leerse como una prueba de diferencias entre perfiles ni como inferencia de causalidad. Los tamaños varían; el grupo de estudios primarios o menos tiene 131 casos válidos. La aproximación de contraste no corrige el diseño complejo y no se presentan pruebas de significación entre subgrupos. La ficha técnica ofrece un error de ±1,6 puntos porcentuales para el conjunto bajo el supuesto de muestreo aleatorio simple, pero no equivale a una estimación de incertidumbre para cada promedio ponderado o subgrupo.

Las cifras sobre EPA, sanidad e IMV de la última diapositiva son fuentes externas, con unidades y fechas propias. No se mezclan con los microdatos CIS. Deben citarse con su periodo de referencia y no interpretarse como evidencia causal.

## 6. Conclusión

La autopercepción es claramente menor que la percepción de la sociedad en esta encuesta. El patrón se repite en los perfiles examinados, aunque la magnitud varía. La conclusión responsable es limitada: existe una distancia entre la imagen individual y la colectiva en las respuestas del CIS 3536. Para evaluar actitudes, prácticas o cambios temporales harían falta indicadores adicionales y varias oleadas comparables.

## 7. Fuentes y herramientas

- Centro de Investigaciones Sociológicas, estudio 3536, Barómetro de diciembre de 2025: microdatos etiquetados, cuestionario y ficha técnica.
- Encuesta de Población Activa (INE), informe sanitario del Ministerio de Sanidad y estadísticas del Ingreso Mínimo Vital de la Seguridad Social: fuentes independientes citadas en la diapositiva final.
- Python, pandas, NumPy, Matplotlib, Jupyter, HTML, CSS y JavaScript.
