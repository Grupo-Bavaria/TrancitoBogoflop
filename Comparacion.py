import pandas as pd
import matplotlib.pyplot as plt

def ejecutar_analisis_maestro():
    archivo_transporte = 'osb_evento_transporte.csv'
    archivo_lluvia = 'lluvia_mensual_bogota.csv'

    try:
        print("1. Cargando archivos...")
        df_trans = pd.read_csv(archivo_transporte, sep=';', encoding='latin-1')
        df_lluvia = pd.read_csv(archivo_lluvia)

        # --- Procesamiento ---
        meses_orden = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                       'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        meses_map = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio',
                     7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}

        # Mortalidad
        df_trans['MES_DEL_HECHO'] = df_trans['MES_DEL_HECHO'].str.lower().str.strip()
        df_trans['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_'] = (
            df_trans['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_']
            .str.replace('(', '', regex=False).str.replace(')', '', regex=False)
            .str.replace('Sin información', 'No Disponible', case=False).str.strip()
        )
        res_mortalidad = df_trans.groupby('MES_DEL_HECHO')['casos'].sum().reindex(meses_orden)

        # Lluvia: promedio histórico por mes
        df_lluvia['nombre_mes'] = df_lluvia['mes'].map(meses_map)
        res_lluvia = df_lluvia.groupby('nombre_mes')['precipitacion_mm'].mean().reindex(meses_orden)

        # --- Dashboard ---
        print("2. Generando Dashboard...")
        fig = plt.figure(figsize=(16, 10))
        plt.subplots_adjust(hspace=0.5, wspace=0.3)
        fig.suptitle('ANÁLISIS COMBINADO: CLIMA Y SEGURIDAD VIAL EN BOGOTÁ',
                     fontsize=18, fontweight='bold')

        # --- Gráfico 1: Lluvia vs Mortalidad (doble eje) ---
        ax1 = plt.subplot(2, 2, 1)
        bars = ax1.bar(range(len(meses_orden)), res_lluvia, color='skyblue', alpha=0.6, label='Lluvia (mm)')
        # Resaltar octubre en naranja
        bars[9].set_color('orange')
        ax1.set_xticks(range(len(meses_orden)))
        ax1.set_xticklabels(meses_orden, rotation=45, ha='right')
        ax1.set_ylabel('Lluvia promedio (mm)', color='steelblue', fontweight='bold')
        ax1.tick_params(axis='y', labelcolor='steelblue')

        ax2 = ax1.twinx()
        ax2.plot(range(len(meses_orden)), res_mortalidad, color='red',
                 marker='o', linewidth=3, label='Muertes')
        ax2.set_ylabel('N° Muertes', color='red', fontweight='bold')
        ax2.tick_params(axis='y', labelcolor='red')
        ax1.set_title('Lluvia vs Mortalidad por Mes', fontsize=12)

        # Leyenda combinada
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

        # --- Gráfico 2: Top 10 Localidades ---
        ax3 = plt.subplot(2, 2, 2)
        df_loc = df_trans[~df_trans['LOCALIDAD'].isin(['Bogotá', 'Sin información', 'SIN INFORMACION'])]
        df_loc.groupby('LOCALIDAD')['casos'].sum().sort_values().tail(10).plot(
            kind='barh', ax=ax3, color='#ff7f0e')
        ax3.set_title('Top 10 Localidades Críticas', fontsize=12)
        ax3.set_xlabel('Número de casos')

        # --- Gráfico 3: Actor Vial (paleta automática) ---
        ax4 = plt.subplot(2, 2, 3)
        res_actor = df_trans.groupby('CONDICION_DE_LA_VICTIMA_AT_')['casos'].sum().sort_values(ascending=False)
        colores = plt.cm.tab10.colors[:len(res_actor)]
        res_actor.plot(kind='pie', ax=ax4, autopct='%1.1f%%',
                       startangle=140, colors=colores)
        ax4.set_ylabel('')
        ax4.set_title('Distribución por Actor Vial', fontsize=12)

        # --- Gráfico 4: Franjas Horarias ---
        ax5 = plt.subplot(2, 2, 4)
        res_hora = (df_trans[df_trans['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_'] != 'No Disponible']
                    .groupby('RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_')['casos'].sum()
                    .sort_values(ascending=False).head(8))
        res_hora.plot(kind='bar', ax=ax5, color='#e377c2')
        ax5.set_title('Franjas Horarias más Peligrosas (Top 8)', fontsize=12)
        ax5.tick_params(axis='x', rotation=45)
        ax5.set_xlabel('')

        # --- Exportar Excel ---
        with pd.ExcelWriter('Informe_Final_Combinado.xlsx') as writer:
            res_mortalidad.to_excel(writer, sheet_name='Mortalidad_por_Mes')
            res_lluvia.to_excel(writer, sheet_name='Lluvia_por_Mes')
            df_loc.groupby('LOCALIDAD')['casos'].sum().sort_values(ascending=False).to_excel(
                writer, sheet_name='Localidades')
            res_actor.to_excel(writer, sheet_name='Actor_Vial')

        plt.savefig('dashboard_maestro.png', bbox_inches='tight', dpi=150)
        print("\n¡LISTO! Guardados: 'dashboard_maestro.png' e 'Informe_Final_Combinado.xlsx'")
        plt.show()

    except Exception as e:
        print(f"\nERROR: {e}")
        print("Verifica que los archivos estén en la misma carpeta que este script.")
        input("\nPresiona Enter para cerrar...")

if __name__ == "__main__":
    ejecutar_analisis_maestro()