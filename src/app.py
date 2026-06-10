# -*- coding: utf-8 -*-
"""
SIPA v2 - Interfaz de Usuario Premium en Streamlit
El panel interactivo consolida el Coach Psicológico, el Radar de Sesgos y
el Laboratorio de Volatilidad y Anomalías de Mercado.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import os
import sys

# Forzar codificación UTF-8 para consola en Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Importaciones locales seguras
from market_analysis import (
    get_market_data,
    calculate_volatility,
    detect_anomalies,
    get_educational_explanation,
    TICKERS_DICT
)
from coach import get_broker_profile, generate_coach_response, BIASES_COACHING

# Configuración de página de Streamlit
st.set_page_config(
    page_title="SIPA v2 — Coach de Finanzas Personales & Psicología de la Inversión",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Resolver rutas absolutas para cargar los modelos
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models', 'intent_bias')
INTENT_MODEL_PATH = os.path.join(MODEL_DIR, 'intent_model.joblib')
BIAS_MODEL_PATH = os.path.join(MODEL_DIR, 'bias_model.joblib')

@st.cache_resource
def load_ml_models():
    """Carga y cachea los modelos de Machine Learning entrenados."""
    try:
        intent_model = joblib.load(INTENT_MODEL_PATH)
        bias_model = joblib.load(BIAS_MODEL_PATH)
        return intent_model, bias_model, True
    except Exception as e:
        print(f"⚠️ Error al cargar los modelos de ML: {str(e)}")
        return None, None, False

intent_model, bias_model, models_loaded = load_ml_models()

# ==========================================
# 💎 DISEÑO DE ESTÉTICA PREMIUM (CSS PERSONALIZADO)
# ==========================================
st.markdown("""
<style>
    /* Estilo general oscuro y fuentes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Contenedores con efecto Glassmorphism y degradados neon */
    .glass-card {
        background: rgba(15, 23, 42, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .glow-border-indigo {
        border-left: 5px solid #6366F1;
    }
    .glow-border-teal {
        border-left: 5px solid #00F2FE;
    }
    .glow-border-magenta {
        border-left: 5px solid #E100FF;
    }
    
    /* Personalización del Sidebar */
    .css-11xz68, [data-testid="stSidebar"] {
        background-color: #0A0F1D !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Estilos de las pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(10, 15, 29, 0.6);
        padding: 6px 12px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        color: #A3AED0;
        border-radius: 8px;
        padding: 8px 16px;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #FFFFFF;
        background-color: rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        color: #00F2FE !important;
        background-color: rgba(0, 242, 254, 0.1) !important;
        font-weight: 600;
    }
    
    /* Ajustes específicos para burbujas de chat personalizadas */
    .chat-bubble-assistant {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px 14px 14px 2px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🏦 BARRA LATERAL (ONBOARDING Y CONFIGURACIÓN)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='font-size: 26px; margin-bottom: 5px;'>💎 Panel SIPA v2</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A3AED0; font-size: 14px; margin-top:0px;'>Behavioral Finance Engine</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 1. Selector de Broker
    st.markdown("### 🏦 Tu Broker / Banco Online")
    broker_options = {
        "gbm": "GBM+ (México)",
        "trade_republic": "Trade Republic (Europa)",
        "revolut": "Revolut (Global)",
        "scalable_capital": "Scalable Capital (Europa)",
        "interactive_brokers": "Interactive Brokers (Global)",
        "fintual": "Fintual (LATAM)",
        "hey_banco": "Hey Banco (México)",
        "bbva_trader": "BBVA Trader (España/LATAM)",
        "openbank": "Openbank / Santander",
        "robinhood": "Robinhood (EEUU)"
    }
    selected_broker_id = st.selectbox(
        "¿Dónde realizas tus inversiones?",
        options=list(broker_options.keys()),
        format_func=lambda x: broker_options[x]
    )
    
    # Obtener el perfil del broker seleccionado
    broker_profile = get_broker_profile(selected_broker_id)
    
    # 2. Perfil del inversor
    st.markdown("### 👤 Perfil del Inversor")
    exp_level = st.select_slider(
        "Nivel de Experiencia",
        options=["Principiante", "Intermedio", "Avanzado"],
        value="Principiante"
    )
    
    # 3. OpenAI API Key (Opcional)
    st.markdown("### 🔑 Motor Híbrido Conversacional")
    openai_key = st.text_input(
        "OpenAI API Key (Opcional)",
        type="password",
        help="Si no introduces una clave, el Coach SIPA funcionará en local de forma 100% gratuita utilizando un motor experto basado en reglas y psicología científica conductual."
    )
    
    st.markdown("---")
    
    # 📘 Pestaña interactiva de Psicología de la Interfaz del Broker en el Sidebar
    st.markdown(f"### 🛡️ Guía de {broker_profile['name']}")
    with st.expander("⚠️ Alerta de Sesgo en la Interfaz (UX)", expanded=True):
        st.markdown(f"**Sesgo Común:** *{broker_profile['pitfall']}*")
        st.markdown(f"{broker_profile['pitfall_detail']}")
    
    with st.expander("📋 Pasos Recomendados para Principiantes", expanded=False):
        for step in broker_profile["onboarding"]:
            st.markdown(step)
            
    st.markdown("<p style='font-size: 11px; color:#566488; text-align:center; margin-top:20px;'>SIPA v2 © 2026. La predicción del futuro es imposible. Invierte con base científica y disciplina psicológica.</p>", unsafe_allow_html=True)

# ==========================================
# 🧠 INTERFAZ PRINCIPAL (TABS SISTEMA)
# ==========================================
st.markdown("<h1 style='font-size: 40px; margin-bottom: 2px;'>🧠 SIPA v2: Behavioral & Market Coach</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #A3AED0; font-size: 16px; margin-top: 0px; margin-bottom: 25px;'>Asistente psicológico antisesgos y laboratorio del pulso del mercado</p>", unsafe_allow_html=True)

tab_chat, tab_market, tab_guide = st.tabs([
    "💬 Consultorio Psicológico (Coach)",
    "🔬 Laboratorio de Volatilidad y Anomalías",
    "📘 Guía de Estudio de Sesgos"
])

# ------------------------------------------
# PESTAÑA 1: 💬 EL CONSULTORIO PSICOLÓGICO
# ------------------------------------------
with tab_chat:
    if not models_loaded:
        st.error("❌ Los modelos de NLP en `models/intent_bias/` no se encuentran entrenados. Por favor, ejecuta primero `python src/classifier.py` en tu terminal para activar el cerebro de SIPA.")
    else:
        # Layout de 2 columnas: Chat a la izquierda, Radar de Sesgos a la derecha
        col_chat, col_radar = st.columns([2, 1])
        
        with col_chat:
            st.markdown("<div class='glass-card glow-border-indigo'>", unsafe_allow_html=True)
            st.markdown("### 💬 Conversa con SIPA Coach v2")
            st.markdown("<p style='color: #A3AED0; font-size: 13px;'>Expresa tus pensamientos, miedos o planes de inversión. Nuestro modelo de Machine Learning analizará los sesgos psicológicos de tu mensaje en tiempo real.</p>", unsafe_allow_html=True)
            
            # Inicializar historial de chat si no existe
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [
                    {
                        "role": "assistant",
                        "content": (
                            f"👋 ¡Hola! Soy tu **SIPA Coach v2**. Veo que estás usando la plataforma **{broker_profile['name']}**.\n\n"
                            "Cuéntame: ¿estás pensando en comprar o vender algún activo? ¿hay alguna caída que te asuste o una subida vertical en la que quieras entrar? "
                            "Escribe tus pensamientos sin filtros y analizaremos tu perfil psicológico."
                        )
                    }
                ]
            
            # Mostrar historial
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            # Entrada de texto del chat
            user_input = st.chat_input("Escribe tus ideas o preocupaciones sobre tus inversiones...")
            
            if user_input:
                # 1. Mostrar mensaje del usuario
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.markdown(user_input)
                
                # 2. Análisis NLP de Intenciones y Sesgos
                # Clasificador de Intención
                pred_intent = intent_model.predict([user_input])[0]
                
                # Clasificador de Sesgo y cálculo de vectores probabilísticos
                pred_bias = bias_model.predict([user_input])[0]
                bias_probs_vector = bias_model.predict_proba([user_input])[0]
                classes_bias = bias_model.classes_
                
                # Mapear vector de probabilidades a diccionario
                probs_dict = {classes_bias[i]: float(bias_probs_vector[i]) for i in range(len(classes_bias))}
                
                # Guardar el último vector de probabilidades detectado para actualizar el Radar
                st.session_state.last_probs = probs_dict
                st.session_state.last_bias = pred_bias
                
                # 3. Generar la respuesta híbrida del Coach
                coach_output = generate_coach_response(
                    user_text=user_input,
                    detected_intent=pred_intent,
                    detected_bias=pred_bias,
                    bias_probs=probs_dict,
                    broker_id=selected_broker_id,
                    openai_key=openai_key
                )
                
                # Formatear la burbuja del asistente
                assist_resp = ""
                if coach_output["is_llm"]:
                    assist_resp += "✨ **[SIPA AI Coach activo]** \n\n"
                
                assist_resp += f"{coach_output['response']}\n\n"
                
                # Agregar diagnóstico local colapsable
                with st.expander("🔍 Ver Diagnóstico Matemático del NLP Local (Scikit-Learn)", expanded=False):
                    st.markdown(coach_output["diagnostico"])
                    st.write(probs_dict)
                
                # Agregar al historial de chat
                st.session_state.chat_history.append({"role": "assistant", "content": assist_resp})
                
                # Recargar la app para refrescar el Radar Chart a la derecha
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_radar:
            st.markdown("<div class='glass-card glow-border-magenta'>", unsafe_allow_html=True)
            st.markdown("### 📊 Radar de Sesgos Cognitivos")
            st.markdown("<p style='color: #A3AED0; font-size: 13px;'>Este gráfico dinámico se alimenta de la clasificación probabilística del modelo NLP local.</p>", unsafe_allow_html=True)
            
            # Obtener probabilidades del st.session_state o inicializarlas en cero
            if "last_probs" not in st.session_state:
                st.session_state.last_probs = {
                    "panico": 0.05,
                    "fomo": 0.05,
                    "overconfidence": 0.05,
                    "loss_aversion": 0.05,
                    "anchoring": 0.05,
                    "ninguno": 0.75
                }
                st.session_state.last_bias = "ninguno"
            
            # Renderizar el gráfico de radar espectacular usando Plotly
            categories = ['Pánico', 'FOMO', 'Sobreconfianza', 'Aversión Pérdida', 'Anclaje', 'Racional']
            keys = ['panico', 'fomo', 'overconfidence', 'loss_aversion', 'anchoring', 'ninguno']
            values = [st.session_state.last_probs.get(k, 0.0) for k in keys]
            
            # Cerrar el círculo del radar
            categories_closed = categories + [categories[0]]
            values_closed = values + [values[0]]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                fillcolor='rgba(225, 0, 255, 0.25)', # Magenta con transparencia
                line=dict(color='#E100FF', width=3),
                name='Probabilidad de Sesgo'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1],
                        gridcolor='rgba(255, 255, 255, 0.08)',
                        linecolor='rgba(255, 255, 255, 0.08)',
                        tickfont=dict(color='#A3AED0', size=9)
                    ),
                    angularaxis=dict(
                        gridcolor='rgba(255, 255, 255, 0.08)',
                        tickfont=dict(color='#FFFFFF', size=11, family="Outfit")
                    ),
                    bgcolor='rgba(10, 15, 29, 0.7)'
                ),
                showlegend=False,
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=35, r=35, t=20, b=20),
                height=310
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Explicación resumida de tu estado actual
            detected_bias_name = st.session_state.last_bias
            bias_coaching_info = BIASES_COACHING.get(detected_bias_name, BIASES_COACHING["ninguno"])
            
            st.markdown(f"**Sesgo Dominante Detectado:** `{detected_bias_name.upper()}`")
            st.markdown(f"<p style='font-size: 13px; color:#A3AED0;'>{bias_coaching_info['explanation']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------
# PESTAÑA 2: 🔬 LABORATORIO DE VOLATILIDAD Y ANOMALÍAS
# ------------------------------------------
with tab_market:
    st.markdown("<div class='glass-card glow-border-teal'>", unsafe_allow_html=True)
    st.markdown("### 🔬 Laboratorio del Pulso del Mercado")
    st.markdown("<p style='color: #A3AED0; font-size: 13px;'>Selecciona un índice de referencia o acción popular para analizar sus anomalías de comportamiento histórico y su nivel de volatilidad actual. Recuerda: las anomalías son normales en el comportamiento humano colectivo.</p>", unsafe_allow_html=True)
    
    # Filtros interactivos del mercado
    col_t, col_p, col_z = st.columns([2, 1, 1])
    with col_t:
        selected_ticker = st.selectbox(
            "Selecciona el Activo a Analizar",
            options=list(TICKERS_DICT.keys()),
            format_func=lambda x: f"{x} — {TICKERS_DICT[x]}"
        )
    with col_p:
        selected_period = st.selectbox(
            "Rango de Tiempo Histórico",
            options=["1y", "2y", "5y"],
            index=1
        )
    with col_z:
        z_threshold = st.slider(
            "Sensibilidad del Detector Z-Score",
            min_value=2.0,
            max_value=4.0,
            value=2.8,
            step=0.2,
            help="Desviación estándar para marcar retornos como anomalías. Un valor más bajo detecta más eventos, un valor más alto detecta solo extremos."
        )
        
    # Cargar y procesar datos dinámicamente
    # Ponemos st.spinner para avisar al usuario
    with st.spinner("Descargando cotizaciones y analizando fluctuaciones matemáticas..."):
        df_raw = get_market_data(selected_ticker, period=selected_period)
        df_processed = calculate_volatility(df_raw)
        df_processed = detect_anomalies(df_processed, z_threshold=z_threshold)
        
    # 1. Gráfico de Precios con Anomalías pintadas con Plotly
    fig_price = go.Figure()
    
    # Trazado de precio normal
    fig_price.add_trace(go.Scatter(
        x=df_processed.index,
        y=df_processed['Close'],
        mode='lines',
        line=dict(color='#00F2FE', width=2),
        name='Precio de Cierre'
    ))
    
    # Trazado de Anomalías de Pánico (Caídas extremas)
    panic_points = df_processed[df_processed['Anomaly_Type'] == 'Pánico']
    if not panic_points.empty:
        fig_price.add_trace(go.Scatter(
            x=panic_points.index,
            y=panic_points['Close'],
            mode='markers',
            marker=dict(
                color='#FF416C', # Rojo vivo
                size=11,
                symbol='circle',
                line=dict(color='#FFFFFF', width=1.5)
            ),
            name='Anomalía de Pánico (Venta Colectiva)'
        ))
        
    # Trazado de Anomalías de Euforia (Subidas extremas)
    euphoria_points = df_processed[df_processed['Anomaly_Type'] == 'Euforia']
    if not euphoria_points.empty:
        fig_price.add_trace(go.Scatter(
            x=euphoria_points.index,
            y=euphoria_points['Close'],
            mode='markers',
            marker=dict(
                color='#FFA07A', # Naranja / Gold
                size=11,
                symbol='circle',
                line=dict(color='#FFFFFF', width=1.5)
            ),
            name='Anomalía de Euforia (FOMO Masivo)'
        ))
        
    fig_price.update_layout(
        title=dict(
            text=f"Precio Histórico y Anomalías Detectadas - {TICKERS_DICT[selected_ticker]}",
            font=dict(color='#FFFFFF', size=16, family="Outfit")
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            tickfont=dict(color='#A3AED0'),
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            tickfont=dict(color='#A3AED0')
        ),
        paper_bgcolor='rgba(10, 15, 29, 0.5)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=40, r=40, t=50, b=45),
        height=380,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#A3AED0', size=11)
        )
    )
    
    st.plotly_chart(fig_price, use_container_width=True)
    
    # 2. Gráfico de Volatilidad Histórica Móvil Anualizada
    fig_vol = go.Figure()
    
    fig_vol.add_trace(go.Scatter(
        x=df_processed.index,
        y=df_processed['Vol_21'] * 100, # Representar en %
        mode='lines',
        line=dict(color='#E100FF', width=1.5),
        name='Volatilidad Móvil Corto Plazo (21d, ~1 mes)'
    ))
    
    fig_vol.add_trace(go.Scatter(
        x=df_processed.index,
        y=df_processed['Vol_252'] * 100,
        mode='lines',
        line=dict(color='#38EF7D', width=2),
        name='Volatilidad Móvil Largo Plazo (252d, ~1 año)'
    ))
    
    fig_vol.update_layout(
        title=dict(
            text="Ciclo de Volatilidad Anualizada Móvil (%)",
            font=dict(color='#FFFFFF', size=16, family="Outfit")
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            tickfont=dict(color='#A3AED0')
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            tickfont=dict(color='#A3AED0')
        ),
        paper_bgcolor='rgba(10, 15, 29, 0.5)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=40, r=40, t=50, b=40),
        height=220,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#A3AED0', size=11)
        )
    )
    
    st.plotly_chart(fig_vol, use_container_width=True)
    
    # 3. Listado interactivo de Anomalías Históricas con sus explicaciones
    anomalies_only = df_processed[df_processed['Anomaly_Type'] != 'Normal'].sort_index(ascending=False)
    
    st.markdown("### 📋 Bitácora Científica de Anomalías")
    if anomalies_only.empty:
        st.markdown(f"✅ *No se han detectado anomalías extremas con la sensibilidad Z-Score de {z_threshold} en el período seleccionado. El comportamiento es estable.*")
    else:
        st.markdown(f"Se han identificado **{len(anomalies_only)} días anómalos** en la muestra. Haz clic en las pestañas inferiores para analizar y estudiar la psicología detrás de cada día:")
        
        # Mostrar las últimas 5 anomalías para no saturar la pantalla
        last_anomalies = anomalies_only.head(5)
        
        for idx, row in last_anomalies.iterrows():
            fecha_str = idx.strftime('%d de %B de %Y')
            tipo_anomalia = row['Anomaly_Type']
            retorno_dia = row['Return'] * 100
            vol_dia = row['Volume']
            z_score = row['Return_Z']
            
            emoji_tipo = "📉" if tipo_anomalia == 'Pánico' else "📈"
            color_tipo = "#FF416C" if tipo_anomalia == 'Pánico' else "#FFA07A"
            
            with st.expander(f"{emoji_tipo} Día de {tipo_anomalia}: {fecha_str} (Retorno: {retorno_dia:+.2f}%)"):
                st.markdown(f"<div style='border-left: 4px solid {color_tipo}; padding-left: 15px;'>", unsafe_allow_html=True)
                st.markdown(f"**Fecha:** {fecha_str}")
                st.markdown(f"**Retorno del día:** `{retorno_dia:+.2f}%` (Un Z-Score de `{z_score:+.2f}` desviaciones estándar)")
                st.markdown(f"**Volumen transaccionado:** `{vol_dia:,} unidades` (Volumen anormal: **{'SÍ' if row['Anomaly_Volume'] else 'NO'}**)")
                st.markdown("---")
                
                # Explicación conductual detallada
                explicacion = get_educational_explanation(tipo_anomalia, z_score, selected_ticker)
                st.markdown(explicacion)
                st.markdown("</div>", unsafe_allow_html=True)
                
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------
# PESTAÑA 3: 📘 GUÍA DE ESTUDIO DE SESGOS
# ------------------------------------------
with tab_guide:
    st.markdown("<div class='glass-card glow-border-magenta'>", unsafe_allow_html=True)
    st.markdown("### 📘 Biblioteca Educativa de Sesgos Cognitivos Financieros")
    st.markdown("<p style='color: #A3AED0; font-size: 13px;'>La mente humana está evolutivamente optimizada para la supervivencia física en la selva, no para tomar decisiones matemáticas en el mercado moderno. Estudia estas trampas mentales para volverte un inversor racional e imperturbable.</p>", unsafe_allow_html=True)
    
    for key, val in BIASES_COACHING.items():
        if key == "ninguno":
            continue
            
        st.markdown(f"#### 🧠 {key.upper().replace('_', ' ')}")
        st.markdown(f"**¿Qué es?** {val['explanation']}")
        st.markdown(val["coach_response"])
        st.markdown(val["exercise"])
        st.markdown("---")
        
    st.markdown("</div>", unsafe_allow_html=True)
