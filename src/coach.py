# -*- coding: utf-8 -*-
"""
SIPA v2 - Motor Experto de Psicología Financiera e Integración Híbrida LLM
Módulo que contiene perfiles psicológicos de brokers, estrategias educativas
antisesgos y la lógica híbrida de generación de respuestas.
"""

import sys
import os

# Forzar codificación UTF-8 para consola en Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Diccionario completo de perfiles de brokers y análisis conductual de su UX
BROKERS_PROFILE = {
    "gbm": {
        "name": "GBM+ (México)",
        "region": "LATAM / México",
        "description": "Una de las casas de bolsa más grandes de México, popular por sus estrategias de Wealth Management y trading.",
        "comisiones": "Comisión de corretaje fija de 0.25% por operación (compra/venta) de acciones. Fondos propios con comisiones variables.",
        "pitfall": "Aversión a la Pérdida (Loss Aversion) e Indecisión",
        "pitfall_detail": (
            "El diseño de GBM+ muestra minusvalías y variaciones de portafolio diarias en colores rojos intensos destacados. "
            "Para un principiante, ver su capital fluctuar constantemente en rojo genera una fuerte respuesta de dolor psicológico "
            "(la aversión a la pérdida duele el doble de lo que agrada una ganancia). Esto suele presionar al inversor a vender "
            "en pánico durante correcciones de mercado o a paralizarse por el miedo, evitando aportaciones recurrentes."
        ),
        "onboarding": [
            "1. **Crea una estrategia de 'Smart Cash':** Utiliza este fondo de liquidez diaria de bajo riesgo para tu fondo de emergencia antes de comprar acciones.",
            "2. **Automatiza tus compras:** Programa aportaciones quincenales a ETFs globales (como IVVPESO o SPLG) para evitar decidir en base al pánico diario.",
            "3. **Filtra el ruido del rojo:** Intenta revisar tu saldo solo una vez al mes. Las fluctuaciones diarias no definen tu éxito a 10 años."
        ]
    },
    "trade_republic": {
        "name": "Trade Republic (Europa)",
        "region": "España / Europa",
        "description": "Neobroker alemán líder en Europa, famoso por sus planes de inversión gratuitos y su cuenta de efectivo remunerada.",
        "comisiones": "Tarifa plana de 1€ por operación individual. Planes de inversión automática (DCA) en ETFs y acciones 100% gratuitos.",
        "pitfall": "FOMO (Miedo a quedarse fuera) e Impulsividad",
        "pitfall_detail": (
            "Su interfaz es extremadamente limpia y minimalista, similar a una app de redes sociales o juegos. Alienta al usuario "
            "mostrando activos populares con subidas exponenciales en pestañas destacadas y ofrece compras en un clic. Esto minimiza "
            "la fricción de compra y promueve decisiones impulsivas basadas en ver qué activos suben hoy, alimentando el FOMO."
        ),
        "onboarding": [
            "1. **Aprovecha el DCA gratuito:** Configura un 'Plan de Inversión' semanal o mensual en un ETF global diversificado como el MSCI World. Es gratis y elimina el impulso emocional.",
            "2. **Usa el interés de tu efectivo:** Deja tus ahorros a corto plazo acumulando la tasa de interés anual de la cuenta de efectivo sin arriesgarlos en bolsa.",
            "3. **Apaga notificaciones de mercado:** Desactiva las alertas de subidas repentinas que te empujan a realizar trading impulsivo."
        ]
    },
    "revolut": {
        "name": "Revolut (Global)",
        "region": "Global / España / LATAM",
        "description": "Super-app financiera que ofrece cuentas multidivisa, transferencias internacionales y compra integrada de acciones, metales y cripto.",
        "comisiones": "Operaciones gratuitas limitadas según tu plan mensual (de 1 a 10 gratis), luego comisión de ~0.25% o mínima de 1€/$. Custodia mensual de 0.12% anual.",
        "pitfall": "Exceso de Confianza (Overconfidence) y Especulación Cripto",
        "pitfall_detail": (
            "Revolut integra la inversión en tu pantalla principal al lado de tus gastos de supermercado. Ofrece comprar Bitcoin o acciones "
            "con un solo toque usando el cambio sobrante. Esta excesiva facilidad de acceso diluye la seriedad de la inversión, haciendo "
            "creer al principiante que invertir es solo un juego de azar divertido, induciendo a un exceso de confianza y a sobre-operar."
        ),
        "onboarding": [
            "1. **Usa el 'Cambio de Repuesto':** Puedes configurar que tus compras diarias redondeen al euro y se inviertan de forma pasiva en ETFs de bajo costo.",
            "2. **Separa tu dinero:** No mezcles tu saldo de gastos corrientes con tu dinero destinado a inversión a largo plazo.",
            "3. **Limita las Criptomonedas:** Si decides comprar cripto activos por su extrema sencillez en la app, que no superen el 5% de tu capital total."
        ]
    },
    "scalable_capital": {
        "name": "Scalable Capital (Europa)",
        "region": "España / Europa",
        "description": "Neobroker y robo-advisor líder en Alemania, que permite planes DCA gratuitos e inversión en derivados y cripto.",
        "comisiones": "Modelo 'Free Broker' (0.99€ por orden, DCA gratis) o 'PRIME+' (tarifa plana de 2.99€/mes para trading ilimitado gratis).",
        "pitfall": "Ilusión de Control y Sesgo de Sobre-operar",
        "pitfall_detail": (
            "El modelo de suscripción PRIME+ con tarifa plana de trading genera en el usuario principiante el impulso psicológico de "
            "realizar operaciones constantemente para 'aprovechar y desquitar' la mensualidad. Esto incrementa la rotación de cartera, "
            "provocando malas decisiones y subestimando los costos invisibles del spread entre compra y venta."
        ),
        "onboarding": [
            "1. **Mantente PRIME si automatizas:** Si usas la tarifa PRIME+, enfócate en acumular capital a largo plazo en planes DCA diversificados, no en hacer trading diario.",
            "2. **Cuidado con los apalancados:** La app facilita operar con derivados (derivados financieros). Evítalos por completo al iniciar; multiplican tus pérdidas exponencialmente.",
            "3. **Invierte en la cuenta remunerada:** Coloca la liquidez de corto plazo a generar rendimientos seguros en su tasa PRIME+."
        ]
    },
    "interactive_brokers": {
        "name": "Interactive Brokers (Global)",
        "region": "Global / EEUU / LATAM",
        "description": "Una de las plataformas de inversión más completas e institucionales del mundo, apta para inversores sofisticados.",
        "comisiones": "Comisiones ultrabajas (centavos por acción) pero estructura densa y tarifas por inactividad removidas.",
        "pitfall": "Parálisis por Análisis e Ilusión de Control",
        "pitfall_detail": (
            "La abrumadora cantidad de información técnica, gráficos en tiempo real, terminales de trading (TWS) y opciones exóticas "
            "puede asustar y paralizar a un principiante. Al mismo tiempo, tener acceso a herramientas profesionales crea la ilusión "
            "de que analizando datos densos se puede predecir el futuro del precio, incentivando la especulación."
        ),
        "onboarding": [
            "1. **Usa el modo 'Portal Web' o App Simple:** Evita la terminal avanzada Trader Workstation (TWS) inicialmente. Utiliza la interfaz web simplificada.",
            "2. **Elige ETFs globales de bajo costo:** Busca fondos acumulativos como VWRA o CSPX para armar una cartera diversificada a décadas.",
            "3. **Ignora el apalancamiento (Margen):** No abras una cuenta de margen; mantén tu cuenta en tipo 'Cash' (efectivo) para no arriesgar más dinero del que posees."
        ]
    },
    "fintual": {
        "name": "Fintual (Chile / México)",
        "region": "LATAM / México / Chile",
        "description": "Plataforma automatizada (Robo-advisor) regulada que simplifica la inversión en fondos mutuos diversificados según tu nivel de riesgo.",
        "comisiones": "Comisión fija baja de administración anual (alrededor del 1% anual), sin costos por depósito o retiro de capital.",
        "pitfall": "Sesgo de Anclaje (Anchoring) ante los Fondos Temáticos",
        "pitfall_detail": (
            "Fintual utiliza nombres lúdicos y accesibles para sus fondos ('Very Conservative', 'Conservative', 'Moderate', 'Risky'). "
            "Al simplificar tanto el riesgo bajo apodos amigables, los principiantes a veces se anclan a las rentabilidades pasadas espectaculares "
            "del fondo 'Risky' (que invierte en tecnológicas), asumiendo un riesgo que no toleran psicológicamente ante caídas normales."
        ),
        "onboarding": [
            "1. **Define tus plazos reales:** Si vas a necesitar el dinero en menos de un año, mantente estrictamente en 'Very Conservative' o su fondo de liquidez.",
            "2. **Responde con honestidad el test:** No intentes aparentar mayor tolerancia al riesgo en su cuestionario inicial; está diseñado para protegerte.",
            "3. **Inversión pasiva pura:** Fintual funciona excelente si programas un depósito automático y dejas que los algoritmos rebalanceen por ti."
        ]
    },
    "hey_banco": {
        "name": "Hey Banco (México)",
        "region": "LATAM / México",
        "description": "El banco digital de Banregio en México, conocido por sus pagarés bancarios garantizados e inversión simplificada en fondos.",
        "comisiones": "Cero comisiones en su pagaré tradicional. Fondos mutuos con comisiones implícitas en el precio de administración.",
        "pitfall": "Sesgo de Aversión al Riesgo Extremo",
        "pitfall_detail": (
            "Hey Banco promueve fuertemente su pagaré con rendimientos atractivos a corto plazo (7 días). Para un inversor principiante, "
            "esto actúa como una 'zona de confort' psicológica. Ver la renta variable fluctuar en bolsa contra la renta fija garantizada "
            "provoca un anclaje al rendimiento seguro a corto plazo, impidiendo el crecimiento real del capital contra la inflación a largo plazo."
        ),
        "onboarding": [
            "1. **Usa el pagaré para metas cortas:** Tu fondo de emergencia o dinero de impuestos va en el pagaré garantizado semanal.",
            "2. **Iníciate en fondos paso a paso:** Usa su sección de fondos indexados invirtiendo montos pequeños mensuales para acostumbrarte a las oscilaciones.",
            "3. **Asegura tu estatus Hey Pro:** Si usas sus beneficios, aprovecha las compras con tarjeta de débito/crédito para incrementar tus tasas seguras."
        ]
    },
    "bbva_trader": {
        "name": "BBVA Trader (España / LATAM)",
        "region": "España / LATAM",
        "description": "Plataforma de trading online e inversión respaldada por el grupo bancario tradicional BBVA.",
        "comisiones": "Comisiones más elevadas que los neobrokers (tarifas por custodia y corretaje que varían según el volumen de tu cuenta).",
        "pitfall": "Sesgo de Status Quo y Costos Invisibles",
        "pitfall_detail": (
            "Muchos principiantes eligen BBVA Trader por la comodidad y seguridad de mantener todo en su banco tradicional. "
            "Sin embargo, este 'sesgo de status quo' les hace pagar comisiones elevadas de custodia y corretaje, las cuales erosionan "
            "silenciosamente su rendimiento compuesto a largo plazo. A menudo no son conscientes de que existen alternativas reguladas más baratas."
        ),
        "onboarding": [
            "1. **Revisa la letra chica de comisiones:** Entiende exactamente cuánto te cobrarán al mes solo por mantener las acciones en cartera (custodia).",
            "2. **Evita operar en exceso:** Si las comisiones son altas, realiza aportaciones trimestrales o semestrales más grandes en lugar de muchas aportaciones mensuales pequeñas.",
            "3. **Considera ETFs sobre acciones:** Los ETFs te permiten diversificar en miles de empresas en una sola compra, reduciendo el pago de comisiones múltiples."
        ]
    },
    "openbank": {
        "name": "Openbank / Santander (España / LATAM)",
        "region": "España / LATAM",
        "description": "Banco 100% digital del Grupo Santander, que ofrece el servicio de inversión 'Invertir' con acceso a fondos, ETFs y robo-advisor.",
        "comisiones": "Sin comisión de custodia para fondos mutuos. Comisión de robo-advisor de alrededor de 0.85% anual según tu patrimonio.",
        "pitfall": "Efecto Disposición y Sesgo de Confianza de Marca",
        "pitfall_detail": (
            "El respaldo del Grupo Santander aporta una confianza psicológica que reduce el pánico del inversor principiante. "
            "No obstante, su interfaz promueve fondos de gestión activa con altas comisiones comerciales. Esto genera el 'efecto disposición': "
            "el inversor tiende a quedarse con los fondos mediocres que rinden poco por confianza en la marca, en lugar de optimizar hacia ETFs pasivos."
        ),
        "onboarding": [
            "1. **Compara fondos indexados:** Openbank tiene una excelente gama de fondos indexados (como Amundi o Vanguard) con comisiones bajísimas. Elígelos antes que los de gestión activa.",
            "2. **Prueba el Robo-Advisor con metas claras:** Su servicio automatizado de carteras ('Inversión Delegada') es excelente si buscas simplicidad absoluta.",
            "3. **Mantén tu disciplina de ahorro:** Automatiza transferencias mensuales gratuitas desde tu cuenta nómina hacia tus fondos elegidos."
        ]
    },
    "robinhood": {
        "name": "Robinhood (EEUU)",
        "region": "EEUU / Global",
        "description": "El broker pionero que popularizó el trading sin comisiones en EEUU, revolucionando la inversión minorista.",
        "comisiones": "Cero comisiones en acciones, ETFs, opciones y cripto. Spreads variables implícitos.",
        "pitfall": "Gamificación, FOMO Colectivo e Hiperactividad Financiera",
        "pitfall_detail": (
            "Robinhood diseñó su app aplicando principios de psicología del juego: confeti digital en pantalla al comprar, "
            "listas de tendencias en vivo ('Top 100') que generan urgencia visual y gráficos que parpadean agresivamente en verde/rojo. "
            "Esto induce al cerebro a buscar dopamina mediante la compra y venta constante (trading diario), guiando a pérdidas rápidas por FOMO."
        ),
        "onboarding": [
            "1. **Automatiza compras recurrentes:** Configura compras fraccionadas semanales de ETFs sólidos como VOO o QQQ para evitar mirar la pantalla diario.",
            "2. **Evita el trading de opciones:** Las opciones financieras en Robinhood son presentadas de forma muy sencilla pero son de altísimo riesgo y pérdida probable para novatos.",
            "3. **Desactiva las alertas de tendencia:** Protege tu psicología desactivando alertas de activos altamente volátiles recomendados por las redes."
        ]
    }
}

