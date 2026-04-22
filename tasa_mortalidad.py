import pandas as pd
import matplotlib.pyplot as plt

def ejecutar_analisis_mortalidad():
    # Nombre del archivo en la misma carpeta
    archivo = 'osb_evento_transporte.csv'

    try:
        print("Cargando datos de transporte...")
        # 1. Carga de datos
        df = pd.read_csv(archivo, sep=';', encoding='latin-1')

        # 2. Limpieza de Datos
        # Meses a minúsculas para ordenar correctamente
        df['MES_DEL_HECHO'] = df['MES_DEL_HECHO'].str.lower().str.strip()
        
        # Limpiar franjas horarias (quitar paréntesis)
        df['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_'] = (
            df['RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_']
            .str.replace('(', '', regex=False).str.replace(')', '', regex=False)
            .str.replace('Sin información', 'No Disponible', case=False)
            .str.strip()
        )

        # 3. Preparación de Gráficos
        meses_orden = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                       'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        plt.subplots_adjust(hspace=0.4, wspace=0.3)
        fig.suptitle('ESTADÍSTICAS DE MORTALIDAD VIAL EN BOGOTÁ', fontsize=20, fontweight='bold')

        # --- Gráfico 1: Tendencia Mensual ---
        res_mes = df.groupby('MES_DEL_HECHO')['casos'].sum().reindex(meses_orden)
        res_mes.plot(kind='line', marker='o', ax=axes[0, 0], color='#1f77b4', linewidth=3)
        axes[0, 0].set_title('Mortalidad por Mes (Tendencia)', fontsize=14)
        axes[0, 0].grid(True, linestyle='--', alpha=0.6)

        # --- Gráfico 2: Top Localidades (Excluyendo "Bogotá") ---
        df_loc = df[df['LOCALIDAD'] != 'Bogotá']
        res_loc = df_loc.groupby('LOCALIDAD')['casos'].sum().sort_values().tail(10)
        res_loc.plot(kind='barh', ax=axes[0, 1], color='#ff7f0e')
        axes[0, 1].set_title('Top 10 Localidades Críticas', fontsize=14)

        # --- Gráfico 3: Actor Vial ---
        res_actor = df.groupby('CONDICION_DE_LA_VICTIMA_AT_')['casos'].sum().sort_values(ascending=False)
        res_actor.plot(kind='pie', ax=axes[1, 0], autopct='%1.1f%%', startangle=140, colors=['#2ca02c', '#d62728', '#9467bd', '#8c564b'])
        axes[1, 0].set_ylabel('')
        axes[1, 0].set_title('Distribución por Actor Vial', fontsize=14)

        # --- Gráfico 4: Franjas Horarias ---
        res_hora = df.groupby('RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_')['casos'].sum().sort_values(ascending=False).head(8)
        res_hora.plot(kind='bar', ax=axes[1, 1], color='#e377c2')
        axes[1, 1].set_title('Horarios más Peligrosos (Top 8)', fontsize=14)
        plt.xticks(rotation=45)

        print(" Generando Dashboard de Mortalidad...")
        
        # Muestra la ventana con los gráficos
        plt.show()

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Asegúrate de que el archivo '{archivo}' esté en la misma carpeta que este script.")

if __name__ == "__main__":
    ejecutar_analisis_mortalidad()