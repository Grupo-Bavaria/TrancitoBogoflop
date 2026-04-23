import pandas as pd
import matplotlib.pyplot as plt

def ejecutar_analisis_lluvia():
    archivo = 'lluvia_mensual_bogota.csv'

    try:
        print("Cargando datos de lluvia...")
        df = pd.read_csv(archivo)

        # El archivo tiene columnas: mes_anio, precipitacion_mm, num_registros, anio, mes
        meses_map = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
                     5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
                     9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}
        meses_orden = list(meses_map.values())

        df['nombre_mes'] = df['mes'].map(meses_map)

        # Promedio histórico de lluvia por mes (2017-2023)
        lluvia_mensual = df.groupby('nombre_mes')['precipitacion_mm'].mean().reindex(meses_orden)

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('COMPORTAMIENTO HISTÓRICO DE LLUVIA EN BOGOTÁ (2017-2023)',
                     fontsize=14, fontweight='bold')

        # --- Gráfico 1: Promedio mensual histórico ---
        axes[0].bar(meses_orden, lluvia_mensual, color='skyblue', edgecolor='navy', alpha=0.8)
        axes[0].set_title('Precipitación Promedio por Mes', fontsize=12)
        axes[0].set_ylabel('mm promedio')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(axis='y', linestyle='--', alpha=0.5)
        # Resaltar octubre
        axes[0].get_children()[9].set_color('orange')  # índice 9 = octubre

        # --- Gráfico 2: Evolución anual de octubre (para mostrar variabilidad) ---
        octubre_anual = df[df['mes'] == 10].groupby('anio')['precipitacion_mm'].mean()
        axes[1].plot(octubre_anual.index, octubre_anual.values,
                     marker='o', color='orange', linewidth=2)
        axes[1].set_title('Precipitación en Octubre por Año', fontsize=12)
        axes[1].set_ylabel('mm')
        axes[1].set_xlabel('Año')
        axes[1].grid(True, linestyle='--', alpha=0.5)

        print("Generando gráfico de lluvias...")
        plt.tight_layout()
        plt.savefig('dashboard_lluvia.png', bbox_inches='tight', dpi=150)
        print("Guardado como 'dashboard_lluvia.png'")
        plt.show()

    except Exception as e:
        print(f"Error: {e}")
        print(f"Verifica que '{archivo}' esté en la misma carpeta que este script.")

if __name__ == "__main__":
    ejecutar_analisis_lluvia()