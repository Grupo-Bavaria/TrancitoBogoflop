import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas as pd

def ejecutar_analisis_mortalidad():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    archivo = os.path.join(script_dir, 'osb_evento_transporte.csv')
    df = pd.read_csv(archivo, sep=';', encoding='latin-1')
    df = df[(df['ANO'] >= 2017) & (df['ANO'] <= 2022) & (df['ANO'] != 2019)]

    df['MES_DEL_HECHO'] = df['MES_DEL_HECHO'].str.lower().str.strip()
    df['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_'] = (
        df['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_']
        .str.replace('(', '', regex=False)
        .str.replace(')', '', regex=False)
        .str.replace('Sin información', 'No Disponible', case=False)
        .str.strip()
    )

    meses_orden = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                   'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    fig.suptitle('ESTADÍSTICAS DE MORTALIDAD VIAL EN BOGOTÁ (2017-2022)', fontsize=18, fontweight='bold')

    res_mes = df.groupby('MES_DEL_HECHO')['casos'].sum().reindex(meses_orden)
    res_mes.plot(kind='line', marker='o', ax=axes[0, 0], color='#1f77b4', linewidth=3)
    axes[0, 0].set_title('Mortalidad por Mes (2017-2022)', fontsize=12)
    axes[0, 0].set_xlabel('')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, linestyle='--', alpha=0.6)

    df_loc = df[~df['LOCALIDAD'].isin(['Bogotá', 'Sin información', 'SIN INFORMACION'])]
    res_loc = df_loc.groupby('LOCALIDAD')['casos'].sum().sort_values().tail(10)
    res_loc.plot(kind='barh', ax=axes[0, 1], color='#ff7f0e')
    axes[0, 1].set_title('Top 10 Localidades con Mayor Mortalidad', fontsize=12)
    axes[0, 1].set_xlabel('Número de casos')

    res_actor = df.groupby('CONDICION_DE_LA_VICTIMA_AT_')['casos'].sum().sort_values(ascending=False)
    colores = plt.cm.tab10.colors[:len(res_actor)]
    res_actor.plot(kind='pie', ax=axes[1, 0], autopct='%1.1f%%', startangle=140, colors=colores)
    axes[1, 0].set_ylabel('')
    axes[1, 0].set_title('Distribución por Actor Vial', fontsize=12)

    res_hora = (df[df['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_'] != 'No Disponible']
                .groupby('RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_')['casos'].sum()
                .sort_values(ascending=False).head(8))
    res_hora.plot(kind='bar', ax=axes[1, 1], color='#e377c2')
    axes[1, 1].set_title('Franjas Horarias más Peligrosas (Top 8)', fontsize=12)
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].set_xlabel('')

    plt.savefig('outputs/tasa_mortalidad.png', bbox_inches='tight', dpi=150)

if __name__ == "__main__":
    ejecutar_analisis_mortalidad()
