import pandas as pd
import matplotlib.pyplot as plt

def ejecutar_analisis_maestro():
    # Nombres de los archivos en la misma carpeta
    archivo_transporte = 'osb_evento_transporte.csv'
    archivo_lluvia = 'lluvia_mensual_bogota.csv'

    try:
        print("1. Cargando archivos...")
        # Carga de transporte (con separador ; y encoding latin-1)
        df_trans = pd.read_csv(archivo_transporte, sep=';', encoding='latin-1')
        # Carga de lluvia (separador , por defecto)
        df_lluvia = pd.read_csv(archivo_lluvia)

        # 2. Procesamiento de Meses (Unificar a minúsculas para el cruce)
        meses_orden = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                       'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        
        df_trans['MES_DEL_HECHO'] = df_trans['MES_DEL_HECHO'].str.lower().str.strip()
        
        # 3. Limpieza de Horas y Actores
        df_trans['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_'] = (
            df_trans['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_']
            .str.replace('(', '', regex=False).str.replace(')', '', regex=False)
            .str.replace('Sin información', 'No Disponible', case=False).str.strip()
        )

        # 4. Cálculos para la Correlación
        res_mortalidad = df_trans.groupby('MES_DEL_HECHO')['casos'].sum().reindex(meses_orden)
        
        meses_map = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio', 
                     7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
        df_lluvia['nombre_mes'] = df_lluvia['mes'].map(meses_map)
        res_lluvia = df_lluvia.groupby('nombre_mes')['precipitacion_mm'].mean().reindex(meses_orden)

        # 5. CREACIÓN DEL DASHBOARD
        print("2. Generando Dashboard...")
        fig = plt.figure(figsize=(16, 10))
        plt.subplots_adjust(hspace=0.5, wspace=0.3)
        fig.suptitle('ANÁLISIS COMBINADO: CLIMA Y SEGURIDAD VIAL EN BOGOTÁ', fontsize=20, fontweight='bold')

        # --- Gráfico 1: Lluvia vs Mortalidad (Doble Eje) ---
        ax1 = plt.subplot(2, 2, 1)
        ax1.bar(meses_orden, res_lluvia, color='skyblue', alpha=0.5, label='Lluvia (mm)')
        ax1.set_ylabel('Lluvia (mm)', color='blue', fontweight='bold')
        ax2 = ax1.twinx()
        ax2.plot(meses_orden, res_mortalidad, color='red', marker='o', linewidth=3, label='Muertes')
        ax2.set_ylabel('N° Muertes', color='red', fontweight='bold')
        ax1.set_title('Impacto de la Lluvia en Accidentes', fontsize=12)
        ax1.set_xticklabels(meses_orden, rotation=45)

        # --- Gráfico 2: Localidades ---
        ax3 = plt.subplot(2, 2, 2)
        df_loc = df_trans[df_trans['LOCALIDAD'] != 'Bogotá']
        df_loc.groupby('LOCALIDAD')['casos'].sum().sort_values().tail(10).plot(kind='barh', ax=ax3, color='#ff7f0e')
        ax3.set_title('Top 10 Localidades Críticas', fontsize=12)

        # --- Gráfico 3: Actor Vial ---
        ax4 = plt.subplot(2, 2, 3)
        df_trans.groupby('CONDICION_DE_LA_VICTIMA_AT_')['casos'].sum().plot(kind='pie', ax=ax4, autopct='%1.1f%%', colors=['#2ca02c','#d62728','#9467bd'])
        ax4.set_ylabel('')
        ax4.set_title('Distribución de Víctimas', fontsize=12)

        # --- Gráfico 4: Horarios ---
        ax5 = plt.subplot(2, 2, 4)
        df_trans.groupby('RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_')['casos'].sum().sort_values(ascending=False).head(8).plot(kind='bar', ax=ax5, color='#e377c2')
        ax5.set_title('Franjas Horarias más Peligrosas', fontsize=12)
        plt.xticks(rotation=45)

        # 6. Exportar Excel
        with pd.ExcelWriter('Informe_Final_Combinado.xlsx') as writer:
            res_mortalidad.to_excel(writer, sheet_name='Mortalidad')
            res_lluvia.to_excel(writer, sheet_name='Lluvia')

        print("\n ¡LISTO! Gráficos generados y Excel 'Informe_Final_Combinado.xlsx' guardado.")
        
        # IMPORTANTE: Esto mantiene la ventana abierta
        plt.show()

    except Exception as e:
        print(f"\n ERROR: {e}")
        print("Verifica que los nombres de los archivos coincidan exactamente.")
        input("\nPresiona Enter para cerrar...")

if __name__ == "__main__":
    ejecutar_analisis_maestro()