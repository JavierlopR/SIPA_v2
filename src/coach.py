# -*- coding: utf-8 -*-
"""
SIPA v2 - Motor de Coaching con Gemini AI como cerebro principal.

Arquitectura:
  1. NLP local (scikit-learn) detecta sesgo e intención → contexto
  2. yfinance descarga datos reales del activo mencionado → contexto
  3. Gemini 2.0 Flash recibe TODO el contexto + mensaje original → respuesta inteligente
  4. Fallback a OpenAI si no hay key de Gemini
  5. Fallback a motor de reglas enriquecido si no hay ninguna key

El motor de reglas ahora solo es el ÚLTIMO recurso, no el principal.
"""

import sys
import re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ─────────────────────────────────────────────────────────────────────────────
# PERFILES DE BROKERS
# ─────────────────────────────────────────────────────────────────────────────
BROKERS_PROFILE = {
    "trade_republic": {
        "name": "Trade Republic",
        "region": "Europa / Internacional",
        "tipo": "Neobroker",
        "comisiones": "1€ por orden manual. DCA automático en ETFs gratis. Cuenta remunerada ~4% TAE.",
        "minimo_deposito": "1€",
        "activos_disponibles": "Acciones, ETFs, derivados, cripto, bonos",
        "pitfall": "FOMO impulsivo",
        "pitfall_detail": "Diseñado para que comprar sea tan fácil como Amazon. Listas de trending, gráficos en verde fluorescente y notificaciones de subidas crean el impulso de comprar sin análisis. El peligro: entrar en máximos por pura interfaz.",
        "ventajas": "Comisión flat de 1€, DCA gratuito, cuenta remunerada, interfaz limpia.",
        "desventajas": "Sin gráficos técnicos avanzados, incentiva el trading emocional.",
        "recomendacion": [
            "Configura un Plan de Inversión mensual automático en ETFs globales: es gratis y elimina la emoción.",
            "Desactiva las notificaciones de precio y listas de 'Trending'.",
            "Aprovecha la cuenta de efectivo para tu fondo de emergencia.",
        ],
    },
    "revolut": {
        "name": "Revolut",
        "region": "Global",
        "tipo": "Super-app financiera / broker",
        "comisiones": "Plan gratuito: 1 operación/mes gratis, luego ~0.25% (mín. 1€).",
        "minimo_deposito": "1€",
        "activos_disponibles": "Acciones fraccionadas, ETFs, cripto, metales",
        "pitfall": "Especulación cripto banalizada",
        "pitfall_detail": "Revolut pone la compra de Bitcoin al lado de pagar el café. Este diseño banaliza el riesgo. Resultado: carteras con 60-80% en activos especulativos.",
        "ventajas": "Todo integrado, multi-divisa, acciones fraccionadas.",
        "desventajas": "Límite de operaciones gratis, sin herramientas de análisis serias.",
        "recomendacion": [
            "Limita la exposición a cripto al 5-10% del capital. Sin excepción.",
            "Separa cuentas: dinero de gastos vs. dinero de inversión.",
            "Usa la función de ahorro automático en fracciones.",
        ],
    },
    "scalable_capital": {
        "name": "Scalable Capital",
        "region": "Europa (DACH + España)",
        "tipo": "Neobroker / Robo-advisor",
        "comisiones": "Free: 0.99€/orden. PRIME+: 2.99€/mes → trading ilimitado gratis.",
        "minimo_deposito": "1€",
        "activos_disponibles": "Acciones, ETFs, fondos, derivados, cripto",
        "pitfall": "Sobreoperar por suscripción flat",
        "pitfall_detail": "PRIME+ crea el sesgo de 'aprovechar' haciendo más trades. Más rotación = más errores de timing = peores resultados.",
        "ventajas": "Gran variedad, DCA gratuito, Robo-advisor disponible.",
        "desventajas": "PRIME+ incentiva el sobretrading.",
        "recomendacion": [
            "Con PRIME+, comprométete a no más de 2-3 cambios de cartera al año.",
            "Activa el Robo-Advisor para el rebalanceo automático.",
            "Evita los ETPs apalancados hasta dominar la inversión pasiva.",
        ],
    },
    "interactive_brokers": {
        "name": "Interactive Brokers (IBKR)",
        "region": "Global",
        "tipo": "Broker institucional / avanzado",
        "comisiones": "LITE (EEUU): 0€ en acciones/ETFs. PRO: desde $0.005/acción.",
        "minimo_deposito": "0€",
        "activos_disponibles": "Acciones, ETFs, opciones, futuros, forex, bonos, 150+ mercados",
        "pitfall": "Parálisis por análisis / Ilusión de control",
        "pitfall_detail": "La terminal TWS tiene cientos de indicadores. Para un principiante, más datos mal interpretados generan peores decisiones.",
        "ventajas": "Las comisiones más bajas del mundo, acceso a cualquier mercado global.",
        "desventajas": "Curva de aprendizaje muy pronunciada, interfaz abrumadora.",
        "recomendacion": [
            "Usa la app 'IBKR GlobalTrader' en lugar de TWS.",
            "Empieza solo con ETFs globales (VWRA, CSPX).",
            "Nunca abras cuenta de Margen hasta tener 2+ años de experiencia.",
        ],
    },
    "robinhood": {
        "name": "Robinhood",
        "region": "EEUU",
        "tipo": "Neobroker gamificado",
        "comisiones": "0$ en acciones, ETFs, opciones y cripto (EEUU).",
        "minimo_deposito": "1$",
        "activos_disponibles": "Acciones, ETFs, opciones, cripto (solo EEUU)",
        "pitfall": "Gamificación extrema / FOMO",
        "pitfall_detail": "Confeti digital al comprar, listas de Top Movers cada minuto. Responsable del boom de opciones de novatos en 2021 con pérdidas devastadoras.",
        "ventajas": "Sin comisiones, interfaz simple, acciones fraccionadas desde 1$.",
        "desventajas": "Solo EEUU, modelo PFOF, fomenta el trading impulsivo.",
        "recomendacion": [
            "Desactiva TODAS las notificaciones de precio.",
            "Ignora 'Trending' y 'Top Movers' completamente.",
            "Considera alternativas: Fidelity o Schwab para EEUU.",
        ],
    },
    "fintual": {
        "name": "Fintual",
        "region": "Chile / México",
        "tipo": "Robo-advisor regulado",
        "comisiones": "~1% anual de administración.",
        "minimo_deposito": "1 USD / 10 MXN",
        "activos_disponibles": "Fondos mutuos diversificados (gestionados por Fintual)",
        "pitfall": "Anclaje a rentabilidades pasadas del fondo 'Risky'",
        "pitfall_detail": "'Risky' tuvo +40-80% en 2020-2021. Muchos se anclaron a esas cifras. En 2022 cayó 35%. El sesgo de anclaje a rendimientos pasados genera frustración.",
        "ventajas": "Regulado, diversificado automáticamente, muy fácil de usar.",
        "desventajas": "No puedes elegir activos individuales, comisión del 1% puede ser alta.",
        "recomendacion": [
            "Responde el cuestionario de riesgo con total honestidad.",
            "Si usas 'Risky', asegúrate de aguantar caídas del 40-50%.",
            "Complementa con fondo de liquidez para metas a menos de 3 años.",
        ],
    },
    "gbm": {
        "name": "GBM+",
        "region": "México / LATAM",
        "tipo": "Casa de bolsa / broker digital",
        "comisiones": "0.25% por operación en acciones. Smart Cash sin comisión.",
        "minimo_deposito": "200 MXN",
        "activos_disponibles": "Acciones MX, ETFs en MXN, CETES, fondos GBM, Smart Cash",
        "pitfall": "Aversión a la pérdida por saldos en rojo",
        "pitfall_detail": "GBM+ muestra minusvalías en rojo brillante. La investigación de Kahneman demuestra que perder 100 duele 2x más que alegra ganar 100. Ver el saldo rojo empuja a vender en fondos de ciclos.",
        "ventajas": "Regulado CNBV, Smart Cash de alta liquidez, CETES, soporte en español.",
        "desventajas": "Enfocado en mercado mexicano, comisión por operación acumulable.",
        "recomendacion": [
            "Usa Smart Cash para tu fondo de emergencia.",
            "Revisa tu cartera de acciones una vez al mes, no diariamente.",
            "Automatiza inversiones en ETFs indexados quincenalmente.",
        ],
    },
    "hey_banco": {
        "name": "Hey Banco",
        "region": "México",
        "tipo": "Banco digital / inversión integrada",
        "comisiones": "Sin comisión en pagaré. Fondos con comisión implícita.",
        "minimo_deposito": "1 MXN",
        "activos_disponibles": "Pagaré bancario, fondos, CETES",
        "pitfall": "Zona de confort renta fija",
        "pitfall_detail": "El pagaré garantizado impide aprender a invertir en renta variable. A largo plazo, los pagarés no superan la inflación.",
        "ventajas": "Sencillo, garantizado, ideal para fondo de emergencia.",
        "desventajas": "No supera la inflación a largo plazo, sin mercados globales.",
        "recomendacion": [
            "Perfecto para fondo de emergencia y metas a menos de 1 año.",
            "Inadecuado para jubilación o metas a más de 5 años.",
            "Complementa con GBM+ o Fintual para mercados globales.",
        ],
    },
    "bbva_trader": {
        "name": "BBVA Trader",
        "region": "España / México",
        "tipo": "Broker bancario tradicional",
        "comisiones": "Desde 6€ + % sobre valor, tarifas de custodia anuales.",
        "minimo_deposito": "Variable",
        "activos_disponibles": "Acciones españolas, europeas, EEUU, ETFs, fondos, warrants",
        "pitfall": "Costos invisibles / Status Quo",
        "pitfall_detail": "Las comisiones de custodia son considerablemente más altas que los neobrokers. Una cartera de 50.000€ puede pagar 300-500€/año solo en custodia, erosionando silenciosamente el rendimiento.",
        "ventajas": "Seguridad bancaria, posibilidad de hablar con gestor.",
        "desventajas": "Las comisiones más altas del mercado para inversión minorista.",
        "recomendacion": [
            "Calcula exactamente cuánto pagas al año en custodia + corretaje.",
            "Si tienes más de 30.000€, considera mover ETFs a Trade Republic o IBKR.",
            "Usa BBVA para fondos con asesor; para ETFs, neobroker.",
        ],
    },
    "openbank": {
        "name": "Openbank / Santander",
        "region": "España",
        "tipo": "Banco digital del Grupo Santander",
        "comisiones": "Sin custodia en fondos. Robo-advisor: ~0.45-0.85% anual.",
        "minimo_deposito": "10€",
        "activos_disponibles": "Fondos de inversión, ETFs, robo-advisor, depósitos",
        "pitfall": "Efecto disposición + fondos de gestión activa cara",
        "pitfall_detail": "El catálogo incluye fondos de gestión activa con TER 1.5-2.5%. El 'efecto disposición' hace que inversores mantengan fondos que rinden poco por confianza en la marca.",
        "ventajas": "Respaldo Santander, buen Robo-advisor, fondos indexados disponibles.",
        "desventajas": "Fácil caer en fondos de gestión activa con comisiones altas.",
        "recomendacion": [
            "Busca fondos Amundi o Vanguard con TER < 0.2%.",
            "Usa el Robo-advisor para metas de largo plazo.",
            "Siempre mira el TER antes de contratar cualquier fondo.",
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# SESGOS (solo para el radar visual, no para generar respuestas plantilla)
# ─────────────────────────────────────────────────────────────────────────────
BIASES_COACHING = {
    "fomo": {
        "explanation": "FOMO (Fear of Missing Out): urgencia de comprar impulsado por ver que otros ganan dinero rápido.",
        "coach_intro": "Detecto señales de FOMO en tu mensaje.",
        "framework": [],
    },
    "panico": {
        "explanation": "Pánico Vendedor: el impulso de liquidar posiciones ante caídas para 'evitar perderlo todo'.",
        "coach_intro": "Detecto señales de pánico vendedor.",
        "framework": [],
    },
    "overconfidence": {
        "explanation": "Sobreconfianza: creer que puedes predecir el mercado mejor que la media.",
        "coach_intro": "Detecto señales de exceso de confianza.",
        "framework": [],
    },
    "loss_aversion": {
        "explanation": "Aversión a la Pérdida: el dolor de perder es tan intenso que mantienes posiciones perdedoras.",
        "coach_intro": "Detecto aversión a la pérdida.",
        "framework": [],
    },
    "anchoring": {
        "explanation": "Anclaje: tomar decisiones basándose en un precio de referencia del pasado.",
        "coach_intro": "Detecto sesgo de anclaje.",
        "framework": [],
    },
    "ninguno": {
        "explanation": "Comportamiento racional: tono equilibrado, sin señales de sesgo emocional dominante.",
        "coach_intro": "Tu mensaje es racional.",
        "framework": [],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# CONSTRUCTOR DE CONTEXTO PARA EL LLM
# ─────────────────────────────────────────────────────────────────────────────

def _build_llm_context(
    user_text: str,
    detected_intent: str,
    detected_bias: str,
    bias_probs: dict,
    ticker_audit: dict | None,
    broker_id: str | None,
    exp_level: str = "Principiante",
) -> str:
    """
    Construye un bloque de contexto estructurado para enviar al LLM
    junto al mensaje del usuario. Este contexto transforma la respuesta
    de genérica a específica y fundamentada.
    """
    lines = []

    # ── Perfil del usuario ──────────────────────────────────────────────
    lines.append(f"PERFIL DEL USUARIO:")
    lines.append(f"- Nivel de experiencia: {exp_level}")
    lines.append(f"- Sesgo psicológico detectado por ML: {detected_bias} "
                 f"(probabilidades: {', '.join(f'{k}={v:.0%}' for k,v in sorted(bias_probs.items(), key=lambda x:-x[1])[:3])})")
    lines.append(f"- Intención detectada: {detected_intent}")

    # ── Datos de mercado ────────────────────────────────────────────────
    if ticker_audit:
        nombre = ticker_audit.get("nombre", ticker_audit.get("ticker", "?"))
        ticker = ticker_audit.get("ticker", "?")
        if ticker_audit.get("simulado") or ticker_audit.get("precio_actual") is None:
            lines.append(f"\nACTIVO MENCIONADO: {nombre} ({ticker})")
            lines.append("- Estado: datos en tiempo real no disponibles (posible ticker desconocido o fallo de red)")
        else:
            lines.append(f"\nDAILY MARKET AUDIT — {nombre} ({ticker}):")
            lines.append(f"- Precio actual: ${ticker_audit['precio_actual']:,.4f}")
            retorno = ticker_audit.get('retorno_hoy', 0)
            signo = "+" if retorno >= 0 else ""
            lines.append(f"- Retorno hoy: {signo}{retorno:.3f}%")
            lines.append(f"- RSI 14 días: {ticker_audit['rsi_14']} "
                         f"({'SOBRECOMPRADO' if ticker_audit['rsi_14'] >= 65 else 'SOBREVENDIDO' if ticker_audit['rsi_14'] <= 35 else 'NEUTRAL'})")
            lines.append(f"- Distancia a SMA50: {ticker_audit['distancia_sma']:+.2f}%")
            lines.append(f"- Z-Score retorno hoy: {ticker_audit['zscore_hoy']:+.3f} "
                         f"({'estadísticamente extremo' if abs(ticker_audit['zscore_hoy']) > 2.5 else 'normal'})")
            lines.append(f"- Volatilidad anualizada (21d): {ticker_audit['vol_anualizada']:.1f}%")
            lines.append(f"- Estado técnico: {ticker_audit['estado_tecnico'].upper()}")
            lines.append(f"- Diagnóstico técnico: {ticker_audit['alerta_tecnica']}")

    # ── Info del broker ─────────────────────────────────────────────────
    broker_profile = BROKERS_PROFILE.get(broker_id) if broker_id else None
    if broker_profile:
        lines.append(f"\nPLATAFORMA DEL USUARIO: {broker_profile['name']}")
        lines.append(f"- Comisiones: {broker_profile['comisiones']}")
        lines.append(f"- Trampa de diseño frecuente: {broker_profile['pitfall']} — {broker_profile['pitfall_detail']}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# SISTEMA PROMPT DEL CONSEJERO FINANCIERO
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Eres SIPA, un consejero financiero personal de élite con especialización en psicología conductual del inversor. Piensas y respondes como un asesor financiero experimentado que además entiende profundamente la psicología humana.

TU PERSONALIDAD:
- Eres directo, honesto y empático. No das rodeos.
- Hablas como un amigo que sabe de finanzas, no como un manual académico.
- Cuando alguien comete un error, lo dices con claridad pero sin juzgar.
- Eres específico: usas los datos reales del mercado que te proporcionan para dar opiniones concretas.
- Nunca predices el futuro del precio con certeza. Razonas con probabilidades y principios.
- Adaptas tu nivel de tecnicismo al perfil del usuario.

LO QUE HACES:
1. Respondes la pregunta concreta del usuario (no la ignores por el sesgo).
2. Si hay datos técnicos reales del activo (RSI, SMA, etc.), los integras naturalmente en tu respuesta como haría un analista.
3. Identificas sesgos emocionales y los nombras de forma educativa, no condescendiente.
4. Das pasos de acción concretos y accionables, no consejos genéricos.
5. Si el activo es desconocido o no tienes datos, dices que no puedes analizarlo con datos y explicas qué factores buscarías.
6. Si preguntan por brokers, comparas con contexto real de costos y perfil del usuario.

LO QUE NUNCA HACES:
- Responder con plantillas genéricas que podrían servir para cualquier pregunta.
- Repetir siempre el mismo bloque de texto independientemente del contexto.
- Decir "consulta a un asesor financiero" como única respuesta (tú ERES el asesor).
- Ignorar los datos de mercado reales que te proporcionan.
- Dar respuestas de más de 400 palabras (ser conciso es ser profesional).

FORMATO:
- Responde en español conversacional.
- Usa párrafos cortos, no bloques de texto.
- Puedes usar negritas para enfatizar puntos clave.
- Si das una lista, que sean 3-4 puntos máximo, no 10.
- Sé humano: puedes usar expresiones coloquiales cuando el tono lo permita.
"""


# ─────────────────────────────────────────────────────────────────────────────
# MOTOR DE FALLBACK (reglas, solo si no hay ninguna API key)
# ─────────────────────────────────────────────────────────────────────────────

def _fallback_rules_response(
    user_text: str,
    detected_bias: str,
    ticker_audit: dict | None,
    broker_id: str | None,
) -> str:
    """
    Motor de último recurso. Genera una respuesta mínima estructurada.
    Sin API key, no puede ser conversacional — informa al usuario.
    """
    msg_parts = []

    # Aviso sobre la limitación
    msg_parts.append(
        "⚠️ **Sin API Key configurada** — Las respuestas en modo local son limitadas. "
        "Para obtener análisis conversacionales completos, añade tu **Gemini API Key** (gratuita) en el panel lateral.\n\n"
        "---\n"
    )

    # Análisis técnico si hay datos
    if ticker_audit and not ticker_audit.get("simulado") and ticker_audit.get("precio_actual"):
        nombre = ticker_audit["nombre"]
        ret = ticker_audit["retorno_hoy"]
        rsi = ticker_audit["rsi_14"]
        signo = "+" if ret >= 0 else ""
        msg_parts.append(f"**{nombre}** — Precio: ${ticker_audit['precio_actual']:,.2f} ({signo}{ret:.2f}% hoy)")
        msg_parts.append(f"RSI 14d: **{rsi}** → {ticker_audit['estado_tecnico'].upper()}")
        msg_parts.append(f"{ticker_audit['alerta_tecnica']}\n")

    # Sesgo detectado
    bias_msgs = {
        "panico": "El análisis NLP detecta **pánico vendedor** en tu mensaje. Históricamente, vender en caídas extremas es la decisión más costosa que puede tomar un inversor.",
        "fomo": "El análisis NLP detecta **FOMO** en tu mensaje. Comprar por urgencia de no perderte algo raramente termina bien.",
        "overconfidence": "El análisis NLP detecta **sobreconfianza** en tu mensaje. Los mercados han arruinado a traders que creyeron poder predecirlos.",
        "loss_aversion": "El análisis NLP detecta **aversión a la pérdida**. Las pérdidas en papel no son reales hasta que vendes.",
        "anchoring": "El análisis NLP detecta **sesgo de anclaje**. El precio al que compraste no determina el valor actual del activo.",
        "ninguno": "No se detectan sesgos emocionales dominantes. Tu enfoque parece racional.",
    }
    msg_parts.append(bias_msgs.get(detected_bias, ""))

    # Info de broker
    bp = BROKERS_PROFILE.get(broker_id) if broker_id else None
    if bp:
        msg_parts.append(f"\n**{bp['name']}:** {bp['comisiones']}")

    return "\n".join(msg_parts)


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL: generate_coach_response
# ─────────────────────────────────────────────────────────────────────────────

def generate_coach_response(
    user_text: str,
    detected_intent: str,
    detected_bias: str,
    bias_probs: dict,
    broker_id: str = None,
    gemini_key: str = None,
    openai_key: str = None,
    ticker_audit: dict = None,
    exp_level: str = "Principiante",
    chat_history: list = None,
) -> dict:
    """
    Genera la respuesta del Coach SIPA v2.
    Jerarquía: Gemini → OpenAI → Fallback local.

    Args:
        chat_history: lista de dicts [{role: 'user'|'model', parts: [str]}]
                      para mantener contexto de conversación en Gemini.
    """
    # Construir el contexto enriquecido
    context_block = _build_llm_context(
        user_text=user_text,
        detected_intent=detected_intent,
        detected_bias=detected_bias,
        bias_probs=bias_probs,
        ticker_audit=ticker_audit,
        broker_id=broker_id,
        exp_level=exp_level,
    )

    # ── 1. GEMINI (principal) ────────────────────────────────────────────
    if gemini_key and gemini_key.strip().startswith("AI"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key.strip())

            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                system_instruction=SYSTEM_PROMPT,
                generation_config={
                    "temperature": 0.75,
                    "max_output_tokens": 700,
                    "top_p": 0.95,
                },
            )

            # Mensaje enriquecido con contexto
            full_user_message = (
                f"[CONTEXTO ANALÍTICO — procesa esto internamente, no lo repitas en tu respuesta]\n"
                f"{context_block}\n"
                f"[FIN DEL CONTEXTO]\n\n"
                f"PREGUNTA DEL USUARIO: {user_text}"
            )

            # Mantener historial de conversación si existe
            if chat_history and len(chat_history) > 0:
                history_gemini = []
                for msg in chat_history[-6:]:  # últimos 3 intercambios
                    if msg.get("role") in ("user", "model"):
                        history_gemini.append(msg)
                chat = model.start_chat(history=history_gemini)
            else:
                chat = model.start_chat(history=[])

            response = chat.send_message(full_user_message)
            ai_text = response.text

            return {
                "success": True,
                "is_llm": True,
                "llm_engine": "Gemini 2.0 Flash",
                "response": ai_text,
                "probs": bias_probs,
            }
        except Exception as e:
            error_msg = str(e)
            # Key inválida
            if "API_KEY" in error_msg.upper() or "INVALID" in error_msg.upper():
                return {
                    "success": False,
                    "is_llm": False,
                    "llm_engine": "error",
                    "response": f"❌ La API Key de Gemini no es válida: `{error_msg[:120]}`",
                    "probs": bias_probs,
                }
            # Otros errores → seguir al siguiente motor

    # ── 2. OPENAI (fallback) ─────────────────────────────────────────────
    if openai_key and openai_key.strip().startswith("sk-"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key.strip())

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            # Incluir historial si existe
            if chat_history:
                for msg in chat_history[-6:]:
                    role = "assistant" if msg.get("role") == "model" else msg.get("role", "user")
                    content = msg.get("parts", [""])[0] if msg.get("parts") else ""
                    if content and role in ("user", "assistant"):
                        messages.append({"role": role, "content": content})

            messages.append({
                "role": "user",
                "content": (
                    f"[CONTEXTO]\n{context_block}\n[FIN CONTEXTO]\n\n"
                    f"PREGUNTA: {user_text}"
                )
            })

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.72,
                max_tokens=700,
            )
            ai_text = resp.choices[0].message.content
            return {
                "success": True,
                "is_llm": True,
                "llm_engine": "GPT-4o-mini",
                "response": ai_text,
                "probs": bias_probs,
            }
        except Exception:
            pass

    # ── 3. FALLBACK LOCAL ────────────────────────────────────────────────
    fallback_text = _fallback_rules_response(
        user_text=user_text,
        detected_bias=detected_bias,
        ticker_audit=ticker_audit,
        broker_id=broker_id,
    )
    return {
        "success": True,
        "is_llm": False,
        "llm_engine": "local",
        "response": fallback_text,
        "probs": bias_probs,
    }


# ─────────────────────────────────────────────────────────────────────────────
# TEST
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Solo prueba el contexto sin LLM
    from market_analysis import get_ticker_audit

    audit = get_ticker_audit("NVDA")
    ctx = _build_llm_context(
        user_text="Compré nvidia y está cayendo, ¿vendo?",
        detected_intent="quiero_vender",
        detected_bias="panico",
        bias_probs={"panico": 0.85, "fomo": 0.08},
        ticker_audit=audit,
        broker_id="trade_republic",
    )
    print("=== CONTEXTO GENERADO PARA EL LLM ===")
    print(ctx)
    print("\n=== TEST SIN KEY (fallback) ===")
    resp = generate_coach_response(
        user_text="Compré nvidia y está cayendo, ¿vendo?",
        detected_intent="quiero_vender",
        detected_bias="panico",
        bias_probs={"panico": 0.85},
        ticker_audit=audit,
    )
    print(resp["response"])
