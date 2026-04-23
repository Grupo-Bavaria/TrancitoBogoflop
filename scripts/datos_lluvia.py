import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas as pd

def ejecutar_analisis_lluvia():
    script_dir = os.path.dirname(os.path.abspath(__file__))


    archivo = os.path.join(script_dir, 'lluvia_mensual_bogota.csv')
    df = pd.read_csv(archivo)
    df = df[(df['anio'] >= 2017) & (df['anio'] <= 2022) & (df['anio'] != 2019)]

    meses_map = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
                 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
                 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}
    meses_orden = list(meses_map.values())
    df['nombre_mes'] = df['mes'].map(meses_map)

    lluvia_mensual = df.groupby('nombre_mes')['precipitacion_mm'].mean().reindex(meses_orden)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('COMPORTAMIENTO HISTÓRICO DE LLUVIA EN BOGOTÁ (2017-2022)', fontsize=14, fontweight='bold')

    bars = axes[0].bar(meses_orden, lluvia_mensual, color='skyblue', edgecolor='navy', alpha=0.8)
    axes[0].set_title('Precipitación Promedio por Mes', fontsize=12)
    axes[0].set_ylabel('mm promedio')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y', linestyle='--', alpha=0.5)
    bars[9].set_color('orange')

    octubre_df = df[df['mes'] == 10]
    octubre_anual = octubre_df.groupby('anio')['precipitacion_mm'].mean()
    axes[1].plot(octubre_anual.index, octubre_anual.values, marker='o', color='orange', linewidth=2)
    axes[1].set_title('Precipitación en Octubre por Año (2017-2022)', fontsize=12)
    axes[1].set_ylabel('mm')
    axes[1].set_xlabel('Año')
    axes[1].set_xticks(octubre_anual.index)
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('outputs/datos_lluvia.png', bbox_inches='tight', dpi=150)

if __name__ == "__main__":
    ejecutar_analisis_lluvia()
