import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# 1. CONFIGURACION Y ESTILO
st.set_page_config(page_title="DataJam Bogota 2026", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #31333f; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL
with st.sidebar:
    st.title("Panel de Control")
    years = [2017, 2018, 2020, 2021, 2022]
    selected_years = st.multiselect("Seleccione los Anios:", years, default=years)
    st.markdown("---")
    st.info("Navegue por las pestanias para ver diferentes perspectivas.")

# 3. FUNCION DE CARGA
@st.cache_data
def cargar_y_filtrar(anios_seleccionados):
    df_t = pd.read_csv('osb_evento_transporte.csv', sep=';', encoding='latin-1')
    df_l = pd.read_csv('lluvia_mensual_bogota.csv')
    df_t.columns = df_t.columns.str.strip().str.upper()
    df_l.columns = df_l.columns.str.strip().str.upper()
    df_filt = df_t[df_t['ANO'].isin(anios_seleccionados)].copy()
    df_l_filt = df_l[df_l['ANIO'].isin(anios_seleccionados)].copy()
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
    st.title('Observatorio de Movilidad y Clima - Bogota')
    
    r_val = stats.linregress(lluvia.values, muertes.values)[2]
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Correlacion (r)", f"{r_val:.3f}")
    with m2: st.metric("Impacto Clima (R2)", f"{r_val**2:.1%}")
    with m3: st.metric("Total Muertes", f"{int(muertes.sum())}")
    with m4: st.metric("Pico Mensual", muertes.idxmax().capitalize())

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["Relacion Clima", "Perfil Geografico", "Causas y Tipos"])

    with tab1:
        c_a, c_b = st.columns(2)
        with c_a:
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(x=meses, y=lluvia, name="Lluvia (mm)", marker_color='#3498DB', opacity=0.5))
            fig1.add_trace(go.Scatter(x=meses, y=muertes, name="Muertes", line=dict(color='#E74C3C', width=4), yaxis="y2"))
            fig1.update_layout(title="Precipitacion vs Mortalidad", yaxis2=dict(overlaying="y", side="right"), template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
        with c_b:
            l_n = (lluvia - lluvia.min())/(lluvia.max() - lluvia.min())
            m_n = (muertes - muertes.min())/(muertes.max() - muertes.min())
            st.plotly_chart(px.line(x=meses, y=[l_n, m_n], labels={'value':'Escala 0-1', 'x':'Meses'}, title="Sincronia de Tendencias", template="plotly_dark"), use_container_width=True)

    with tab2:
        c_c, c_d = st.columns(2)
        with c_c:
            excluir_loc = ['BOGOTA', 'BOGOTÁ', 'SDP', 'SIN INFORMACION', 'SUBESTACION']
            df_loc = df_full[~df_full['LOCALIDAD'].str.upper().isin(excluir_loc)]
            top_loc = df_loc.groupby('LOCALIDAD')['CASOS'].sum().sort_values().tail(10)
            st.plotly_chart(px.bar(top_loc, orientation='h', title="Top 10 Localidades Criticas", color_discrete_sequence=['#F39C12'], template="plotly_dark"), use_container_width=True)
        with c_d:
            dist_c = df_full.groupby('CONDICION_DE_LA_VICTIMA_AT_')['CASOS'].sum()
            fig_pie_actor = px.pie(values=dist_c, names=dist_c.index, hole=.4, title="Actor Vial Involucrado", template="plotly_dark")
            fig_pie_actor.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie_actor, use_container_width=True)

    with tab3:
        c_e, c_f = st.columns(2)
        with c_e:
            col_cau = 'CIRCUNSTANCIA_DEL_HECHO_DETALLADA'
            df_c_limpio = df_full[~df_full[col_cau].str.upper().str.contains('OTRO|OTRA|SIN INFO|NO APLICA', na=False)]
            dist_cau = df_c_limpio.groupby(col_cau)['CASOS'].sum().sort_values().tail(8)
            st.plotly_chart(px.bar(dist_cau, orientation='h', title="Causas mas Comunes", labels={'value': 'Muertes', 'index': 'Causa'}, color_discrete_sequence=['#45B39D'], template="plotly_dark"), use_container_width=True)
            
        with c_f:
            # --- TIPO DE SINIESTRO SOFISTICADO (ARREGLADO) ---
            col_tip = 'CLASE_O_TIPO_DE_ACCIDENTE_DE_TRANSPORTE'
            dist_tipo = df_full.groupby(col_tip)['CASOS'].sum().sort_values(ascending=False).head(6)
            
            fig_tipo = go.Figure(data=[go.Pie(
                labels=dist_tipo.index, 
                values=dist_tipo.values, 
                hole=0.5,
                marker=dict(colors=px.colors.sequential.Tealgrn),
                textinfo='label+percent',
                textposition='outside', # Esto saca las etiquetas para que no se vea vacio
                insidetextorientation='radial'
            )])
            
            fig_tipo.update_layout(
                title="Distribucion por Tipo de Siniestro",
                template="plotly_dark",
                showlegend=False,
                margin=dict(t=50, b=20, l=20, r=20), # Ajustamos los margenes para que use todo el cuadro
                annotations=[dict(text='Tipos', x=0.5, y=0.5, font_size=20, showarrow=False)] # Texto en el centro de la dona
            )
            st.plotly_chart(fig_tipo, use_container_width=True)

    st.markdown("---")
    st.subheader("Franjas Horarias de Mayor Riesgo")
    col_hora = 'RANGO_DE_HORA_DEL_HECHO_XXX3_HORAS_'
    df_h = df_full.copy()
    df_h[col_hora] = df_h[col_hora].astype(str).str.replace(r'[\(\)]', '', regex=True).str.strip()
    df_h = df_h[~df_h[col_hora].str.upper().str.contains('SIN INFO')]
    dist_h = df_h.groupby(col_hora)['CASOS'].sum().sort_values(ascending=False).head(8)
    fig_h = px.bar(x=dist_h.index, y=dist_h.values, color=dist_h.values, color_continuous_scale='Reds', labels={'x': 'Horas', 'y': 'Muertes'}, template="plotly_dark")
    fig_h.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
    st.plotly_chart(fig_h, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")