# Diccionario de sesgos cognitivos y estrategias de coaching conductual
BIASES_COACHING = {
    "fomo": {
        "explanation": "FOMO (Miedo a perderse algo): La urgencia psicológica de comprar un activo impulsado por ver que otros ganan dinero rápido y que su precio sube bruscamente.",
        "coach_response": (
            "🚀 **Coach SIPA:** Veo que sientes la adrenalina de no querer quedarte fuera de esta subida. Es una respuesta biológica normal sentir envidia sana cuando otros ganan dinero. "
            "Sin embargo, la historia nos enseña que **comprar un activo que ha subido de forma vertical es la forma más común en que los inversores novatos pierden capital**. "
            "El precio en euforia suele incorporar expectativas poco realistas. Cuando la masa eufórica se agota, el activo suele experimentar correcciones violentas.\n\n"
            "Recuerda: **El mercado da oportunidades constantemente**. Es preferible perderse una subida temporal que subirse en la cima de una burbuja."
        ),
        "exercise": (
            "🧘 **Micro-Ejercicio de Calma:** Antes de comprar, cierra la aplicación de trading. Escribe en un papel: "
            "1) ¿Compraría este activo si nadie más estuviera hablando de él? "
            "2) ¿Entiendo cómo gana dinero este negocio, o solo lo compro porque su precio está subiendo? "
            "Espera **24 horas** antes de tomar cualquier decisión de compra impulsiva."
        )
    },
    "panico": {
        "explanation": "Pánico Vendedor: El impulso descontrolado de vender tus activos ante caídas repentinas en el mercado para evitar 'perderlo todo'.",
        "coach_response": (
            "📉 **Coach SIPA:** Comprendo perfectamente tu preocupación. Ver que el dinero que tanto esfuerzo te costó ganar disminuye en pantalla dispara de inmediato la alerta de supervivencia de nuestro cerebro. "
            "Pero ten presente esto: **Las fluctuaciones de precio a corto plazo son completamente normales y cíclicas en la inversión**. "
            "Históricamente, los mercados financieros globales tienen un sesgo alcista a largo plazo porque representan el crecimiento de la economía mundial. "
            "Vender en el punto más bajo del pánico solo tiene un resultado garantizado: **congelar y materializar pérdidas reales** que de otro modo habrían sido minusvalías temporales en papel."
        ),
        "exercise": (
            "🧘 **Micro-Ejercicio de Calma:** Haz un paso atrás. Abre el gráfico histórico del S&P 500 a 30 años. "
            "Busca caídas brutales como la burbuja puntocom (2000), la crisis subprime (2008) o la pandemia (2020). "
            "Observa cómo todas ellas, en el gran esquema de las cosas, terminaron siendo baches temporales. "
            "Si tu tesis de inversión a largo plazo sigue en pie, no tomes decisiones permanentes basadas en tormentas transitorias."
        )
    },
    "overconfidence": {
        "explanation": "Exceso de Confianza: Creer que posees un conocimiento, sexto sentido o intuición superior que te permite anticipar los movimientos del mercado y batirlo de forma recurrente.",
        "coach_response": (
            "🦁 **Coach SIPA:** Es excelente que tengas seguridad en tus análisis, pero el mercado es un sistema caótico complejo compuesto por millones de mentes y algoritmos. "
            "Subestimar la aleatoriedad y el azar es el error más costoso de los inversores. "
            "El exceso de confianza nos hace concentrar el capital en muy pocos activos especulativos y nos lleva a creer que un éxito inicial se debe enteramente a nuestra habilidad, cuando "
            "a menudo fue simplemente viento a favor del mercado.\n\n"
            "El inversor más exitoso no es el que cree que lo sabe todo, sino el que reconoce sus limitaciones y diseña una cartera a prueba de su propia ignorancia mediante la diversificación."
        ),
        "exercise": (
            "🧘 **Micro-Ejercicio de Calma:** Anota tus predicciones exactas hoy: escribe qué activo subirá, cuánto y cuándo. "
            "Revisa esta nota en 3 meses. Esto te dará una dosis realista de humildad sobre la extrema dificultad de predecir el futuro a corto plazo."
        )
    },
    "loss_aversion": {
        "explanation": "Aversión a la Pérdida: Sentir un dolor psicológico tan agudo ante una pérdida que prefieres mantener posiciones perdedoras indefinidamente con la vana esperanza de recuperar tu dinero.",
        "coach_response": (
            "🩹 **Coach SIPA:** La psicología del comportamiento ha demostrado que **sentimos el doble de dolor al perder 100 dólares que el placer que nos da ganar 100 dólares**. "
            "Por eso nos aferramos a inversiones zombis o en declive, pensando: 'si no vendo, no he perdido realmente'. "
            "Este comportamiento te ancla al pasado y te impide reasignar ese capital a activos productivos o ETFs diversificados que sí tienen potencial real de recuperación y crecimiento futuro."
        ),
        "exercise": (
            "🧘 **Micro-Ejercicio de Calma:** Pregúntate sinceramente: 'Si hoy tuviera el equivalente en efectivo de mi posición actual en esta empresa perdedora, ¿compraría acciones de esta misma empresa hoy?' "
            "Si la respuesta es NO, entonces no tiene sentido lógico seguir manteniendo ese activo. Estás sufriendo el sesgo del costo hundido."
        )
    },
    "anchoring": {
        "explanation": "Anclaje: Tomar decisiones financieras basándote obsesivamente en un punto de referencia del pasado (usualmente tu precio de compra original), ignorando los nuevos datos fundamentales.",
        "coach_response": (
            "⚓ **Coach SIPA:** Te has anclado a un número de referencia. Al mercado no le importa a qué precio compraste tú esa acción, ni respeta tus puntos de equilibrio personales. "
            "Los precios se mueven en base al valor actual de la empresa, las tasas de interés y las condiciones macroeconómicas. "
            "Esperar a vender 'hasta que vuelva a lo que me costó' es una regla mental arbitraria que puede costarte años de costo de oportunidad en inversiones mucho más seguras y rentables."
        ),
        "exercise": (
            "🧘 **Micro-Ejercicio de Calma:** Escribe en una hoja el precio actual de mercado de tu activo y olvida por un momento tu precio de entrada. "
            "Haz un análisis objetivo de las perspectivas de esta empresa para los próximos 5 años bajo las condiciones de hoy. Decide tu permanencia en base al futuro, no al pasado."
        )
    },
    "ninguno": {
        "explanation": "Comportamiento Racional / Neutro: Enfoque equilibrado, enfocado en el largo plazo, el análisis objetivo y la diversificación de riesgos sin cargas emocionales extremas.",
        "coach_response": (
            "⚖️ **Coach SIPA:** Tu tono refleja equilibrio, racionalidad y una mentalidad serena. Esta es exactamente la actitud mental "
            "que separa a los inversores exitosos de la masa que es arrastrada por los vaivenes emocionales del mercado. "
            "Mantener este enfoque estructurado, enfocado en el ahorro constante y el control de costos, es tu mejor escudo protector "
            "contra la aleatoriedad bursátil."
        ),
        "exercise": (
            "📈 **Consejo de Mantenimiento:** Sigue documentando tu diario de inversión. Continúa programando tus planes de ahorro "
            "de forma automática y dedícale tiempo a tu educación financiera sin obsesionarte con los precios diarios."
        )
    }
}

