import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def ejecutar_correlacion():
    archivo_transporte = 'osb_evento_transporte.csv'
    archivo_lluvia     = 'lluvia_mensual_bogota.csv'

    df_trans  = pd.read_csv(archivo_transporte, sep=';', encoding='latin-1')
    df_lluvia = pd.read_csv(archivo_lluvia)

    df_trans  = df_trans[(df_trans['ANO'] >= 2017) & (df_trans['ANO'] <= 2022) & (df_trans['ANO'] != 2019)]
    df_lluvia = df_lluvia[(df_lluvia['anio'] >= 2017) & (df_lluvia['anio'] <= 2022) & (df_lluvia['anio'] != 2019)]

    meses_map = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio',
                 7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
    meses_orden = list(meses_map.values())

    df_trans['MES_DEL_HECHO'] = df_trans['MES_DEL_HECHO'].str.lower().str.strip()
    df_lluvia['nombre_mes']   = df_lluvia['mes'].map(meses_map)

    muertes = df_trans.groupby('MES_DEL_HECHO')['casos'].sum().reindex(meses_orden)
    lluvia  = df_lluvia.groupby('nombre_mes')['precipitacion_mm'].mean().reindex(meses_orden)

    x = lluvia.values
    y = muertes.values

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r2 = r_value ** 2

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('CORRELACIÓN: PRECIPITACIONES vs MORTALIDAD VIAL EN BOGOTÁ (2017-2022)', fontsize=14, fontweight='bold')

    ax = axes[0]
    ax.scatter(x, y, color='steelblue', s=100, zorder=5, label='Meses')
    for i, mes in enumerate(meses_orden):
        ax.annotate(mes[:3], (x[i], y[i]), textcoords="offset points", xytext=(6, 4), fontsize=8, color='gray')
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, color='red', linewidth=2, label=f'y = {slope:.2f}x + {intercept:.1f}')
    ax.set_xlabel('Precipitación promedio (mm)', fontsize=11)
    ax.set_ylabel('N° Muertes (total 2017-2022)', fontsize=11)
    ax.set_title(f'Dispersión y Regresión Lineal\nr = {r_value:.3f} | R² = {r2:.3f} | p = {p_value:.3f}', fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.5)

    ax2 = axes[1]
    lluvia_norm  = (lluvia  - lluvia.min())  / (lluvia.max()  - lluvia.min())
    muertes_norm = (muertes - muertes.min()) / (muertes.max() - muertes.min())
    ax2.plot(range(12), lluvia_norm,  marker='o', color='steelblue', linewidth=2, label='Lluvia (normalizada)')
    ax2.plot(range(12), muertes_norm, marker='s', color='red',       linewidth=2, label='Muertes (normalizada)')
    ax2.set_xticks(range(12))
    ax2.set_xticklabels([m[:3] for m in meses_orden], rotation=45)
    ax2.set_ylabel('Valor normalizado (0-1)', fontsize=11)
    ax2.set_title('Comparación de Tendencias por Mes', fontsize=11)
    ax2.legend(fontsize=9)
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('correlacion_lluvia_muertes.png', bbox_inches='tight', dpi=150)

if __name__ == "__main__":
    ejecutar_correlacion()
