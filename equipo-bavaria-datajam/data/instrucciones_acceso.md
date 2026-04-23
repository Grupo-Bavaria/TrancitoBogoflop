# Instrucciones de acceso a los datasets

## 1. Siniestros viales - Secretaría de Movilidad (SDM)
- *Fuente*: Portal de Datos Abiertos de Bogotá
- *Enlace*: https://datosabiertos.bogota.gov.co/dataset/mortalidad-por-accidentes-de-transito
- *Dataset usado*: osb_evento_transporte.csv
- *Fecha de descarga*: Abril 2026
- *Periodo cubierto*: 2015-2025
- *Notas*: 
  - Los datos están consolidados por evento; no incluyen georreferenciación detallada pública
  - Para replicar el análisis, agrupa por localidad + mes

## 2. Precipitación - IDEAM
- *Fuente*: Sistema de Consulta de Datos Meteorológicos IDEAM
- *Enlace*: https://www.ideam.gov.co/nuestra-entidad/meteorologia/informes?page=1
- *Dataset usado*: Normales_climatológicas_estándar_periodo_1991-2020
- *Fecha de descarga*: Abril 2026
- *Notas*:
  - Se usó como referencia, pues los datos son acumulados muy grandes

## 2. Precipitaciones - Ambiente y desarrollo sostenible
* *Fuente*: Sistema de Consulta de precipitación de datos colombia
* *Enlace*: https://www.datos.gov.co/Ambiente-y-Desarrollo-Sostenible/Precipitaciones/ksew-j3zj
* *Dataset usado*: Lluvia_mensual_bogota.csv
* *Fecha de descarga*: Abril 2026
* *Datos incluidos*:  Filtrados por Cundinamarca y Bogotá
* *Notas*:
  - Se utilizó el API, puesto que el archivo es demasiado grande

## 3. Datos procesados (outputs intermedios)
Los archivos ya limpios y listos para el análisis están incluidos en este repositorio:
- /data/datasets.csv → Tabla maestra con cruce temporal mensual
- /data/lluvia_mensual_bogota.csv → Precipitación agregada por mes
- /data/osb_evento_transporte.csv → Siniestros filtrados y agregados por localidad/mes