def get_broker_profile(broker_id: str) -> dict:
    """Devuelve la ficha psicológica y de onboarding del broker seleccionado."""
    return BROKERS_PROFILE.get(broker_id, BROKERS_PROFILE["gbm"])

def generate_coach_response(
    user_text: str,
    detected_intent: str,
    detected_bias: str,
    bias_probs: dict,
    broker_id: str,
    openai_key: str = None
) -> dict:
    """
    Genera la respuesta del Coach SIPA v2 de manera híbrida.
    Si se proporciona una OpenAI API Key válida, enriquece la conversación vía GPT-4o-mini.
    Si no, genera una respuesta local robusta basada en reglas conductuales detalladas.
    """
    broker_info = get_broker_profile(broker_id)
    bias_coaching = BIASES_COACHING.get(detected_bias, BIASES_COACHING["ninguno"])
    
    # Formatear el diagnóstico local cuantitativo en un texto legible
    diagnostico_local = (
        f"**Diagnóstico Psicológico Cuantitativo (Local ML):**\n"
        f"- **Sesgo Dominante:** {detected_bias.upper()} (Explicación: {bias_coaching['explanation']})\n"
        f"- **Intención Detectada:** {detected_intent.upper()}\n"
        f"- **Plataforma Activa:** {broker_info['name']} ({broker_info['region']})\n"
    )
    
    # Camino A: Integración opcional con OpenAI
    if openai_key and openai_key.strip().startswith("sk-"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key.strip())
            
            # Construir el sistema de prompt para guiar la respuesta del Coach Financiero
            system_prompt = (
                "Eres el Coach SIPA v2, un asistente psicológico y de finanzas personales "
                "de élite, especializado en guiar a inversores principiantes. Tu tono es empático, racional, "
                "humilde y profundamente educativo. Tu misión principal es desmitificar la ilusión de predecir "
                "el futuro y promover la inversión diversificada a largo plazo basada en evidencia del comportamiento.\n\n"
                f"El usuario te escribe utilizando la plataforma: {broker_info['name']}.\n"
                f"Nuestros modelos locales de machine learning han analizado su mensaje y detectado:\n"
                f"- Sesgo Cognitivo: {detected_bias} (Confianza en probabilidades: {bias_probs})\n"
                f"- Intención del usuario: {detected_intent}\n\n"
                "Instrucciones de Respuesta:\n"
                "1. Saluda cordialmente y sé sumamente empático sobre la emoción que siente el usuario (pánico, codicia, FOMO, etc.).\n"
                f"2. Conecta su estado emocional con las trampas específicas de la interfaz (UX) del broker: '{broker_info['name']}' "
                f"usando esta advertencia conductual de nuestra base de datos: '{broker_info['pitfall_detail']}'.\n"
                "3. Explica científicamente por qué el mercado es cíclico y por qué intentar adivinar los movimientos a corto plazo es "
                "matemáticamente improductivo para un minorista.\n"
                "4. Bríndale pasos de acción prácticos e introduce un micro-ejercicio de calma psicológica.\n"
                "5. Estructura tu respuesta en Markdown de manera elegante, profesional y visualmente escaneable. Usa negritas y viñetas."
            )
            
            # Llamar al modelo rápido GPT-4o-mini
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            ai_content = response.choices[0].message.content
            
            return {
                "success": True,
                "is_llm": True,
                "diagnostico": diagnostico_local,
                "response": ai_content,
                "probs": bias_probs
            }
            
        except Exception as e:
            # Fallback en caso de que falle la API (por red, cuota o key inválida)
            print(f"⚠️ Error al llamar a OpenAI API: {str(e)}. Utilizando fallback local por reglas.")
            # Continuar hacia el Camino B
            
    # Camino B: Motor experto local por reglas conductuales (100% gratuito)
    response_markdown = (
        f"### {bias_coaching['coach_response'].split('**')[0]} {bias_coaching['coach_response'].split('**')[1] if len(bias_coaching['coach_response'].split('**')) > 1 else ''}\n"
        f"{bias_coaching['coach_response'].replace('🚀 **Coach SIPA:** ', '').replace('📉 **Coach SIPA:** ', '').replace('🦁 **Coach SIPA:** ', '').replace('🩹 **Coach SIPA:** ', '').replace('⚓ **Coach SIPA:** ', '').replace('⚖️ **Coach SIPA:** ', '')}\n\n"
        f"--- \n\n"
        f"### 🛡️ Trampa Psicológica de la Interfaz del Broker ({broker_info['name']})\n"
        f"En tu perfil seleccionaste **{broker_info['name']}**. Esto es lo que debes tener en cuenta al usar su plataforma:\n"
        f"- **Sesgo Frecuente en esta App:** *{broker_info['pitfall']}*\n"
        f"- **¿Cómo te influye su diseño?** {broker_info['pitfall_detail']}\n"
        f"- **Comisiones Reales:** {broker_info['comisiones']}\n\n"
        f"--- \n\n"
        f"{bias_coaching['exercise']}\n\n"
        f"--- \n\n"
        f"### 📋 Guía Rápida para Iniciantes en {broker_info['name']}:\n"
        f"Sigue estos tres pasos para estructurar tu inversión con disciplina:\n"
        f"{chr(10).join(broker_info['onboarding'])}"
    )
    
    return {
        "success": True,
        "is_llm": False,
        "diagnostico": diagnostico_local,
        "response": response_markdown,
        "probs": bias_probs
    }

# Prueba local del módulo
if __name__ == "__main__":
    print("Testing coach module...")
    # Simulando vectores de probabilidad y salida del clasificador local
    dummy_probs = {"fomo": 0.85, "panico": 0.02, "overconfidence": 0.03, "loss_aversion": 0.05, "anchoring": 0.05}
    
    # Test local gratis (Reglas)
    print("\n--- TEST LOCAL (SIN API KEY) ---")
    res_free = generate_coach_response(
        user_text="Todos están ganando menos yo, ¡debería comprar ya!",
        detected_intent="quiero_comprar",
        detected_bias="fomo",
        bias_probs=dummy_probs,
        broker_id="trade_republic"
    )
    print(res_free["diagnostico"])
    print(res_free["response"][:300] + "...\n[Truncated for console preview]")
