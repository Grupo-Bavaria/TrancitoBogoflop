import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="DataJam 2026", layout="wide")

# CSS personalizado para mejorar la elegancia
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #31333f; }
    div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL INTERACTIVA
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.title("Panel de Control")
    st.markdown("Filtre los datos para profundizar en el análisis.")
    
    # Filtro dinámico por año
    years = [2017, 2018, 2020, 2021, 2022]
    selected_years = st.multiselect("Seleccione los Años:", years, default=years)
    
    st.info(" Consejo: Pase el mouse sobre los gráficos para ver detalles específicos.")

# 3. CARGA Y FILTRADO
@st.cache_data # Esto hace que la página cargue instantáneamente al filtrar
def cargar_y_filtrar(años):
    df_t = pd.read_csv('osb_evento_transporte.csv', sep=';', encoding='latin-1')
    df_l = pd.read_csv('lluvia_mensual_bogota.csv')
    
    df_t.columns = df_t.columns.str.strip().str.upper()
    df_l.columns = df_l.columns.str.strip().str.upper()

    df_filt = df_t[df_t['ANO'].isin(años)].copy()
    df_l_filt = df_l[df_l['ANIO'].isin(años)].copy()

    meses_map = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio',
                 7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
    meses_orden = list(meses_map.values())

    df_filt['MES_DEL_HECHO'] = df_filt['MES_DEL_HECHO'].astype(str).str.lower().str.strip()
    df_l_filt['NOMBRE_MES'] = df_l_filt['MES'].map(meses_map)

    muertes = df_filt.groupby('MES_DEL_HECHO')['CASOS'].sum().reindex(meses_orden)
    lluvia  = df_l_filt.groupby('NOMBRE_MES')['PRECIPITACION_MM'].mean().reindex(meses_orden)
    
    return df_filt, meses_orden, lluvia, muertes

try:
    df_full, meses, lluvia, muertes = cargar_y_filtrar(selected_years)

    # TITULO ELEGANTE
    st.title(' Observatorio de Movilidad y Clima')
    st.subheader(f"Análisis correspondiente a los años: {', '.join(map(str, selected_years))}")
    
    # 4. MÉTRICAS EN "CARDS"
    r_val = stats.linregress(lluvia.values, muertes.values)[2]
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Correlación (r)", f"{r_val:.3f}")
    with c2: st.metric("Impacto Clima (R²)", f"{r_val**2:.1%}")
    with c3: st.metric("Total Muertes", f"{int(muertes.sum())}")
    with c4: st.metric("Mes más crítico", muertes.idxmax().capitalize())

    st.markdown("---")

    # 5. GRÁFICOS CON TABS (Pestañas para elegancia)
    tab1, tab2 = st.tabs([" Relación Clima-Mortalidad", " Perfil de Siniestralidad"])

    with tab1:
        col_left, col_right = st.columns(2)
        with col_left:
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(x=meses, y=lluvia, name="Lluvia (mm)", marker_color='#3498DB', opacity=0.6))
            fig1.add_trace(go.Scatter(x=meses, y=muertes, name="Muertes", line=dict(color='#E74C3C', width=4), yaxis="y2"))
            fig1.update_layout(title="Lluvia vs Mortalidad", yaxis2=dict(overlaying="y", side="right"), template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_right:
            l_n = (lluvia - lluvia.min())/(lluvia.max() - lluvia.min())
            m_n = (muertes - muertes.min())/(muertes.max() - muertes.min())
            fig2 = px.line(x=meses, y=[l_n, m_n], labels={'value':'Escala 0-1', 'x':'Mes'}, title="Sincronía de Tendencias")
            fig2.update_layout(template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        col_left, col_right = st.columns(2)
        with col_left:
            # Localidades (Limpieza integrada)
            excluir = ['BOGOTA', 'BOGOTÁ', 'SDP', 'SIN INFORMACION']
            df_loc = df_full[~df_full['LOCALIDAD'].str.upper().isin(excluir)]
            top_loc = df_loc.groupby('LOCALIDAD')['CASOS'].sum().sort_values().tail(10)
            st.plotly_chart(px.bar(top_loc, orientation='h', title="Top 10 Localidades", color_discrete_sequence=['#F39C12'], template="plotly_dark"), use_container_width=True)
            
        with col_right:
            # Actor Vial
            col_act = 'CONDICION_DE_LA_VICTIMA_AT_'
            dist = df_full.groupby(col_act)['CASOS'].sum()
            st.plotly_chart(px.pie(values=dist, names=dist.index, hole=.4, title="Víctimas por Actor Vial", template="plotly_dark"), use_container_width=True)

    # FRANJAS HORARIAS (EJES PERSONALIZADOS)
    st.markdown("---")
    st.subheader(" Franjas Horarias de Mayor Riesgo")
    col_h = 'RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_'
    
    if col_h in df_full.columns:
        df_h = df_full.copy()
        # Limpieza de paréntesis y espacios
        df_h[col_h] = df_h[col_h].astype(str).str.replace(r'[\(\)]', '', regex=True).str.strip()
        # Filtro de "Sin Información"
        df_h = df_h[~df_h[col_h].str.upper().str.contains('SIN INFO')]
        
        # Agrupación
        dist_h = df_h.groupby(col_h)['CASOS'].sum().sort_values(ascending=False).head(8)
        
        # Creación del gráfico con etiquetas personalizadas
        fig_hora = px.bar(
            x=dist_h.index, 
            y=dist_h.values, 
            color=dist_h.values, 
            color_continuous_scale='Reds', # Cambiado a escala de rojos para indicar peligro
            labels={
                'x': 'Horas',      # Cambio de etiqueta Eje X
                'y': 'Muertes',    # Cambio de etiqueta Eje Y
                'color': 'Total'   # Etiqueta de la leyenda de color
            },
            template="plotly_dark"
        )
        
        # Ajustes estéticos finales
        fig_hora.update_layout(
            xaxis_tickangle=-45,
            coloraxis_showscale=False # Ocultamos la barra de color para más limpieza
        )
        
        st.plotly_chart(fig_hora, use_container_width=True)
    else:
        st.warning(f"No se encontró la columna de horario especificada: {col_h}")

except Exception as e:
    st.error(f"Error: {e}")