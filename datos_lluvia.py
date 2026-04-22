import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar datos de lluvia (este usa coma como separador normalmente)
df_lluvia = pd.read_csv('lluvia_mensual_bogota.csv')

# 2. Limpieza de Lluvia: Agrupar por mes para tener un promedio histórico
# Tu archivo tiene datos por año/mes, saquemos el promedio por mes del año
meses_map = {
    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 
    5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 
    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
}
df_lluvia['nombre_mes'] = df_lluvia['mes'].map(meses_map)

# Promedio de lluvia por mes (histórico)
lluvia_mensual = df_lluvia.groupby('nombre_mes')['precipitacion_mm'].mean().reindex(meses_map.values())

# 3. Traer los datos de mortalidad que ya tenías (ejemplo basado en el anterior)
# Asumiendo que res_mes es lo que calculamos antes:
# res_mes = df_mortalidad.groupby('MES_DEL_HECHO')['casos'].sum().reindex(meses_map.values())

# 4. Graficar la Correlación
fig, ax1 = plt.subplots(figsize=(12, 6))

# Eje 1: Barras para la Lluvia
ax1.bar(lluvia_mensual.index, lluvia_mensual, color='skyblue', alpha=0.6, label='Precipitación (mm)')
ax1.set_xlabel('Mes')
ax1.set_ylabel('Lluvia Promedio (mm)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Eje 2: Línea para la Mortalidad (Crea un segundo eje Y)
ax2 = ax1.twinx()
# Nota: Aquí deberías pasar tu serie de 'res_mes' de mortalidad
# ax2.plot(res_mes.index, res_mes, color='red', marker='o', linewidth=2, label='Mortalidad')
ax2.set_ylabel('Casos de Mortalidad', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title('¿Afecta la lluvia a la mortalidad vial en Bogotá?', fontsize=15)
ax1.legend(loc='upper left')
# ax2.legend(loc='upper right')

plt.show()