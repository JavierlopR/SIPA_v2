# -*- coding: utf-8 -*-
"""
SIPA v2 - Interfaz de Usuario Premium en Streamlit
Coach psicológico financiero universal con análisis técnico en tiempo real.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Importaciones locales seguras ──────────────────────────────────────────
from market_analysis import (
    get_market_data, calculate_volatility, detect_anomalies,
    get_educational_explanation, get_ticker_audit, extract_ticker_from_text,
    TICKERS_DICT,
)
from coach import (
    generate_coach_response, BIASES_COACHING, BROKERS_PROFILE,
)

# ── Configuración Streamlit ────────────────────────────────────────────────
st.set_page_config(
    page_title="SIPA v2 — Coach de Finanzas Personales & Psicología de la Inversión",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models', 'intent_bias')
INTENT_MODEL_PATH = os.path.join(MODEL_DIR, 'intent_model.joblib')
BIAS_MODEL_PATH = os.path.join(MODEL_DIR, 'bias_model.joblib')


@st.cache_resource
def load_ml_models():
    try:
        return joblib.load(INTENT_MODEL_PATH), joblib.load(BIAS_MODEL_PATH), True
    except Exception as e:
        return None, None, False


intent_model, bias_model, models_loaded = load_ml_models()

# ══════════════════════════════════════════════════════════════════════════
# 💎 CSS PREMIUM
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

h1, h2, h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.glass-card {
    background: rgba(15, 23, 42, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(12px);
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.glow-border-indigo  { border-left: 5px solid #6366F1; }
.glow-border-teal    { border-left: 5px solid #00F2FE; }
.glow-border-magenta { border-left: 5px solid #E100FF; }
.glow-border-green   { border-left: 5px solid #38EF7D; }

[data-testid="stSidebar"] {
    background-color: #0A0F1D !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background-color: rgba(10,15,29,0.6);
    padding: 6px 12px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif;
    color: #A3AED0;
    border-radius: 8px;
    padding: 8px 16px;
    transition: all 0.3s;
}

.stTabs [data-baseweb="tab"]:hover { color: #FFF; background-color: rgba(255,255,255,0.05); }
.stTabs [aria-selected="true"] {
    color: #00F2FE !important;
    background-color: rgba(0,242,254,0.1) !important;
    font-weight: 600;
}

.metric-badge {
    background: rgba(0,242,254,0.08);
    border: 1px solid rgba(0,242,254,0.2);
    border-radius: 10px;
    padding: 10px 15px;
    text-align: center;
    margin: 4px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# 🏦 SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<h2 style='font-size:26px; margin-bottom:5px;'>💎 Panel SIPA v2</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A3AED0;font-size:14px;margin-top:0'>Behavioral Finance Engine</p>", unsafe_allow_html=True)
    st.markdown("---")

    # ── OpenAI API Key ─────────────────────────────────────────────────────
    st.markdown("### 🔑 Motor Conversacional")
    openai_key = st.text_input(
        "OpenAI API Key (Opcional)",
        type="password",
        help="Sin clave el Coach funciona al 100% gratis en local con motor de reglas y ML."
    )

    # ── Perfil del inversor ────────────────────────────────────────────────
    st.markdown("### 👤 Tu Perfil")
    exp_level = st.select_slider(
        "Nivel de Experiencia",
        options=["Principiante", "Intermedio", "Avanzado"],
        value="Principiante",
    )

    # ── Consultor de Broker (opcional, no obligatorio) ─────────────────────
    st.markdown("### 🏦 Consultar Broker (Opcional)")
    broker_options_display = {"": "— Ninguno / No sé —"}
    broker_options_display.update({k: v["name"] for k, v in BROKERS_PROFILE.items()})
    selected_broker_id = st.selectbox(
        "¿Usas alguna de estas plataformas?",
        options=list(broker_options_display.keys()),
        format_func=lambda x: broker_options_display[x],
        help="Puedes dejar esto en blanco. Solo lo usamos para darte contexto específico de tu plataforma."
    )

    if selected_broker_id and selected_broker_id in BROKERS_PROFILE:
        bp = BROKERS_PROFILE[selected_broker_id]
        with st.expander(f"⚠️ Trampa en {bp['name']}", expanded=False):
            st.markdown(f"**{bp['pitfall']}**")
            st.markdown(bp['pitfall_detail'])
        with st.expander("💡 Recomendaciones", expanded=False):
            for r in bp["recomendacion"]:
                st.markdown(f"- {r}")
        with st.expander("💰 Comisiones", expanded=False):
            st.markdown(f"**Mínimo:** {bp['minimo_deposito']}")
            st.markdown(f"**Comisiones:** {bp['comisiones']}")
            st.markdown(f"**Activos:** {bp['activos_disponibles']}")

    st.markdown("---")
    st.markdown(
        "<p style='font-size:11px;color:#566488;text-align:center;'>SIPA v2 © 2026. "
        "Invierte con base científica. La predicción del futuro es imposible.</p>",
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════
# 🧠 HEADER PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════
st.markdown("<h1 style='font-size:40px;margin-bottom:2px;'>🧠 SIPA v2: Behavioral & Market Coach</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#A3AED0;font-size:16px;margin-top:0;margin-bottom:25px;'>Asistente universal de psicología financiera con análisis técnico en tiempo real</p>", unsafe_allow_html=True)

tab_chat, tab_broker, tab_market, tab_guide = st.tabs([
    "💬 Coach Psicológico",
    "🏦 Comparador de Brokers",
    "🔬 Laboratorio de Mercado",
    "📘 Guía de Sesgos",
])

# ══════════════════════════════════════════════════════════════════════════
# TAB 1: COACH PSICOLÓGICO
# ══════════════════════════════════════════════════════════════════════════
with tab_chat:
    if not models_loaded:
        st.error(
            "❌ Los modelos de NLP no están cargados. "
            "Ejecuta primero: `python src/classifier.py`"
        )
    else:
        col_chat, col_radar = st.columns([2, 1])

        with col_chat:
            st.markdown("<div class='glass-card glow-border-indigo'>", unsafe_allow_html=True)
            st.markdown("### 💬 Conversa con SIPA Coach")
            st.markdown(
                "<p style='color:#A3AED0;font-size:13px;'>"
                "Escribe cualquier duda, miedo o plan de inversión. Si mencionas un activo (ej: 'compré nvidia' o 'debería vender Bitcoin'), "
                "SIPA descargará datos reales de mercado para darte un análisis técnico personalizado junto al diagnóstico psicológico. "
                "Puedes preguntar sobre <b>cualquier broker</b>: Trade Republic, Revolut, IBKR, GBM, Fintual, Robinhood, BBVA, Openbank...</p>",
                unsafe_allow_html=True
            )

            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [
                    {
                        "role": "assistant",
                        "content": (
                            "👋 ¡Hola! Soy **SIPA Coach v2**, tu asistente de psicología financiera y mercados.\n\n"
                            "Puedo ayudarte con:\n"
                            "- 📊 **Análisis técnico en tiempo real** de cualquier acción, ETF o cripto que menciones\n"
                            "- 🧠 **Diagnóstico de sesgos** cognitivos en tus decisiones de inversión\n"
                            "- 🏦 **Consultas sobre cualquier broker**: comisiones, trampas de diseño, recomendaciones\n"
                            "- ❓ **Gestión de posiciones**: ¿vender? ¿comprar más? ¿mantener?\n\n"
                            "Cuéntame: ¿qué tienes en mente? Puedes escribir algo como: "
                            "*'Compré Tesla y está cayendo, ¿vendo?'* o "
                            "*'¿Qué piensas de Trade Republic para empezar?'*"
                        )
                    }
                ]

            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            user_input = st.chat_input("Escribe tu consulta sobre inversiones, activos o brokers...")

            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.markdown(user_input)

                with st.chat_message("assistant"):
                    with st.spinner("Analizando tu mensaje y consultando mercados..."):
                        # ── NLP: Intención y Sesgo ─────────────────────────
                        pred_intent = intent_model.predict([user_input])[0]
                        pred_bias = bias_model.predict([user_input])[0]
                        bias_probs_vector = bias_model.predict_proba([user_input])[0]
                        classes_bias = bias_model.classes_
                        probs_dict = {classes_bias[i]: float(bias_probs_vector[i]) for i in range(len(classes_bias))}

                        st.session_state.last_probs = probs_dict
                        st.session_state.last_bias = pred_bias

                        # ── Detección de ticker en el mensaje ─────────────
                        detected_ticker = extract_ticker_from_text(user_input)
                        ticker_audit = None
                        if detected_ticker:
                            ticker_audit = get_ticker_audit(detected_ticker)

                        # ── Detección de broker mencionado en texto ────────
                        msg_lower = user_input.lower()
                        mentioned_broker = selected_broker_id or ""
                        for bid, bdata in BROKERS_PROFILE.items():
                            if bdata["name"].lower().split()[0] in msg_lower or bid.replace("_", " ") in msg_lower:
                                mentioned_broker = bid
                                break

                        # ── Generar respuesta del Coach ────────────────────
                        coach_output = generate_coach_response(
                            user_text=user_input,
                            detected_intent=pred_intent,
                            detected_bias=pred_bias,
                            bias_probs=probs_dict,
                            broker_id=mentioned_broker if mentioned_broker else None,
                            openai_key=openai_key,
                            ticker_audit=ticker_audit,
                        )

                    # ── Renderizar respuesta ───────────────────────────────
                    mode_badge = "✨ **[GPT-4o-mini]**" if coach_output.get("is_llm") else "🧠 **[Motor SIPA Local]**"
                    full_response = f"{mode_badge}\n\n{coach_output['response']}"
                    st.markdown(full_response)

                    # ── Panel colapsable: diagnóstico NLP ──────────────────
                    with st.expander("🔍 Diagnóstico NLP (detalles técnicos)", expanded=False):
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Intención", pred_intent)
                        c2.metric("Sesgo Dominante", pred_bias)
                        c3.metric("Ticker detectado", detected_ticker or "ninguno")
                        st.write("**Probabilidades de sesgos:**")
                        for k, v in sorted(probs_dict.items(), key=lambda x: -x[1]):
                            pct = v * 100
                            st.progress(v, text=f"{k}: {pct:.1f}%")

                    # ── Métricas del activo si se detectó ticker ──────────
                    if ticker_audit and not ticker_audit.get("simulado") and ticker_audit.get("precio_actual"):
                        with st.expander(
                            f"📊 Métricas de mercado — {ticker_audit['nombre']} ({ticker_audit['ticker']})",
                            expanded=True
                        ):
                            m1, m2, m3, m4, m5 = st.columns(5)
                            ret = ticker_audit['retorno_hoy']
                            signo = "+" if ret >= 0 else ""
                            m1.metric("Precio", f"${ticker_audit['precio_actual']:,.2f}")
                            m2.metric("Hoy", f"{signo}{ret:.2f}%")
                            m3.metric("RSI 14d", ticker_audit['rsi_14'])
                            m4.metric("vs SMA50", f"{ticker_audit['distancia_sma']:+.1f}%")
                            m5.metric("Vol. Anual", f"{ticker_audit['vol_anualizada']:.1f}%")

                            st.markdown(f"**Estado técnico:** `{ticker_audit['estado_tecnico'].upper()}`")
                            if ticker_audit['alerta_tecnica']:
                                st.info(ticker_audit['alerta_tecnica'])

                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            st.markdown("</div>", unsafe_allow_html=True)

        with col_radar:
            st.markdown("<div class='glass-card glow-border-magenta'>", unsafe_allow_html=True)
            st.markdown("### 📊 Radar de Sesgos")
            st.markdown(
                "<p style='color:#A3AED0;font-size:12px;'>Se actualiza en tiempo real con cada mensaje que envías.</p>",
                unsafe_allow_html=True
            )

            if "last_probs" not in st.session_state:
                st.session_state.last_probs = {
                    "panico": 0.05, "fomo": 0.05, "overconfidence": 0.05,
                    "loss_aversion": 0.05, "anchoring": 0.05, "ninguno": 0.75
                }
                st.session_state.last_bias = "ninguno"

            cats = ['Pánico', 'FOMO', 'Sobreconfianza', 'Av. Pérdida', 'Anclaje', 'Racional']
            keys = ['panico', 'fomo', 'overconfidence', 'loss_aversion', 'anchoring', 'ninguno']
            vals = [st.session_state.last_probs.get(k, 0.0) for k in keys]
            cats_c = cats + [cats[0]]
            vals_c = vals + [vals[0]]

            fig_r = go.Figure()
            fig_r.add_trace(go.Scatterpolar(
                r=vals_c, theta=cats_c, fill='toself',
                fillcolor='rgba(225,0,255,0.25)',
                line=dict(color='#E100FF', width=3),
                name='Probabilidad'
            ))
            fig_r.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0,1],
                        gridcolor='rgba(255,255,255,0.08)',
                        linecolor='rgba(255,255,255,0.08)',
                        tickfont=dict(color='#A3AED0', size=9)),
                    angularaxis=dict(gridcolor='rgba(255,255,255,0.08)',
                        tickfont=dict(color='#FFF', size=11, family="Outfit")),
                    bgcolor='rgba(10,15,29,0.7)',
                ),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=35, r=35, t=20, b=20),
                height=300,
            )
            st.plotly_chart(fig_r, use_container_width=True)

            detected_b = st.session_state.last_bias
            bias_info_radar = BIASES_COACHING.get(detected_b, BIASES_COACHING["ninguno"])
            st.markdown(f"**Sesgo detectado:** `{detected_b.upper()}`")
            st.markdown(
                f"<p style='font-size:12px;color:#A3AED0;'>{bias_info_radar['explanation']}</p>",
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# TAB 2: COMPARADOR DE BROKERS
# ══════════════════════════════════════════════════════════════════════════
with tab_broker:
    st.markdown("<div class='glass-card glow-border-green'>", unsafe_allow_html=True)
    st.markdown("### 🏦 Comparador Universal de Plataformas de Inversión")
    st.markdown(
        "<p style='color:#A3AED0;font-size:13px;'>"
        "Consulta las características, trampas psicológicas de diseño y recomendaciones de las principales "
        "plataformas de inversión globales. Selecciona una o compara varias.</p>",
        unsafe_allow_html=True
    )

    # Selector múltiple de brokers
    broker_names = {k: v["name"] for k, v in BROKERS_PROFILE.items()}
    selected_brokers = st.multiselect(
        "Selecciona los brokers a comparar",
        options=list(broker_names.keys()),
        default=["trade_republic", "revolut", "interactive_brokers"],
        format_func=lambda x: broker_names[x],
    )

    if selected_brokers:
        # Tabla comparativa
        st.markdown("#### 📋 Comparativa Rápida")
        rows = []
        for bid in selected_brokers:
            bp = BROKERS_PROFILE[bid]
            rows.append({
                "Broker": bp["name"],
                "Región": bp["region"],
                "Tipo": bp["tipo"],
                "Depósito Mín.": bp["minimo_deposito"],
                "Comisiones": bp["comisiones"][:70] + "..." if len(bp["comisiones"]) > 70 else bp["comisiones"],
                "Sesgo/Trampa": bp["pitfall"],
            })
        st.dataframe(pd.DataFrame(rows).set_index("Broker"), use_container_width=True)

        st.markdown("#### 🔎 Análisis Detallado por Plataforma")
        broker_tabs = st.tabs([broker_names[b] for b in selected_brokers])
        for i, bid in enumerate(selected_brokers):
            bp = BROKERS_PROFILE[bid]
            with broker_tabs[i]:
                col_l, col_r = st.columns([1, 1])
                with col_l:
                    st.markdown(f"**Región:** {bp['region']}")
                    st.markdown(f"**Tipo:** {bp['tipo']}")
                    st.markdown(f"**Depósito mínimo:** {bp['minimo_deposito']}")
                    st.markdown(f"**Activos disponibles:** {bp['activos_disponibles']}")
                    st.markdown(f"**Comisiones:** {bp['comisiones']}")
                with col_r:
                    st.markdown("**✅ Ventajas:**")
                    st.success(bp["ventajas"])
                    st.markdown("**❌ Desventajas:**")
                    st.error(bp["desventajas"])

                st.markdown("---")
                st.markdown("**⚠️ Trampa de Diseño Psicológico (UX):**")
                st.warning(f"**{bp['pitfall']}** — {bp['pitfall_detail']}")

                st.markdown("**💡 Qué hacer como inversor en esta plataforma:**")
                for r in bp["recomendacion"]:
                    st.markdown(f"- {r}")

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# TAB 3: LABORATORIO DE MERCADO
# ══════════════════════════════════════════════════════════════════════════
with tab_market:
    st.markdown("<div class='glass-card glow-border-teal'>", unsafe_allow_html=True)
    st.markdown("### 🔬 Laboratorio del Pulso del Mercado")
    st.markdown(
        "<p style='color:#A3AED0;font-size:13px;'>"
        "Analiza anomalías de comportamiento colectivo (pánico y euforia) en cualquier activo del mercado global. "
        "Los puntos rojos y naranjas en el gráfico son días donde el comportamiento de los inversores fue estadísticamente irracional.</p>",
        unsafe_allow_html=True
    )

    col_t, col_p, col_z = st.columns([2, 1, 1])
    with col_t:
        selected_ticker = st.selectbox(
            "Activo a Analizar",
            options=list(TICKERS_DICT.keys()),
            format_func=lambda x: f"{x} — {TICKERS_DICT[x]}",
        )
    with col_p:
        selected_period = st.selectbox("Rango Histórico", options=["1y", "2y", "5y"], index=1)
    with col_z:
        z_threshold = st.slider("Sensibilidad Z-Score", min_value=2.0, max_value=4.0, value=2.8, step=0.2)

    # Auditoría en tiempo real del ticker seleccionado
    with st.spinner("Obteniendo datos en tiempo real..."):
        audit_lab = get_ticker_audit(selected_ticker)

    if not audit_lab.get("simulado") and audit_lab.get("precio_actual"):
        m1, m2, m3, m4, m5 = st.columns(5)
        ret_lab = audit_lab['retorno_hoy']
        sig = "+" if ret_lab >= 0 else ""
        m1.metric("Precio actual", f"${audit_lab['precio_actual']:,.2f}")
        m2.metric("Cambio hoy", f"{sig}{ret_lab:.2f}%")
        m3.metric("RSI 14 días", audit_lab['rsi_14'])
        m4.metric("vs SMA50", f"{audit_lab['distancia_sma']:+.1f}%")
        m5.metric("Volatilidad anual", f"{audit_lab['vol_anualizada']:.1f}%")
        st.caption(f"Estado técnico: **{audit_lab['estado_tecnico'].upper()}** — {audit_lab['alerta_tecnica'][:200]}")
    else:
        st.caption("⚠️ Datos de tiempo real no disponibles — usando simulación educativa.")

    # Descarga y proceso de datos históricos
    with st.spinner("Analizando anomalías históricas..."):
        df_raw = get_market_data(selected_ticker, period=selected_period)
        df_v = calculate_volatility(df_raw)
        df_v = detect_anomalies(df_v, z_threshold=z_threshold)

    # Gráfico de precios con anomalías
    fig_p = go.Figure()
    fig_p.add_trace(go.Scatter(
        x=df_v.index, y=df_v['Close'], mode='lines',
        line=dict(color='#00F2FE', width=2), name='Precio de Cierre'
    ))
    panics = df_v[df_v['Anomaly_Type'] == 'Pánico']
    eufs = df_v[df_v['Anomaly_Type'] == 'Euforia']
    if not panics.empty:
        fig_p.add_trace(go.Scatter(
            x=panics.index, y=panics['Close'], mode='markers',
            marker=dict(color='#FF416C', size=11, symbol='circle', line=dict(color='#FFF', width=1.5)),
            name='Pánico (Venta Colectiva)'
        ))
    if not eufs.empty:
        fig_p.add_trace(go.Scatter(
            x=eufs.index, y=eufs['Close'], mode='markers',
            marker=dict(color='#FFA07A', size=11, symbol='circle', line=dict(color='#FFF', width=1.5)),
            name='Euforia (FOMO Masivo)'
        ))
    fig_p.update_layout(
        title=dict(text=f"Precio y Anomalías — {TICKERS_DICT[selected_ticker]}", font=dict(color='#FFF', size=16, family="Outfit")),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#A3AED0'), rangeslider=dict(visible=False)),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#A3AED0')),
        paper_bgcolor='rgba(10,15,29,0.5)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=50, b=45), height=390,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#A3AED0', size=11)),
    )
    st.plotly_chart(fig_p, use_container_width=True)

    # Gráfico de volatilidad
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(
        x=df_v.index, y=df_v['Vol_21'] * 100, mode='lines',
        line=dict(color='#E100FF', width=1.5), name='Volatilidad 21d (corto plazo)'
    ))
    fig_vol.add_trace(go.Scatter(
        x=df_v.index, y=df_v['Vol_252'] * 100, mode='lines',
        line=dict(color='#38EF7D', width=2), name='Volatilidad 252d (largo plazo)'
    ))
    fig_vol.update_layout(
        title=dict(text="Volatilidad Histórica Anualizada (%)", font=dict(color='#FFF', size=15, family="Outfit")),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#A3AED0')),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#A3AED0')),
        paper_bgcolor='rgba(10,15,29,0.5)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=50, b=40), height=220,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#A3AED0', size=11)),
    )
    st.plotly_chart(fig_vol, use_container_width=True)

    # Bitácora de anomalías
    st.markdown("### 📋 Bitácora de Días Anómalos")
    anoms = df_v[df_v['Anomaly_Type'] != 'Normal'].sort_index(ascending=False)
    if anoms.empty:
        st.success(f"✅ No se detectaron anomalías con sensibilidad Z={z_threshold} en este período.")
    else:
        st.markdown(f"Se identificaron **{len(anoms)} días anómalos**. Estos son los más recientes:")
        for idx, row in anoms.head(5).iterrows():
            fecha_str = idx.strftime('%d de %B de %Y')
            tipo = row['Anomaly_Type']
            ret_d = row['Return'] * 100
            z_sc = row['Return_Z']
            emoji = "📉" if tipo == 'Pánico' else "📈"
            color = "#FF416C" if tipo == 'Pánico' else "#FFA07A"
            with st.expander(f"{emoji} {tipo}: {fecha_str} ({ret_d:+.2f}%)"):
                st.markdown(f"<div style='border-left:4px solid {color};padding-left:15px;'>", unsafe_allow_html=True)
                st.markdown(f"**Z-Score:** `{z_sc:+.2f}` | **Volumen anormal:** `{'SÍ' if row['Anomaly_Volume'] else 'NO'}`")
                st.markdown("---")
                st.markdown(get_educational_explanation(tipo, z_sc, selected_ticker))
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# TAB 4: GUÍA DE SESGOS
# ══════════════════════════════════════════════════════════════════════════
with tab_guide:
    st.markdown("<div class='glass-card glow-border-magenta'>", unsafe_allow_html=True)
    st.markdown("### 📘 Biblioteca de Sesgos Cognitivos Financieros")
    st.markdown(
        "<p style='color:#A3AED0;font-size:13px;'>"
        "El cerebro humano está optimizado para sobrevivir en la sabana, no para invertir en mercados modernos. "
        "Estos sesgos son responsables de la mayoría de las pérdidas de inversores individuales. "
        "Conocerlos es el primer paso para superarlos.</p>",
        unsafe_allow_html=True
    )

    bias_data = {
        "panico": {
            "icon": "😱", "color": "#FF416C",
            "titulo": "Pánico Vendedor",
            "que_es": "El impulso incontrolable de vender todo ante una caída del mercado para 'evitar perderlo todo'.",
            "ejemplo": "El S&P 500 cayó un 34% en marzo de 2020 por COVID-19. Los que vendieron en el mínimo y no compraron, perdieron la recuperación del 100% que llegó en los meses siguientes.",
            "como_combatirlo": [
                "Define por escrito tu plan de inversión ANTES de que lleguen las crisis.",
                "Establece un máximo de pérdida tolerable (stop-loss mental) antes de comprar.",
                "Espera siempre 48-72 horas antes de ejecutar cualquier venta de urgencia.",
                "Recuerda: el S&P 500 se recuperó de las 30+ correcciones mayores del siglo XX.",
            ],
        },
        "fomo": {
            "icon": "🚀", "color": "#FFA07A",
            "titulo": "FOMO (Fear of Missing Out)",
            "que_es": "La urgencia de comprar un activo porque está subiendo rápido y 'todos están ganando dinero'.",
            "ejemplo": "Bitcoin subió de $10k a $60k en 2020-2021. Millones compraron en los máximos empujados por el FOMO. En 2022 cayó a $16k, borrando el 73% del valor.",
            "como_combatirlo": [
                "Pregúntate: '¿Compraría esto si NO supiera que subió un 40% este mes?'",
                "Invierte en plazos fijos (DCA mensual) sin importar el precio de ese momento.",
                "La oportunidad perdida nunca es tan cara como la pérdida ejecutada impulsivamente.",
                "Desconéctate de las redes sociales financieras durante semanas de alta euforia.",
            ],
        },
        "overconfidence": {
            "icon": "🎯", "color": "#4FACFE",
            "titulo": "Sobreconfianza (Overconfidence)",
            "que_es": "Creer que tienes la habilidad de predecir el mercado mejor que la media de los participantes.",
            "ejemplo": "El 90% de los gestores activos no supera al índice S&P 500 en períodos de 10+ años. Si los profesionales con equipos de 100 personas fallan, ¿qué nos dice eso?",
            "como_combatirlo": [
                "Registra tus predicciones en un diario y mide su acierto después de 6 meses.",
                "Compara tu rendimiento con el ETF del índice correspondiente.",
                "Por cada argumento de compra, busca activamente 3 argumentos en contra.",
                "Mantén siempre un 20-30% de la cartera en activos indexados como 'control'.",
            ],
        },
        "loss_aversion": {
            "icon": "😰", "color": "#E100FF",
            "titulo": "Aversión a la Pérdida",
            "que_es": "El dolor psicológico de perder 100€ es 2x más intenso que la alegría de ganar 100€ (Kahneman & Tversky). Esto te mantiene atrapado en posiciones perdedoras.",
            "ejemplo": "Compras una acción a 50€. Cae a 30€. No vendes porque 'no has perdido hasta que vendas'. La empresa quiebra y pierdes todo. Si hubieras vendido a 30€, habrías conservado el 60%.",
            "como_combatirlo": [
                "El experimento mental: ¿Comprarías este activo hoy al precio actual? Si no, vende.",
                "El precio de compra es solo relevante para tu fiscalidad, no para el futuro del activo.",
                "Establece reglas automáticas: si cae más del X%, reviso activamente si la tesis cambió.",
                "Recuerda: mantener una posición perdedora tiene un costo de oportunidad real.",
            ],
        },
        "anchoring": {
            "icon": "⚓", "color": "#38EF7D",
            "titulo": "Sesgo de Anclaje",
            "que_es": "Usar un número del pasado (como tu precio de compra) como referencia irracional para decisiones del presente.",
            "ejemplo": "Compraste TSLA a 400$. Ahora está a 200$. Dices: 'No vendo hasta que vuelva a 400€'. El mercado no sabe ni le importa a cuánto compraste.",
            "como_combatirlo": [
                "Ignora conscientemente tu precio de compra en tus decisiones de venta.",
                "Analiza el activo como si lo vieras por primera vez hoy.",
                "La pregunta correcta es: ¿cuánto vale este activo hoy según sus fundamentales?",
                "Tu precio de compra no es un objetivo de precio. Es solo un hecho fiscal.",
            ],
        },
    }

    for key, data in bias_data.items():
        color = data["color"]
        st.markdown(
            f"<div style='border-left:5px solid {color};padding:16px 20px;margin:16px 0;"
            f"background:rgba(15,23,42,0.5);border-radius:0 12px 12px 0;'>",
            unsafe_allow_html=True
        )
        st.markdown(f"## {data['icon']} {data['titulo']}")
        st.markdown(f"**¿Qué es?** {data['que_es']}")
        st.markdown(f"**Ejemplo real:** *{data['ejemplo']}*")
        st.markdown("**Cómo combatirlo:**")
        for point in data["como_combatirlo"]:
            st.markdown(f"- ✅ {point}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<p style='color:#566488;text-align:center;font-size:12px;margin-top:30px;'>"
        "Fuentes: Kahneman & Tversky (1979), Barber & Odean (2000), "
        "Dalbar QAIB 2023, Morningstar Behavioral Finance Research</p>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
