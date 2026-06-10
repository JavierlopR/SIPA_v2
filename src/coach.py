# -*- coding: utf-8 -*-
"""
SIPA v2 - Motor Inteligente de Coaching Psicológico y Financiero
Genera respuestas dinámicas basadas en métricas de mercado reales y sesgos detectados.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ---------------------------------------------------------------------------
# PERFILES DE BROKERS (completo, universal, sin restricción)
# ---------------------------------------------------------------------------
BROKERS_PROFILE = {
    "trade_republic": {
        "name": "Trade Republic",
        "region": "Europa / Internacional",
        "tipo": "Neobroker",
        "comisiones": "1€ por orden manual. DCA automático en ETFs: gratis. Cuenta de efectivo remunerada ~4% TAE.",
        "minimo_deposito": "1€",
        "activos_disponibles": "Acciones, ETFs, derivados, cripto, bonos",
        "pitfall": "FOMO impulsivo",
        "pitfall_detail": (
            "Trade Republic fue diseñado para que comprar sea tan fácil y satisfactorio como comprar en Amazon. "
            "Listas de activos en tendencia, gráficos en verde fluorescente y notificaciones de subidas rápidas "
            "generan el impulso de comprar sin análisis previo. El peligro: entrar en máximos de euforia por pura interfaz."
        ),
        "ventajas": "Comisión flat de 1€, DCA gratuito, cuenta remunerada, interfaz muy limpia.",
        "desventajas": "Oferta limitada de mercados, sin gráficos técnicos avanzados, incentiva el trading emocional.",
        "recomendacion": [
            "Configura un Plan de Inversión mensual automático en ETFs globales: es gratis y elimina la emoción.",
            "Desactiva las notificaciones de precio y listas de 'Trending'. Solo mira tu cartera una vez al mes.",
            "Aprovecha la cuenta de efectivo para tu fondo de emergencia en lugar de dejarlo parado.",
        ],
    },
    "revolut": {
        "name": "Revolut",
        "region": "Global",
        "tipo": "Super-app financiera / broker",
        "comisiones": "Plan gratuito: 1 operación/mes gratis, luego ~0.25% (mín. 1€). Planes de pago: más operaciones incluidas.",
        "minimo_deposito": "1€",
        "activos_disponibles": "Acciones fraccionadas, ETFs, cripto, metales, materias primas",
        "pitfall": "Exceso de confianza / Especulación cripto",
        "pitfall_detail": (
            "Revolut coloca la compra de Bitcoin al lado de la tarjeta de débito y los gastos del supermercado. "
            "Este diseño banaliza la inversión: si comprar cripto es igual de fácil que pagar el café, el cerebro "
            "no registra el riesgo. Resultado: carteras con 60-80% en activos especulativos sin diversificación."
        ),
        "ventajas": "Todo integrado en una sola app, soporte multi-divisa sin comisión, acciones fraccionadas.",
        "desventajas": "Custodia discutible en cripto, límite de operaciones gratis, sin herramientas de análisis.",
        "recomendacion": [
            "Usa la función 'Ahorro en fracciones' para invertir automáticamente el cambio de tus compras diarias.",
            "Si inviertes en cripto, limita esa posición al 5-10% del capital total. Nunca más.",
            "Separa en cuentas distintas: dinero de gastos vs. dinero de inversión a largo plazo.",
        ],
    },
    "scalable_capital": {
        "name": "Scalable Capital",
        "region": "Europa (esp. DACH + España)",
        "tipo": "Neobroker / Robo-advisor",
        "comisiones": "Free Broker: 0.99€/orden. PRIME+: 2.99€/mes → trading ilimitado gratis.",
        "minimo_deposito": "1€",
        "activos_disponibles": "Acciones, ETFs, fondos, derivados, cripto, bonos",
        "pitfall": "Sesgo de sobre-operar (suscripción flat)",
        "pitfall_detail": (
            "El modelo PRIME+ de tarifa plana crea un sesgo poderoso: si pagas 2.99€/mes y cada operación es gratis, "
            "el cerebro presiona para 'aprovechar' haciendo más trades. Más rotación = más errores de timing = peores resultados. "
            "Estudios demuestran que inversores que operan más frecuentemente obtienen peores rentabilidades."
        ),
        "ventajas": "Gran variedad de activos, DCA gratuito, interfaz intuitiva, Robo-advisor disponible.",
        "desventajas": "PRIME+ puede incentivar el sobretrading, derivados complejos accesibles para novatos.",
        "recomendacion": [
            "Si usas PRIME+, comprométete a no hacer más de 2-3 cambios en tu cartera al año.",
            "Activa el Robo-Advisor para dejar que el algoritmo gestione el rebalanceo.",
            "Evita los derivados (ETPs apalancados, opciones) hasta dominar la inversión pasiva básica.",
        ],
    },
    "interactive_brokers": {
        "name": "Interactive Brokers (IBKR)",
        "region": "Global",
        "tipo": "Broker institucional / avanzado",
        "comisiones": "Plan LITE (EEUU): gratis en acciones/ETFs. Plan PRO: desde $0.005/acción. Comisiones ultra-bajas en mercados globales.",
        "minimo_deposito": "0€ (plan IBKR Lite / Global Trader)",
        "activos_disponibles": "Acciones, ETFs, opciones, futuros, forex, bonos, fondos, cripto en 150+ mercados",
        "pitfall": "Parálisis por análisis / Ilusión de control",
        "pitfall_detail": (
            "La terminal TWS de IBKR tiene cientos de indicadores, datos Level-2, scanner de mercado y herramientas cuantitativas. "
            "Para un principiante, esto crea la ilusión de que si analiza suficientes datos podrá predecir el mercado. "
            "Paradoja: más datos mal interpretados generan peores decisiones que menos datos bien entendidos."
        ),
        "ventajas": "Las comisiones más bajas del mundo, acceso a cualquier mercado global, herramientas de nivel institucional.",
        "desventajas": "Curva de aprendizaje muy pronunciada, interfaz abrumadora, no recomendado para empezar.",
        "recomendacion": [
            "Usa la app móvil 'IBKR GlobalTrader' en lugar de la terminal TWS: es mucho más sencilla.",
            "Empieza comprando solo ETFs globales (VT, VWRA, CSPX) hasta dominar el proceso.",
            "No abras cuenta de Margen hasta tener al menos 2 años de experiencia. Nunca operes con dinero prestado.",
        ],
    },
    "robinhood": {
        "name": "Robinhood",
        "region": "EEUU (sin acceso desde Europa)",
        "tipo": "Neobroker gamificado",
        "comisiones": "0€ en acciones, ETFs, opciones y cripto (EEUU). Ingresos por PFOF (venta del flujo de órdenes).",
        "minimo_deposito": "1$",
        "activos_disponibles": "Acciones, ETFs, opciones, cripto, ADRs (solo mercado EEUU)",
        "pitfall": "FOMO extremo / Gamificación",
        "pitfall_detail": (
            "Robinhood fue la primera app en aplicar psicología del juego a la inversión: confeti digital al comprar, "
            "listas de 'Top Movers' que cambian cada minuto, gráficos que parpادean en rojo y verde. "
            "Fue responsable del boom de opciones de novatos en 2021 y múltiples casos de pérdidas devastadoras. "
            "Su modelo de PFOF implica que tu orden se ejecuta peor para que el broker cobre de tu spread."
        ),
        "ventajas": "Sin comisiones, interfaz muy simple, acciones fraccionadas desde 1$.",
        "desventajas": "Solo mercado EEUU, modelo PFOF, fomenta el trading impulsivo, sin herramientas reales de análisis.",
        "recomendacion": [
            "Desactiva todas las notificaciones de precio. Sin excepción.",
            "Ignora las secciones de 'Trending' y 'Top Movers'. Son FOMO puro.",
            "Considera alternativas con mejor ejecución: Fidelity o Schwab para EEUU.",
        ],
    },
    "fintual": {
        "name": "Fintual",
        "region": "Chile / México",
        "tipo": "Robo-advisor regulado",
        "comisiones": "~1% anual de comisión de administración. Sin cobro por depósitos ni retiros.",
        "minimo_deposito": "1 USD / 10 MXN",
        "activos_disponibles": "Fondos mutuos diversificados (gestionados por Fintual) + ETFs subyacentes",
        "pitfall": "Anclaje a rentabilidades pasadas del fondo 'Risky'",
        "pitfall_detail": (
            "El fondo 'Risky' de Fintual (con exposición a tecnológicas) tuvo rentabilidades del 40-80% en 2020-2021. "
            "Muchos inversores se anclaron a esas cifras como expectativa normal. En 2022 cayó 35%. "
            "El sesgo de anclaje a rendimientos pasados excepcionales es una de las fuentes de mayor frustración."
        ),
        "ventajas": "Regulado, diversificado automáticamente, sin mínimos relevantes, muy fácil de usar.",
        "desventajas": "No puedes elegir activos individuales, comisión del 1% puede ser alta a largo plazo.",
        "recomendacion": [
            "Responde el cuestionario de riesgo con total honestidad. Es tu escudo psicológico.",
            "Si usas 'Risky', asegúrate de poder aguantar caídas de 40-50% sin vender.",
            "Complementa con un fondo de liquidez si necesitas acceder al dinero en menos de 3 años.",
        ],
    },
    "gbm": {
        "name": "GBM+",
        "region": "México / LATAM",
        "tipo": "Casa de bolsa / broker digital",
        "comisiones": "0.25% por operación en acciones. Smart Cash (liquidez) sin comisión.",
        "minimo_deposito": "200 MXN",
        "activos_disponibles": "Acciones mexicanas, ETFs en MXN, CETES, fondos GBM, Smart Cash",
        "pitfall": "Aversión a la pérdida por saldos en rojo",
        "pitfall_detail": (
            "GBM+ muestra minusvalías y rendimientos diarios en rojo brillante de forma prominente. "
            "La investigación de Kahneman y Tversky demuestra que perder 100 duele el doble de lo que alegra ganar 100. "
            "Ver tu saldo fluctuar diariamente en rojo dispara este mecanismo y empuja a vender en fondos de ciclos."
        ),
        "ventajas": "Regulado por CNBV, Smart Cash de alta liquidez, CETES para principiantes, soporte en español.",
        "desventajas": "Enfocado en mercado mexicano, comisión por operación puede acumularse si se opera mucho.",
        "recomendacion": [
            "Usa Smart Cash para tu fondo de emergencia: rendimientos de CETES sin riesgo de mercado.",
            "Revisa tu cartera de acciones una vez al mes, no diariamente.",
            "Automatiza inversiones en ETFs indexados con aportaciones quincenales fijas.",
        ],
    },
    "hey_banco": {
        "name": "Hey Banco",
        "region": "México",
        "tipo": "Banco digital / inversión integrada",
        "comisiones": "Sin comisión en pagaré tradicional. Fondos con comisión implícita en el precio de administración.",
        "minimo_deposito": "1 MXN",
        "activos_disponibles": "Pagaré bancario garantizado, fondos de inversión, CETES",
        "pitfall": "Aversión al riesgo extremo / Zona de confort renta fija",
        "pitfall_detail": (
            "Hey Banco promueve su pagaré con rendimientos atractivos y garantizados. Para un principiante, "
            "esto actúa como una 'zona segura' que impide aprender a invertir en renta variable. "
            "A largo plazo, los pagarés no superan la inflación y el dinero pierde poder adquisitivo real."
        ),
        "ventajas": "Sencillo, garantizado por la CNBV, excelente para fondo de emergencia y metas de corto plazo.",
        "desventajas": "Rendimientos que no superan la inflación a largo plazo, no invierte en mercados globales.",
        "recomendacion": [
            "Perfecto para: fondo de emergencia, ahorro a menos de 1 año, dinero que necesitarás pronto.",
            "Inadecuado para: jubilación, metas a más de 5 años, creación de patrimonio real.",
            "Complementa con una cuenta en GBM+ o Fintual para exposición a mercados globales.",
        ],
    },
    "bbva_trader": {
        "name": "BBVA Trader",
        "region": "España / México",
        "tipo": "Broker bancario tradicional",
        "comisiones": "Comisiones variables por mercado (desde 6€ + % sobre valor), tarifas de custodia anuales.",
        "minimo_deposito": "Variable según cuenta",
        "activos_disponibles": "Acciones españolas, europeas, EEUU, ETFs, fondos, warrants",
        "pitfall": "Sesgo de Status Quo + costos invisibles",
        "pitfall_detail": (
            "Muchos inversores eligen BBVA Trader por la tranquilidad de tenerlo todo en su banco tradicional. "
            "Sin embargo, las comisiones de custodia y corretaje son considerablemente más altas que los neobrokers. "
            "Una cartera de 50.000€ puede pagar 300-500€/año solo en custodia, erosionando silenciosamente el rendimiento compuesto."
        ),
        "ventajas": "Seguridad de banco regulado, posibilidad de hablar con un gestor, familiaridad.",
        "desventajas": "Las comisiones más altas del mercado para inversión minorista, tecnología más antigua.",
        "recomendacion": [
            "Calcula exactamente cuánto pagas al año en custodia más corretaje. Puede sorprenderte.",
            "Si tu cartera es mayor de 30.000€, considera mover ETFs a Trade Republic o IBKR.",
            "Usa BBVA para fondos de inversión si ya tienes asesor; para ETFs usa un neobroker.",
        ],
    },
    "openbank": {
        "name": "Openbank / Santander",
        "region": "España",
        "tipo": "Banco digital del Grupo Santander",
        "comisiones": "Sin comisión de custodia en fondos. Robo-advisor: ~0.45-0.85% anual según patrimonio.",
        "minimo_deposito": "10€ (fondos) / 1€ (ahorro)",
        "activos_disponibles": "Fondos de inversión, ETFs, robo-advisor automatizado, depósitos",
        "pitfall": "Efecto disposición + fondos de gestión activa cara",
        "pitfall_detail": (
            "El catálogo de Openbank incluye muchos fondos de gestión activa con TER de 1.5-2.5%. "
            "El 'efecto disposición' hace que los inversores mantengan fondos que rinden poco por confianza en la marca Santander, "
            "en lugar de cambiar a fondos indexados de bajo costo con mejor historial estadístico."
        ),
        "ventajas": "Respaldo del Grupo Santander, buen Robo-advisor, fondos indexados baratos disponibles.",
        "desventajas": "Fácil caer en fondos de gestión activa con comisiones altas si no se mira el TER.",
        "recomendacion": [
            "Busca específicamente fondos Amundi o Vanguard disponibles en el catálogo: tienen TER < 0.2%.",
            "Si quieres simplicidad total, usa el Robo-advisor para metas de largo plazo.",
            "Siempre mira el TER (Total Expense Ratio) antes de contratar cualquier fondo.",
        ],
    },
}

# ---------------------------------------------------------------------------
# MOTOR DE COACHING PSICOLÓGICO CONDUCTUAL
# ---------------------------------------------------------------------------

BIASES_COACHING = {
    "fomo": {
        "explanation": "FOMO (Fear of Missing Out): urgencia de comprar impulsado por ver que otros ganan dinero rápido.",
        "coach_intro": "Detecto que sientes urgencia de actuar antes de 'perderte' algo. Esa sensación es muy humana, pero es también la causa número uno de pérdidas en inversores minoristas.",
        "framework": [
            "**El problema del timing:** Entrar en un activo porque ha subido mucho es exactamente lo contrario de comprar barato. Estás pagando la expectativa de otros, no el valor real.",
            "**La trampa narrativa:** Las historias de ganancias rápidas que oyes (en redes, con amigos) son el sesgo de supervivencia: no oyes a los que perdieron el 80%.",
            "**La solución del tiempo:** Pregúntate: '¿Compraría este activo igual si no supiera que subió un 40% este mes?' Si la respuesta es no, estás comprando emoción, no valor.",
        ],
    },
    "panico": {
        "explanation": "Pánico Vendedor: el impulso de liquidar posiciones ante caídas para 'evitar perderlo todo'.",
        "coach_intro": "Lo que describes suena a pánico de mercado. Es la reacción más natural del mundo, pero también la más costosa estadísticamente.",
        "framework": [
            "**Las pérdidas en papel vs. pérdidas reales:** Una caída del 20% en tu pantalla es una minusvalía latente. Si vendes, la conviertes en pérdida definitiva e irreversible.",
            "**La evidencia histórica:** El S&P 500 ha tenido correcciones del 20%+ en más de 30 ocasiones desde 1928. En todos los casos, superó los máximos anteriores.",
            "**La pregunta correcta:** '¿Cambió algo fundamental en el negocio de esta empresa, o solo cambió el precio?' Si solo cambió el precio, tu tesis sigue vigente.",
        ],
    },
    "overconfidence": {
        "explanation": "Sobreconfianza: creer que tienes información o habilidad suficiente para predecir el mercado mejor que la media.",
        "coach_intro": "Detecto una confianza alta en la decisión. Eso no es malo en sí, pero vale la pena someterla a un test de rigor.",
        "framework": [
            "**El problema de la complejidad:** El precio de un activo incorpora simultáneamente el análisis de millones de inversores, algoritmos institucionales y datos macroeconómicos. Tu ventaja informativa sobre todo eso es estadísticamente marginal.",
            "**El sesgo de confirmación:** Cuando tenemos una idea, buscamos instintivamente información que la confirme y descartamos la que la contradice. Es un fallo cognitivo universal.",
            "**El test de reversión:** ¿Podrías argumentar con igual convicción el caso contrario (que el activo NO va a subir)? Si no, puede que no estés analizando, sino racionalizando.",
        ],
    },
    "loss_aversion": {
        "explanation": "Aversión a la Pérdida: el dolor psicológico de perder es tan intenso que prefieres mantener una posición perdedora indefinidamente.",
        "coach_intro": "Parece que el dolor de las pérdidas latentes está influyendo en tu decisión. Es comprensible, pero es un sesgo que casi siempre lleva a peores resultados.",
        "framework": [
            "**El experimento mental:** Imagina que hoy vendes esa posición y recibes el efectivo. ¿Lo volverías a invertir en ese mismo activo hoy, al precio actual? Si la respuesta es no, solo estás manteniendo por no querer 'admitir' la pérdida.",
            "**El costo de oportunidad invisible:** Cada euro bloqueado en una posición perdedora sin perspectivas es un euro que no está trabajando en algo mejor.",
            "**El precio de compra es irrelevante para el mercado:** El mercado no sabe ni le importa a cuánto compraste. Ese número solo existe en tu mente.",
        ],
    },
    "anchoring": {
        "explanation": "Anclaje: tomar decisiones basándose en un precio de referencia del pasado (tu precio de compra) en lugar del valor actual.",
        "coach_intro": "Identifico que estás usando un precio del pasado como referencia para tomar decisiones del presente. Eso es el sesgo de anclaje.",
        "framework": [
            "**El número mágico que no existe:** Tu precio de compra es información relevante para tu fiscalidad, pero completamente irrelevante para el valor futuro del activo.",
            "**La pregunta correcta:** '¿Cuánto vale este activo HOY en función de sus fundamentales, flujos de caja esperados y perspectivas de sector?' No: '¿Cuándo volverá al precio al que lo compré?'",
            "**La trampa del punto de equilibrio:** Esperar a 'recuperar lo invertido' puede mantenerte atrapado en una posición mediocre mientras otros activos generan retornos reales.",
        ],
    },
    "ninguno": {
        "explanation": "Comportamiento racional: tono equilibrado, sin señales de sesgo emocional dominante.",
        "coach_intro": "Tu mensaje refleja un enfoque bastante racional. Vamos a analizar la situación con detalle.",
        "framework": [
            "**Mantén la disciplina:** La consistencia y la paciencia son las dos variables que más contribuyen al rendimiento de largo plazo, por encima del market timing.",
            "**Revisa tu tesis periódicamente:** Una buena inversión se basa en una tesis fundamentada. Revisarla cada trimestre (no cada día) es una buena práctica.",
            "**Sigue educándote:** El conocimiento compuesto, igual que el interés compuesto, es el mayor activo a largo plazo.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Lógica dinámica de gestión: ¿Vender? ¿Comprar? ¿Aguantar?
# ---------------------------------------------------------------------------

def _build_management_advice(question_type: str, audit: dict, bias: str) -> str:
    """
    Genera consejos de gestión adaptados al tipo de pregunta detectada,
    al estado técnico real del activo y al sesgo del usuario.
    """
    ticker = audit.get("ticker", "el activo")
    nombre = audit.get("nombre", ticker)
    precio = audit.get("precio_actual")
    retorno = audit.get("retorno_hoy")
    rsi = audit.get("rsi_14")
    dist_sma = audit.get("distancia_sma")
    zscore = audit.get("zscore_hoy")
    vol = audit.get("vol_anualizada")
    estado = audit.get("estado_tecnico", "neutral")
    simulado = audit.get("simulado", False)

    # Header con datos técnicos reales
    if simulado or precio is None:
        header = f"\n**{nombre}** — *Datos de mercado no disponibles en este momento*\n"
    else:
        signo = "+" if retorno >= 0 else ""
        header = (
            f"\n**{nombre} ({ticker})**\n"
            f"| Precio Actual | Retorno Hoy | RSI 14d | Dist. SMA50 | Volatilidad anual |\n"
            f"|:---:|:---:|:---:|:---:|:---:|\n"
            f"| **${precio:,.2f}** | **{signo}{retorno:.2f}%** | **{rsi}** | **{dist_sma:+.1f}%** | **{vol:.1f}%** |\n\n"
        )

    # Lógica condicional según pregunta y datos
    advice_lines = []

    if question_type == "vender":
        advice_lines.append("### ¿Debería vender?")
        if bias == "panico":
            advice_lines.append(
                "> ⚠️ **El pánico es el peor consejero para vender.** "
                "Vender durante una caída impulsiva convierte una pérdida temporal en una pérdida permanente."
            )
        if not simulado and rsi is not None:
            if rsi <= 30:
                advice_lines.append(
                    f"- RSI en **{rsi}** (sobreventa): técnicamente, el mercado ya ha 'castigado' este activo "
                    f"de forma exagerada. Vender aquí es vender en el momento estadísticamente más desfavorable."
                )
            elif rsi >= 70:
                advice_lines.append(
                    f"- RSI en **{rsi}** (sobrecompra): si tu objetivo era tomar ganancias, el mercado "
                    f"técnicamente te está dando una oportunidad. Pero considera: ¿cambió tu tesis original de inversión?"
                )
            else:
                advice_lines.append(f"- RSI en **{rsi}** (zona neutral): no hay señal técnica extrema de sobrecompra ni sobreventa.")
        advice_lines.extend([
            "**Las 3 preguntas antes de vender:**",
            "1. ¿Ha cambiado la razón por la que compraste este activo (fundamentales del negocio, tendencia del sector)?",
            "2. ¿Estás vendiendo porque el precio bajó (emoción) o porque tu análisis cambió (racional)?",
            "3. Si vendes hoy, ¿en qué invertirías el dinero y por qué sería mejor que mantener?",
            "",
            "**Alternativas a vender todo:**",
            "- **Recorte parcial:** vende el 20-30% de la posición para reducir exposición sin liquidarla.",
            "- **Stop-loss mental:** define un nivel de precio o pérdida máxima que te resulte tolerable antes de actuar.",
            "- **Espera 48 horas:** las decisiones de venta en caliente suelen revertirse cuando baja la adrenalina.",
        ])

    elif question_type == "comprar":
        advice_lines.append("### ¿Debería comprar?")
        if bias == "fomo":
            advice_lines.append(
                "> ⚠️ **El FOMO es la peor motivación para comprar.** "
                "Si compras porque el activo ya subió mucho, estás pagando la euforia de otros."
            )
        if not simulado and rsi is not None:
            if rsi >= 70:
                advice_lines.append(
                    f"- RSI en **{rsi}** (sobrecompra): el activo ha subido rápido en poco tiempo. "
                    f"Comprar en esta zona implica asumir el riesgo de una corrección técnica próxima."
                )
            elif rsi <= 35:
                advice_lines.append(
                    f"- RSI en **{rsi}** (sobreventa): si tu tesis es sólida, este puede ser un punto "
                    f"de entrada con mejor relación riesgo/recompensa que en momentos de euforia."
                )
            if dist_sma is not None and dist_sma > 15:
                advice_lines.append(
                    f"- El precio está un **{dist_sma:.1f}%** por encima de su SMA50. "
                    f"Comprar lejos de la media móvil reduce tu margen de seguridad."
                )
        advice_lines.extend([
            "**Principios de compra inteligente:**",
            "- **DCA (Dollar Cost Averaging):** en lugar de comprar todo de golpe, divide la compra en 3-6 partes durante los próximos meses. Reduce el riesgo de timing.",
            "- **Tamaño de posición:** ningún activo individual debería superar el 10-15% de tu cartera total si no estás muy familiarizado con él.",
            "- **Horizonte temporal:** ¿Cuánto tiempo estás dispuesto a mantenerlo si cae un 40%? Si la respuesta es 'lo vendería', reconsidera el tamaño de la posición.",
            f"- **Volatilidad actual de {nombre}:** **{vol:.1f}% anualizada**. " + (
                "Alta volatilidad → invertir en múltiples momentos, no de golpe." if vol and vol > 30
                else "Volatilidad moderada."
            ) if not simulado and vol else "",
        ])

    elif question_type == "mantener":
        advice_lines.append("### ¿Debería mantener?")
        advice_lines.extend([
            "Mantener una inversión es una decisión activa, no pasiva. Requiere que tu tesis original siga vigente.",
            "",
            "**Checklist de mantenimiento:**",
            "- [ ] ¿El negocio sigue generando ingresos/crecimiento según lo esperado?",
            "- [ ] ¿Han cambiado significativamente las condiciones del sector?",
            "- [ ] ¿Tu peso en esta posición sigue siendo proporcional a tu tolerancia al riesgo?",
            "- [ ] ¿Llevas más de 6 meses sin revisar tus fundamentos?",
            "",
            "**Sobre el rebalanceo:**",
            "Si el activo ha crecido mucho y ahora ocupa más del 15-20% de tu cartera, considera vender una fracción para restablecer el equilibrio, no por miedo, sino por gestión de riesgo sistemática.",
        ])

    return header + "\n".join([line for line in advice_lines if line is not None])


def _detect_question_type(text: str) -> str:
    """Detecta si el usuario pregunta por vender, comprar, mantener u otro."""
    text_lower = text.lower()
    vender_words = ["vend", "salir", "liquidar", "cerrar posicion", "deshacerme", "quiero salir"]
    comprar_words = ["compr", "entrar", "meter", "invertir", "añadir", "aumentar posicion"]
    mantener_words = ["manten", "aguantar", "quedarme", "seguir", "esperar", "hodl"]

    if any(w in text_lower for w in vender_words):
        return "vender"
    if any(w in text_lower for w in comprar_words):
        return "comprar"
    if any(w in text_lower for w in mantener_words):
        return "mantener"
    return "general"


def generate_coach_response(
    user_text: str,
    detected_intent: str,
    detected_bias: str,
    bias_probs: dict,
    broker_id: str = None,
    openai_key: str = None,
    ticker_audit: dict = None,
) -> dict:
    """
    Genera la respuesta del Coach SIPA v2 de forma dinámica.
    - Integra datos técnicos reales del activo si se detectó un ticker.
    - Aplica lógica de gestión condicional (vender/comprar/mantener).
    - Fusiona el sesgo psicológico con el estado técnico para dar un veredicto único.
    - Opcionalmente enriquece con OpenAI si hay API Key.
    """
    bias_info = BIASES_COACHING.get(detected_bias, BIASES_COACHING["ninguno"])
    question_type = _detect_question_type(user_text)

    # --- Sección 1: Diagnóstico psicológico ---
    bias_section = f"### Diagnóstico Psicológico\n{bias_info['coach_intro']}\n\n"
    framework_lines = "\n".join([f"- {point}" for point in bias_info['framework']])
    bias_section += f"**Marco de análisis:**\n{framework_lines}\n"

    # --- Sección 2: Auditoría técnica del activo (si aplica) ---
    market_section = ""
    if ticker_audit:
        mgmt = _build_management_advice(question_type, ticker_audit, detected_bias)
        alerta = ticker_audit.get("alerta_tecnica", "")
        market_section = f"\n---\n### Análisis Técnico en Tiempo Real\n{mgmt}\n\n"
        if alerta and not ticker_audit.get("simulado"):
            market_section += f"**Señales técnicas adicionales:** {alerta}\n"

    # --- Sección 3: Broker context (si el usuario mencionó uno) ---
    broker_section = ""
    broker_profile = BROKERS_PROFILE.get(broker_id)
    if broker_profile:
        broker_section = (
            f"\n---\n### Tu Plataforma: {broker_profile['name']}\n"
            f"**Trampa de diseño frecuente:** {broker_profile['pitfall']} — {broker_profile['pitfall_detail']}\n\n"
            f"**Comisiones relevantes:** {broker_profile['comisiones']}\n\n"
            f"**Qué hacer en {broker_profile['name']}:**\n"
            + "\n".join([f"- {r}" for r in broker_profile['recomendacion']]) + "\n"
        )

    # --- Ensamblado final ---
    full_response = bias_section + market_section + broker_section

    # --- OpenAI opcional ---
    if openai_key and openai_key.strip().startswith("sk-"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key.strip())

            ticker_ctx = ""
            if ticker_audit and not ticker_audit.get("simulado"):
                ticker_ctx = (
                    f"El modelo de análisis técnico local ha calculado para el activo {ticker_audit['nombre']} ({ticker_audit['ticker']}):\n"
                    f"- Precio: ${ticker_audit['precio_actual']:.2f}\n"
                    f"- RSI 14d: {ticker_audit['rsi_14']}\n"
                    f"- Distancia SMA50: {ticker_audit['distancia_sma']:+.1f}%\n"
                    f"- Z-Score retorno hoy: {ticker_audit['zscore_hoy']:.2f}\n"
                    f"- Estado técnico: {ticker_audit['estado_tecnico']}\n"
                )

            broker_ctx = f"El usuario usa {broker_profile['name']}. " if broker_profile else ""

            system_prompt = (
                "Eres el Coach SIPA v2, un asistente de psicología financiera y finanzas personales de élite. "
                "Eres empático, riguroso, humilde y educativo. Tu misión: mostrar al usuario que predecir el mercado es imposible "
                "y orientarle hacia una gestión racional basada en su perfil de riesgo real.\n\n"
                f"{broker_ctx}"
                f"Nuestros modelos locales detectaron: Sesgo={detected_bias} (probabilidades={bias_probs}), "
                f"Intención={detected_intent}, Tipo de pregunta={question_type}.\n"
                f"{ticker_ctx}"
                "Genera una respuesta en Markdown que:\n"
                "1. Aborde el sesgo emocional del usuario con empatía y argumentos conductuales.\n"
                "2. Integre los datos técnicos reales para dar un veredicto específico, no genérico.\n"
                "3. Si el usuario pregunta por vender/comprar, aplique un framework de gestión de riesgo real.\n"
                "4. Sea honesto: nunca prediga el futuro del precio. Razona con probabilidades y principios.\n"
                "5. Use encabezados Markdown, tablas si aplica, y sea conciso pero profundo."
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                ],
                temperature=0.65,
                max_tokens=900,
            )
            ai_content = response.choices[0].message.content
            return {
                "success": True, "is_llm": True,
                "response": ai_content,
                "probs": bias_probs,
                "question_type": question_type,
            }
        except Exception as e:
            pass  # Fallback al motor local

    return {
        "success": True,
        "is_llm": False,
        "response": full_response,
        "probs": bias_probs,
        "question_type": question_type,
    }


# ---------------------------------------------------------------------------
# Test autónomo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== TEST COACH ===\n")
    casos = [
        ("Compré nvidia hace poco y está cayendo, ¿vendo?", "quiero_vender", "panico", "NVDA"),
        ("Todos están ganando con Bitcoin, ¿entro ahora?", "quiero_comprar", "fomo", "BTC-USD"),
        ("Tengo Apple y quiero saber si mantenerla o comprar más", "consultar_cartera", "ninguno", "AAPL"),
        ("La compré a 50, no vendo hasta que vuelva a 50", "quiero_vender", "anchoring", None),
    ]

    from market_analysis import get_ticker_audit

    for texto, intent, sesgo, ticker in casos:
        audit = get_ticker_audit(ticker) if ticker else None
        resp = generate_coach_response(
            user_text=texto,
            detected_intent=intent,
            detected_bias=sesgo,
            bias_probs={sesgo: 0.85},
            broker_id="trade_republic",
            ticker_audit=audit,
        )
        print(f"PREGUNTA: {texto}")
        print(f"SESGO: {sesgo} | TICKER: {ticker}")
        print(resp["response"][:600])
        print("\n" + "=" * 70 + "\n")
