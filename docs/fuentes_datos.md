# Fuentes de datos

## Microdatos analizados

- **Estudio:** CIS 3536, Barómetro de diciembre de 2025.
- **Universo y campo:** población española de 18 años o más; entrevistas telefónicas del 1 al 5 de diciembre de 2025.
- **Muestra:** 4.017 entrevistas realizadas.
- **Fichero de trabajo:** `src/data/raw/3536_etiq.csv`, distribuido por el CIS dentro del paquete de microdatos; la versión etiquetada conserva descripciones de respuesta. El fichero contiene datos anonimizados.
- **Variables usadas:** P12_1, P12_2, PESO, SEXO, EDAD, INGRESHOG, ESCIDEOL y ESTUDIOS.
- **Documentación local:** `Ficha_Tecnica_CIS_3536.pdf`.
- **Ficha pública:** https://www.cis.es/documents/20117/13695327/FT3536.pdf/d4b82017-c271-d011-6f8d-012d68f7d8bd?t=1770303151042&version=1.0
- **Página del estudio:** https://www.cis.es/es/w/avance-de-resultados-del-estudio-3536-bar%C3%B3metro-de-diciembre-de-2025-

Los gráficos históricos que aparecen en la presentación se aportaron como imágenes y se atribuyen al Barómetro mensual del CIS (2015–2025). No se digitalizaron ni recalcularon a partir de microdatos.

## Fuentes complementarias de contexto (no fusionadas con CIS 3536)

- INE, EPA 3T 2026: https://www.ine.es/dyngs/Prensa/EPA3T26.htm
- Ministerio de Sanidad, estado de salud y uso sanitario por población migrante: https://www.sanidad.gob.es/gabinete/notasPrensa.do?id=6924
- Seguridad Social, dosier del IMV de mayo de 2026, tabla de sexo y nacionalidad de titulares: https://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/cbe2fda1-3ac7-4bc8-a5ec-06c178839e11/0e716715-d290-4745-a74a-28cc1c3bc9ea/e221487c-d047-45cb-b862-8615b69f3ad4
- **Documento local añadido:** `202601_IMV_Altas_acumuladas.xlsx`, publicado por la Seguridad Social. Resume altas iniciales de prestaciones que han figurado en nómina entre junio de 2020 y enero de 2026, desglosadas por comunidad/provincia, expedientes aprobados, sexo y composición de hogares.

El Excel de altas acumuladas **no incluye nacionalidad**. No es la fuente que permite calcular el 17,5% de titulares extranjeros; esa cifra se refiere a la nómina de mayo de 2026 y procede de la tabla de nacionalidad del dosier mensual de la Seguridad Social. Titulares, expedientes y personas beneficiarias son unidades distintas. La proporción extranjera cambia con el mes de referencia.

El informe de Sanidad de 2026 compara población por lugar de nacimiento y regiones de origen: señala hasta 65% más personas con tres o más problemas crónicos en población nacida en España, y un consumo de medicamentos 62,7% superior al de población procedente de África y casi 50% superior al de población latinoamericana. Son indicadores concretos del informe, no una medida exhaustiva de presión asistencial.

Cada cifra externa mantiene su periodo de referencia y su unidad de análisis. La tasa de actividad no es la tasa de empleo; titulares de IMV no equivale a personas beneficiarias del hogar.
