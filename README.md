# Equipo Bavaria - Bogotá DataJam 2026

## Problema abordado
Análisis de patrones temporales de mortalidad vial en Bogotá (2015-2025) y su posible asociación descriptiva con periodos de precipitación. El objetivo es identificar picos estacionales y territoriales para priorizar intervenciones preventivas.

## Fuentes de datos
1. **SDM - Secretaría de Movilidad**: Registro de siniestros viales graves (agregado por localidad y fecha)
2. **IDEAM**: Datos de precipitación por estación meteorológica en Bogotá
3. **Datos Colombia** Datos de precipitación manejable con API

## Metodología
- **Agregación temporal**: Datos de mortalidad consolidados por mes para cruce con precipitación mensual
- **Integración espacial**: Asignación de la estación IDEAM más cercana a cada localidad como proxy de lluvia
- **Análisis exploratorio**: Identificación de patrones por mes, día de semana y franja horaria
- **Visualización**: Gráficos comparativos de series temporales y distribución por localidad

## Hallazgos clave
- Octubre registra el mayor número de casos (1,180), seguido por diciembre
- Desde 2022, los sábados concentran la mayor frecuencia de siniestros graves
- La franja 6pm-12am presenta mayor tasa de mortalidad
- Causas principales: "Desobedecer señales de tránsito" y "Exceso de velocidad"
- **Nota**: La asociación lluvia-mortalidad es descriptiva; la granularidad de los datos no permite validar causalidad

## Documentación extendida
 [**Wiki del proyecto**](https://github.com/Grupo-Bavaria/TrancitoBogoflop/wiki)
Incluye: presentación equipo, roles del equipo y bitácora de exploración.

## Ejecución del análisis
```bash
# 1. Clonar repositorio
git clone [URL]

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar scripts en orden
python scripts/tasa_mortalidad.py
python scripts/datos_lluvia.py
python scripts/Comparacion.py

# 4. Revisar resultados en /outputs
