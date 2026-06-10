import pandas as pd
import random
from typing import List, Dict
import numpy as np

class DatasetGenerator:
    def __init__(self):
        # Ejemplos base para cada intención (150 por intención = 750 total)
        self.ejemplos_intenciones = {
            'consultar_cartera': [
                "¿cuánto vale mi cartera?", "¿cómo van mis acciones?", "quiero ver mi rendimiento",
                "¿cuál es el valor actual de mi portafolio?", "¿cuánto he ganado/perdido?", "muéstrame mis inversiones",
                "¿qué tal está mi portfolio?", "necesito ver el estado de mis activos", "¿cuánto dinero tengo invertido?",
                "dime el valor de mis acciones", "¿cómo está funcionando mi inversión?", "quiero revisar mi cartera",
                "¿cuál es mi patrimonio actual?", "muéstrame el rendimiento de mis fondos", "¿cómo van mis posiciones?",
                "necesito un resumen de mi cartera", "¿cuál es el valor total de mis activos?", "quiero saber cómo va mi dinero",
                "¿cuánto vale todo lo que tengo invertido?", "dime el estado de mis inversiones", "¿qué rendimiento tengo?",
                "quiero ver mis ganancias/pérdidas", "¿cómo está mi portfolio hoy?", "necesito revisar mis activos",
                "¿cuánto dinero tengo en el mercado?", "muéstrame el valor de mis posiciones", "¿cómo va todo lo invertido?",
                "quiero saber mi situación financiera", "¿cuál es el valor de mi patrimonio bursátil?", "dime cómo van mis fondos",
                "necesito ver el performance de mi cartera", "¿cuánto tengo en acciones?", "quiero revisar mi portafolio completo",
                "¿qué tal mis inversiones este mes?", "muéstrame el detalle de mi cartera", "¿cómo está el valor de mis activos?",
                "quiero saber mi patrimonio neto", "¿cuánto he ganado este año?", "necesito ver el estado de mis posiciones",
                "¿cómo va mi rendimiento acumulado?", "dime el valor actual de todo", "quiero ver mis resultados",
                "¿cuál es mi situación financiera actual?", "muéstrame mis activos y su valor", "necesito un reporte de mi cartera",
                "¿cómo están mis inversiones hoy?", "quiero saber el valor total", "¿cuánto dinero tengo en el mercado bursátil?",
                "dime el rendimiento de mi portafolio", "necesito ver mis ganancias", "¿cómo está funcionando todo lo invertido?",
                "quiero revisar mi situación patrimonial", "¿cuál es el valor de mis posiciones abiertas?", "muéstrame el estado de mis fondos",
                "necesito saber cuánto tengo invertido", "¿cómo va mi portfolio esta semana?", "quiero ver el detalle de mis activos",
                "¿cuál es mi rendimiento total?", "dime el valor de mis inversiones", "necesito revisar mi portafolio completo",
                "¿cómo están mis posiciones hoy?", "quiero saber mi patrimonio", "muéstrame el performance de mis activos",
                "necesito ver el estado de mi dinero", "¿cuánto vale mi portfolio actual?", "dime cómo van mis resultados",
                "quiero revisar mis inversiones detalladamente", "¿cuál es el valor de mis activos financieros?", "necesito un resumen ejecutivo de mi cartera",
                "¿cómo está mi rendimiento mensual?", "quiero ver mis posiciones y su valor", "dime el estado de mis finanzas invertidas",
                "necesito saber cuánto he ganado/perdido", "¿cuál es el valor actual de mi patrimonio?", "quiero ver el reporte de mis inversiones",
                "¿cómo van mis fondos este trimestre?", "muéstrame el detalle de mi portafolio", "necesito ver el valor de mis posiciones",
                "quiero saber mi situación actual", "¿cuánto dinero tengo invertido en total?", "dime el rendimiento de mis activos",
                "necesito revisar mi cartera completa", "¿cómo está mi portfolio hoy en día?", "quiero ver mis resultados financieros",
                "¿cuál es el valor de mis inversiones actuales?", "muéstrame el estado de mis posiciones", "necesito saber mi rendimiento exacto",
                "quiero ver todo lo que tengo invertido", "¿cómo va mi dinero en el mercado?", "dime el valor total de mi portafolio",
                "necesito un informe de mi cartera", "¿cuál es mi rendimiento acumulado este año?", "quiero ver mis activos y su rendimiento",
                "¿cómo están funcionando mis inversiones?", "muéstrame el valor de mis fondos", "necesito saber mi situación patrimonial",
                "quiero revisar mis posiciones abiertas", "¿cuánto tengo en el mercado actualmente?", "dime el performance de mi cartera",
                "necesito ver el estado completo de mis activos", "¿cómo va mi portfolio esta semana?", "quiero saber mi valor neto invertido",
                "¿cuál es el rendimiento de mis fondos?", "muéstrame mis inversiones y su valor", "necesito revisar mi portafolio detalladamente",
                "quiero saber cómo está mi dinero", "¿cuánto vale todo lo invertido?", "dime el estado de mis finanzas bursátiles",
                "necesito ver mis resultados mensuales", "¿cómo está mi cartera hoy?", "quiero un resumen de mis activos",
                "¿cuál es el valor de mis posiciones?", "muéstrame el rendimiento de mis inversiones", "necesito saber mi patrimonio financiero",
                "quiero ver el detalle de mi portafolio", "¿cómo van mis fondos este año?", "dime el valor total de mis activos",
                "necesito revisar mi situación financiera", "¿cuánto he ganado con mis inversiones?", "quiero ver mis posiciones y rendimientos",
                "¿cuál es mi rendimiento trimestral?", "quiero ver mis ganancias acumuladas", "necesito saber mi posición neta",
                "¿cómo está mi diversificación?", "dime el valor por sector", "quiero ver mi allocation",
                "¿cuál es mi risk exposure?", "necesito ver mi volatilidad", "quiero saber mi drawdown",
                "¿cómo está mi sharpe ratio?", "dime mi beta", "necesito ver mi correlación",
                "¿cuál es mi posición en efectivo?", "quiero ver mi liquidity", "necesito saber mi cash ratio",
                "¿cómo está mi performance vs benchmark?", "dime mi alpha", "quiero ver mi tracking error",
                "¿cuál es mi asset allocation?", "necesito ver mi diversificación", "quiero saber mi peso por activo",
                "¿cómo está mi income generation?", "dime mis dividendos", "necesito ver mis yields",
                "¿cuál es mi capital gains?", "quiero ver mis ganancias realizadas", "necesito saber mis pérdidas",
                "¿cómo está mi tax efficiency?", "dime mi carga fiscal", "quiero ver mi after-tax return",
                "¿cuál es mi liquidity ratio?", "necesito ver mi cash flow", "quiero saber mi capacidad de venta",
                "¿cómo está mi concentration risk?", "dime mis posiciones grandes", "necesito ver mi overweight",
                "¿cuál es mi sector allocation?", "quiero ver mi distribución", "necesito saber mi exposure",
                "¿cómo está mi geographic allocation?", "dime mi distribución geográfica", "quiero ver mis mercados",
                "¿cuál es mi duration?", "necesito ver mi sensibilidad", "quiero saber mi convexidad",
                "¿cómo está mi credit quality?", "dime mis ratings", "necesito ver mi default risk",
                "¿cuál es mi ESG score?", "quiero ver mi sostenibilidad", "necesito saber mi impacto",
                "¿cómo está mi turnover?", "dime mi rotación", "quiero ver mis transacciones",
                "¿cuál es mi expense ratio?", "necesito ver mis costos", "quiero saber mis fees",
                "¿cómo está mi rebalancing?", "dime mis ajustes", "necesito ver mi reequilibrio",
                "¿cuál es mi stress test?", "quiero ver mi escenario adverso", "necesito saber mi VaR",
                "¿cómo está mi monte carlo?", "dime mis simulaciones", "quiero ver mis proyecciones",
                "¿cuál es mi scenario analysis?", "necesito ver mis escenarios", "quiero saber mi sensitividad",
                "¿cómo está mi backtesting?", "dime mi histórico", "necesito ver mi validation",
                "¿cuál es mi forward testing?", "quiero ver mis proyecciones", "necesito saber mi out-of-sample",
                "¿cómo está mi optimization?", "dime mi frontera eficiente", "quiero ver mi portafolio óptimo",
                "¿cuál es mi risk parity?", "necesito ver mi balance riesgo", "quiero saber mi igualación",
                "¿cómo está mi factor exposure?", "dime mis factores", "necesito ver mis betas",
                "¿cuál es mi style drift?", "quiero ver mi desviación", "necesito saber mi consistencia",
                "¿cómo está mi capacity?", "dime mi límite", "quiero ver mi escala",
                "¿cuál es mi scalability?", "necesito ver mi crecimiento", "quiero saber mi potencial",
                "¿cómo está mi liquidity premium?", "dime mi prima", "necesito ver mi compensación",
                "¿cuál es mi illiquidity discount?", "quiero ver mi descuento", "necesito saber mi penalización",
                "¿cómo está mi market impact?", "dime mi efecto", "necesito ver mi costo transaccional",
                "¿cuál es mi slippage?", "quiero ver mi deslizamiento", "necesito saber mi execution",
                "¿cómo está mi timing?", "dime mi momento", "quiero ver mi acierto",
                "¿cuál es mi selection?", "necesito ver mi picking", "quiero saber mi acierto",
                "¿cómo está mi attribution?", "dime mi fuente", "necesito ver mi descomposición",
                "¿cuál es mi contribution?", "quiero ver mi impacto", "necesito saber mi peso",
                "¿cómo está mi marginal contribution?", "dime mi marginal", "quiero ver mi incremental",
                "¿cuál es mi risk contribution?", "necesito ver mi riesgo", "quiero saber mi exposición",
                "¿cómo está mi performance attribution?", "dime mi análisis", "necesito ver mi desglose",
                "¿cuál es mi risk attribution?", "quiero ver mi riesgo", "necesito saber mi fuente",
                "¿cómo está mi factor attribution?", "dime mis factores", "necesito ver mi contribución",
                "¿cuál es mi sector attribution?", "quiero ver mis sectores", "necesito saber mi peso",
                "¿cómo está mi security attribution?", "dime mis valores", "necesito ver mi selección",
                "¿cuál es mi currency attribution?", "quiero ver mis divisas", "necesito saber mi efecto",
                "¿cómo está mi duration attribution?", "dime mi duración", "necesito ver mi sensibilidad",
                "¿cuál es mi convexity attribution?", "quiero ver mi curvatura", "necesito saber mi no-linealidad",
                "¿cómo está mi volatility attribution?", "dime mi volatilidad", "necesito ver mi riesgo",
                "¿cuál es my correlation attribution?", "quiero ver mi correlación", "necesito saber mi diversificación",
                "¿cómo está mi skewness attribution?", "dime mi asimetría", "necesito ver mi sesgo",
                "¿cuál es mi kurtosis attribution?", "quiero ver mi cola", "necesito saber mi extremos",
                "¿cómo está mi VaR attribution?", "dime mi pérdida máxima", "necesito ver mi riesgo extremo",
                "¿cuál es mi CVaR attribution?", "quiero ver mi pérdida esperada", "necesito saber mi cola",
                "¿cómo está mi stress attribution?", "dime mi estrés", "necesito ver mi adverso",
                "¿cuál es mi scenario attribution?", "quiero ver mis escenarios", "necesito saber mi sensitividad",
                "¿cómo está mi sensitivity attribution?", "dime mi sensibilidad", "necesito ver mi impacto",
                "¿cuál es mi greeks attribution?", "quiero ver mis griegas", "necesito saber mi derivados",
                "¿cómo está mi delta attribution?", "dime mi delta", "necesito ver mi lineal",
                "¿cuál es mi gamma attribution?", "quiero ver mi gamma", "necesito saber mi curvatura",
                "¿cómo está mi vega attribution?", "dime mi vega", "necesito ver mi volatilidad",
                "¿cuál es mi theta attribution?", "quiero ver mi theta", "necesito saber mi tiempo",
                "¿cómo está mi rho attribution?", "dime mi rho", "necesito ver mi tasa",
                "¿cuál es mi carry attribution?", "quiero ver mi carry", "necesito saber mi financiamiento",
                "¿cómo está mi roll attribution?", "dime mi roll", "necesito ver mi vencimiento",
                "¿cuál es mi term structure attribution?", "quiero ver mi estructura", "necesito saber mi curva",
                "¿cómo está mi spread attribution?", "dime mi spread", "necesito ver mi diferencial",
                "¿cuál es mi credit attribution?", "quiero ver mi crédito", "necesito saber mi default",
                "¿cómo está mi liquidity attribution?", "dime mi liquidez", "necesito ver mi mercado",
                "¿cuál es mi market impact attribution?", "quiero ver mi impacto", "necesito saber mi ejecución",
                "¿cómo está mi transaction cost attribution?", "dime mi costo", "necesito ver mi transacción",
                "¿cuál es mi slippage attribution?", "quiero ver mi deslizamiento", "necesito saber mi ejecución",
                "¿cómo está mi implementation shortfall?", "dime mi shortfall", "necesito ver mi implementación",
                "¿cuál es mi opportunity cost?", "quiero ver mi oportunidad", "necesito saber mi costo",
                "¿cómo está mi market timing?", "dime mi timing", "necesito ver mi momento",
                "¿cuál es mi security selection?", "quiero ver mi selección", "necesito saber mi picking",
                "¿cómo está mi currency selection?", "dime mi divisa", "necesito ver mi forex",
                "¿cuál es mi asset allocation?", "quiero ver mi allocation", "necesito saber mi distribución",
                "¿cómo está mi rebalancing?", "dime mi reequilibrio", "necesito ver mis ajustes",
                "¿cuál es mi cash flow?", "quiero ver mi flujo", "necesito saber mi movimiento",
                "¿cómo está mi contribution?", "dime mi contribución", "necesito ver mi impacto",
                "¿cuál es mi performance?", "quiero ver mi rendimiento", "necesito saber mi resultado"
            ],
            'quiero_comprar': [
                "¿debería meter dinero en NVDA?", "quiero invertir en tech", "estoy pensando en comprar acciones",
                "¿qué tal si compro Tesla?", "me gustaría invertir en criptomonedas", "¿es buen momento para comprar Apple?",
                "quiero entrar en el mercado", "¿dónde puedo invertir mi dinero?", "estoy considerando comprar ETFs",
                "¿qué me recomiendan comprar?", "quiero añadir más acciones a mi cartera", "¿es buena idea comprar ahora?",
                "estoy buscando oportunidades de inversión", "¿debería comprar más de esta acción?", "quiero diversificar mi portafolio",
                "¿qué acción recomiendan comprar?", "estoy pensando en invertir en biotecnología", "quiero comprar mi primera acción",
                "¿es buen momento para entrar al mercado?", "quiero invertir en energías renovables", "¿qué tal si compro oro?",
                "estoy considerando comprar fondos indexados", "¿debería meter más dinero en mi cartera?", "quiero comprar acciones de IA",
                "¿es buena idea comprar cryptocurrency ahora?", "estoy buscando dónde invertir", "quiero comprar acciones baratas",
                "¿qué tal si invierto en bienes raíces?", "estoy pensando en comprar REITs", "¿debería comprar más Tesla?",
                "quiero invertir en empresas de tecnología", "¿es buen momento para comprar crypto?", "estoy considerando comprar dividendos",
                "¿qué acción me recomiendan comprar hoy?", "quiero añadir posiciones a mi portafolio", "¿debería comprar acciones de bancos?",
                "estoy buscando comprar algo estable", "quiero invertir en startups", "¿es buena idea comprar ahora que está barato?",
                "¿qué tal si compro acciones de China?", "estoy pensando en invertir en latinoamérica", "quiero comprar mi primer ETF",
                "¿debería meter dinero en el mercado ahora?", "quiero comprar acciones de crecimiento", "estoy considerando comprar valor",
                "¿es buen momento para comprar tecnología?", "quiero invertir en mercados emergentes", "¿qué tal si compro bonos?",
                "estoy buscando diversificar", "quiero comprar acciones de dividendos", "¿debería comprar más crypto?",
                "¿qué me dicen si compro Amazon?", "estoy pensando en comprar Google", "quiero añadir más tecnología a mi cartera",
                "¿es buena idea comprar ahora que hay volatilidad?", "quiero invertir en sectores defensivos", "¿debería comprar acciones de salud?",
                "estoy considerando comprar commodities", "quiero comprar acciones de energía", "¿qué tal si compro petróleo?",
                "¿debería comprar más cuando baja?", "quiero invertir en inteligencia artificial", "estoy pensando en comprar semiconductores",
                "¿es buen momento para entrar en cripto?", "quiero comprar acciones de retail", "¿qué tal si compro Walmart?",
                "estoy buscando oportunidades de compra", "quiero invertir en infraestructura", "¿debería comprar acciones de construcción?",
                "¿es buena idea comprar ahora que sube?", "quiero comprar acciones de finanzas", "estoy pensando en comprar bancos",
                "¿qué me recomiendan comprar a largo plazo?", "quiero añadir más posiciones", "¿debería comprar más de lo mismo?",
                "estoy considerando comprar algo nuevo", "quiero invertir en sectores que crecen", "¿es buen momento para comprar crecimiento?",
                "¿qué tal si compro acciones de consumo?", "quiero comprar empresas estables", "¿debería comprar blue chips?",
                "estoy buscando comprar algo seguro", "quiero invertir en valores de calidad", "¿es buena idea comprar ahora?",
                "¿qué me dicen si compro más de esto?", "quiero diversificar con nuevas compras", "¿debería comprar cuando hay corrección?",
                "estoy pensando en comprar a buen precio", "quiero añadir más activos", "¿es buen momento para comprar valor?",
                "¿qué tal si compro algo de dividendos?", "quiero comprar acciones de pago de dividendos", "¿debería comprar más ahora?",
                "estoy buscando buenas oportunidades", "quiero invertir en empresas sólidas", "¿es buena idea comprar tecnología?",
                "¿qué me recomiendan comprar para principiantes?", "quiero comprar mi primera inversión", "¿debería comprar ETFs ahora?",
                "estoy considerando comprar fondos mutuos", "quiero invertir en algo conservador", "¿es buen momento para comprar bonos?",
                "¿qué tal si compro algo de crecimiento?", "quiero comprar acciones de empresas en expansión", "¿debería comprar más riesgo?",
                "estoy buscando comprar para el largo plazo", "quiero añadir más diversificación", "¿es buena idea comprar ahora?"
            ],
            'quiero_vender': [
                "quiero salirme de Apple", "voy a vender todo", "necesito vender mis acciones",
                "¿debería vender Tesla ahora?", "estoy pensando en liquidar mi cartera", "quiero vender mis posiciones",
                "¿es buen momento para vender?", "voy a salir del mercado", "necesito liquidez, quiero vender",
                "estoy considerando vender mis ganancias", "quiero vender mis pérdidas", "¿debería vender todo ahora?",
                "voy a reducir mi exposición", "quiero vender algunas acciones", "necesito vender para comprar otra cosa",
                "¿es buena idea vender ahora?", "estoy pensando en vender mis tech stocks", "quiero liquidar todo",
                "voy a vender mis crypto", "necesito vender mis fondos", "¿debería vender mis ganancias?",
                "estoy considerando vender mis pérdidas", "quiero salirme de esta posición", "voy a vender mi cartera completa",
                "¿es buen momento para vender tecnología?", "necesito vender para diversificar", "quiero vender mis acciones de crecimiento",
                "estoy pensando en vender mis ETFs", "voy a reducir mis posiciones", "¿debería vender ahora que subió?",
                "quiero vender mis dividendos", "necesito vender mis bonos", "estoy considerando vender mis REITs",
                "voy a salirme de commodities", "quiero vender mis posiciones perdedoras", "¿es buena idea vender ahora?",
                "necesito vender para reequilibrar", "estoy pensando en vender mis ganancias", "quiero liquidar mis activos de riesgo",
                "voy a vender mis acciones de IA", "¿debería vender mis crypto ahora?", "necesito vender mis posiciones grandes",
                "estoy considerando vender mis bancos", "quiero vender mis acciones de energía", "voy a reducir mi cartera",
                "¿es buen momento para vender retail?", "necesito vender mis posiciones de crecimiento", "estoy pensando en vender mis valores",
                "quiero vender mis acciones de consumo", "voy a liquidar mis fondos indexados", "¿debería vender mis ganancias este año?",
                "necesito vender para pagar impuestos", "estoy considerando vender mis posiciones largas", "quiero salirme del mercado por un tiempo",
                "voy a vender mis acciones de salud", "¿es buena idea vender ahora que hay volatilidad?", "necesito vender mis posiciones de riesgo",
                "estoy pensando en vender mis emergentes", "quiero vender mis acciones de China", "voy a reducir mi exposición internacional",
                "¿debería vender mis bonos ahora?", "necesito vender mis posiciones de dividendos", "estoy considerando vender mis blue chips",
                "quiero vender mis posiciones de valor", "voy a liquidar mis inversiones especulativas", "¿es buen momento para vender?",
                "necesito vender mis acciones de tecnología", "estoy pensando en vender mis posiciones ganadoras", "quiero vender mis activos de crecimiento",
                "voy a reducir mi riesgo", "¿debería vender mis posiciones grandes?", "necesito vender para reinvertir",
                "estoy considerando vender mis posiciones pequeñas", "quiero vender mis acciones de semiconductores", "voy a salirme de energía",
                "¿es buena idea vender ahora?", "necesito vender mis posiciones de finanzas", "estoy pensando en vender mis acciones de construcción",
                "quiero vender mis posiciones de infraestructura", "voy a liquidar mis posiciones de commodities", "¿debería vender mis ganancias?",
                "necesito vender para diversificar", "estoy considerando vender mis posiciones defensivas", "quiero vender mis acciones de consumo básico",
                "voy a reducir mi exposición al mercado", "¿es buen momento para vender todo?", "necesito vender mis posiciones de calidad",
                "estoy pensando en vender mis valores de pago", "quiero vender mis acciones estables", "voy a liquidar mis posiciones seguras",
                "¿debería vender mis posiciones conservadoras?", "necesito vender mis activos de bajo riesgo", "estoy considerando vender mis posiciones largoplacistas",
                "quiero vender mis inversiones a largo plazo", "voy a reducir mi cartera de dividendos", "¿es buena idea vender ahora?",
                "necesito vender para tomar ganancias", "estoy pensando en vender mis posiciones de valor", "quiero vender mis acciones baratas",
                "voy a liquidar mis posiciones de compra", "¿debería vender mis posiciones de crecimiento?", "necesito vender mis activos de alto rendimiento",
                "estoy considerando vender mis posiciones agresivas", "quiero vender mis acciones especulativas", "voy a salirme de inversiones de riesgo",
                "¿es buen momento para vender?", "necesito vender mis posiciones de volatilidad", "estoy pensando en vender mis acciones cíclicas",
                "quiero vender mis posiciones sensibles", "voy a reducir mi exposición sectorial", "¿debería vender mis posiciones geográficas?",
                "necesito vender mis acciones internacionales", "estoy considerando vender mis posiciones de mercados desarrollados", "quiero vender mis activos globales",
                "voy a liquidar mis posiciones mundiales", "¿es buena idea vender ahora?", "necesito vender para reequilibrar mi cartera",
                "estoy pensando en vender mis posiciones desbalanceadas", "quiero vender mis acciones sobrepeso", "voy a reducir mis concentraciones",
                "¿debería vender mis posiciones grandes?", "necesito vender mis activos concentrados", "estoy considerando vender mis posiciones dominantes"
            ],
            'explicar_concepto': [
                "¿qué es el RSI?", "explícame qué es diversificación", "¿qué significa P/E ratio?",
                "¿cómo funciona el mercado de valores?", "¿qué es un ETF?", "explícame qué es una acción",
                "¿qué es la volatilidad?", "¿cómo se calcula el rendimiento?", "¿qué es el beta?",
                "explícame qué es un fondo mutuo", "¿qué significa diversificar?", "¿cómo funciona el interés compuesto?",
                "¿qué es el riesgo en inversiones?", "explícame qué es un bono", "¿qué es la capitalización bursátil?",
                "¿cómo funciona el trading?", "¿qué es un índice bursátil?", "explícame qué es el dividendo",
                "¿qué significa bear market?", "¿cómo funciona el análisis técnico?", "¿qué es el análisis fundamental?",
                "explícame qué es un stop loss", "¿qué es el apalancamiento?", "¿cómo funciona el mercado de futuros?",
                "¿qué es una criptomoneda?", "explícame qué es blockchain", "¿qué significa market cap?",
                "¿cómo funciona el mercado de divisas?", "¿qué es un REIT?", "explícame qué es inflación",
                "¿qué significa PEG ratio?", "¿cómo funciona el mercado de opciones?", "¿qué es el valor intrínseco?",
                "explícame qué es el flujo de caja", "¿qué es el margen de beneficio?", "¿cómo funciona el mercado de commodities?",
                "¿qué significa EBITDA?", "¿qué es el patrimonio neto?", "explícame qué es el ratio de deuda",
                "¿cómo funciona el análisis de riesgos?", "¿qué es la correlación?", "¿qué significa alpha?",
                "explícame qué es el sharpe ratio", "¿qué es la desviación estándar?", "¿cómo funciona el reequilibrio de cartera?",
                "¿qué significa asset allocation?", "¿qué es el horizonte de inversión?", "explícame qué es el perfil de riesgo",
                "¿cómo funciona el dollar cost averaging?", "¿qué es el valor presente neto?", "¿qué significa TIR?",
                "explícame qué es el rendimiento anualizado", "¿qué es la volatilidad implícita?", "¿cómo funciona el mercado de derivados?",
                "¿qué significa Greeks en opciones?", "¿qué es el rendimiento de dividendos?", "explícame qué es el crecimiento de ganancias",
                "¿cómo funciona el análisis sectorial?", "¿qué es el ciclos de mercado?", "¿qué significa sentimiento del mercado?",
                "explícame qué es el momentum", "¿qué es el mean reversion?", "¿cómo funciona el análisis cuantitativo?",
                "¿qué significa backtesting?", "¿qué es el drawdown?", "explícame qué es el maximum drawdown",
                "¿cómo funciona el optimización de cartera?", "¿qué es la frontera eficiente?", "¿qué significa teoría moderna de portafolio?",
                "explícame qué es el CAPM", "¿qué es el WACC?", "¿cómo funciona el valuation?",
                "¿qué significa discounted cash flow?", "¿qué es el enterprise value?", "explícame qué es el múltiplo de EV/EBITDA",
                "¿cómo funciona el análisis de competencia?", "¿qué es el moat económico?", "¿qué significa ventaja competitiva?",
                "explícame qué es el análisis SWOT", "¿qué es el análisis PESTEL?", "¿cómo funciona el análisis de industria?",
                "¿qué significa Porter's Five Forces?", "¿qué es el análisis de cadenas de valor?", "explícame qué es el análisis de stakeholders",
                "¿cómo funciona el análisis ESG?", "¿qué es la inversión sostenible?", "¿qué significa impacto social?",
                "explícame qué es la gobernanza corporativa", "¿qué es el riesgo ambiental?", "¿cómo funciona el análisis de sostenibilidad?",
                "¿qué significa green investing?", "¿qué es la inversión socialmente responsable?", "explícame qué es el impacto financiero",
                "¿cómo funciona el análisis de ratings?", "¿qué es el credit rating?", "¿qué significa default risk?",
                "explícame qué es el sovereign risk", "¿qué es el riesgo de contraparte?", "¿cómo funciona el análisis de crédito?",
                "¿qué significa spread de crédito?", "¿qué es el yield curve?", "explícame qué es la tasa de interés",
                "¿cómo funciona el análisis monetario?", "¿qué es la política fiscal?", "¿qué significa QE?",
                "explícame qué es el tapering", "¿qué es el balance sheet?", "¿cómo funciona el análisis macroeconómico?",
                "¿qué significa PIB?", "¿qué es la inflación core?", "explícame qué es el desempleo",
                "¿cómo funciona el análisis de indicadores?", "¿qué es el ISM?", "¿qué significa PMI?",
                "explícame qué es el sentiment index", "¿qué es el fear and greed index?", "¿cómo funciona el análisis de sentimiento?",
                "¿qué significa volatilidad de VIX?", "¿qué es el put-call ratio?", "explícame qué es el advance-decline line",
                "¿cómo funciona el análisis de volumen?", "¿qué es el open interest?", "¿qué significa liquidity?",
                "explícame qué es el bid-ask spread", "¿qué es el market depth?", "¿cómo funciona el análisis de ordenes?",
                "¿qué significa order flow?", "¿qué es el high frequency trading?", "explícame qué es el market making",
                "¿cómo funciona el arbitraje?", "¿qué es el statistical arbitrage?", "¿qué significa pairs trading?",
                "explícame qué es el momentum trading", "¿qué es el swing trading?", "¿cómo funciona el position trading?",
                "¿qué significa day trading?", "¿qué es el scalping?", "explícame qué es el algorithmic trading"
            ],
            'pedir_recomendacion': [
                "¿qué me recomiendas?", "¿dónde invierto?", "¿en qué debería poner mi dinero?",
                "¿qué acción me recomiendan comprar?", "¿dónde puedo invertir para ganar dinero?", "¿me pueden dar una recomendación?",
                "¿qué es buena inversión ahora?", "¿dónde me conviene invertir?", "¿qué me sugieren hacer con mi dinero?",
                "¿cuál es la mejor inversión?", "¿dónde debería poner mis ahorros?", "¿qué me recomiendan para principiantes?",
                "¿en qué sector debo invertir?", "¿dónde me recomiendan invertir a largo plazo?", "¿qué acción es buena compra?",
                "¿qué me dicen de invertir en crypto?", "¿dónde puedo obtener buenos rendimientos?", "¿qué recomiendan para mi cartera?",
                "¿cuál es la mejor opción de inversión?", "¿dónde invierto mi dinero extra?", "¿qué me sugieren hacer ahora?",
                "¿en qué ETF me recomiendan invertir?", "¿dónde está la oportunidad ahora?", "¿qué acción me recomiendan vender?",
                "¿cuál es la mejor estrategia de inversión?", "¿dónde puedo invertir con bajo riesgo?", "¿qué me recomiendan para diversificar?",
                "¿en qué debería invertir este año?", "¿dónde está el potencial de crecimiento?", "¿qué me dicen de invertir en tecnología?",
                "¿cuál es la mejor inversión para 2024?", "¿dónde puedo invertir de forma segura?", "¿qué me recomiendan para el corto plazo?",
                "¿en qué sector hay oportunidades?", "¿dónde me conviene poner mi dinero?", "¿qué acción me recomiendan comprar ahora?",
                "¿cuál es la mejor inversión para principiantes?", "¿dónde puedo empezar a invertir?", "¿qué me sugieren para mi primer inversión?",
                "¿en qué criptomonedas debo invertir?", "¿dónde está el futuro de las inversiones?", "¿qué me recomiendan para el largo plazo?",
                "¿cuál es la mejor inversión pasiva?", "¿dónde puedo invertir sin mucho riesgo?", "¿qué me dicen de los fondos indexados?",
                "¿en qué debería invertir para jubilación?", "¿dónde está el valor ahora?", "¿qué me recomiendan para generar ingresos?",
                "¿cuál es la mejor inversión de dividendos?", "¿dónde puedo invertir para capitalización?", "¿qué me sugieren para balanced portfolio?",
                "¿en qué commodities debo invertir?", "¿dónde está la inflación protection?", "¿qué me recomiendan para proteger mi dinero?",
                "¿cuál es la mejor inversión defensiva?", "¿dónde puedo invertir en tiempos de incertidumbre?", "¿qué me dicen de los bonos?",
                "¿en qué bienes raíces debo invertir?", "¿dónde está el real estate opportunity?", "¿qué me recomiendan para ingresos pasivos?",
                "¿cuál es la mejor inversión alternativa?", "¿dónde puedo invertir fuera de acciones?", "¿qué me sugieren para private equity?",
                "¿en qué startups debo invertir?", "¿dónde está la innovación?", "¿qué me recomiendan para venture capital?",
                "¿cuál es la mejor inversión en energía?", "¿dónde está el green energy opportunity?", "¿qué me dicen de renewable energy?",
                "¿en qué healthcare debo invertir?", "¿dónde está el medical innovation?", "¿qué me recomiendan para biotech?",
                "¿cuál es la mejor inversión en AI?", "¿dónde está el tech opportunity?", "¿qué me sugieren para semiconductores?",
                "¿en qué finanzas debo invertir?", "¿dónde está el financial sector opportunity?", "¿qué me recomiendan para bancos?",
                "¿cuál es la mejor inversión en consumo?", "¿dónde está el consumer opportunity?", "¿qué me dicen de retail?",
                "¿en qué industrial debo invertir?", "¿dónde está el manufacturing opportunity?", "¿qué me recomiendan para infrastructure?",
                "¿cuál es la mejor inversión en materiales?", "¿dónde está el materials sector opportunity?", "¿qué me sugieren para commodities?",
                "¿en qué utilities debo invertir?", "¿dónde está el energy opportunity?", "¿qué me recomiendan para electric utilities?",
                "¿cuál es la mejor inversión en telecom?", "¿dónde está el communication opportunity?", "¿qué me dicen de 5G?",
                "¿en qué real estate debo invertir?", "¿dónde está el property opportunity?", "¿qué me recomiendan para REITs?",
                "¿cuál es la mejor inversión internacional?", "¿dónde está el global opportunity?", "¿qué me sugieren para emerging markets?",
                "¿en qué developed markets debo invertir?", "¿dónde está el stability opportunity?", "¿qué me recomiendan para developed economies?",
                "¿cuál es la mejor inversión en Asia?", "¿dónde está el Asia opportunity?", "¿qué me dicen de China?",
                "¿en qué Europa debo invertir?", "¿dónde está el European opportunity?", "¿qué me recomiendan para Eurozone?",
                "¿cuál es la mejor inversión en América Latina?", "¿dónde está el LatAm opportunity?", "¿qué me sugieren para Brazil?",
                "¿en qué Africa debo invertir?", "¿dónde está el Africa opportunity?", "¿qué me recomiendan para frontier markets?",
                "¿cuál es la mejor inversión en Middle East?", "¿dónde está el MENA opportunity?", "¿qué me dicen de Gulf countries?",
                "¿en qué commodities debo invertir ahora?", "¿dónde está el inflation hedge?", "¿qué me recomiendan para gold?",
                "¿cuál es la mejor inversión en plata?", "¿dónde está el precious metals opportunity?", "¿qué me sugieren para copper?",
                "¿en qué oil debo invertir?", "¿dónde está el energy opportunity?", "¿qué me recomiendan para natural gas?",
                "¿cuál es la mejor inversión en agricultura?", "¿dónde está el food security opportunity?", "¿qué me dicen de agricultural commodities?",
                "¿en qué lithium debo invertir?", "¿dónde está el battery opportunity?", "¿qué me recomiendan para electric vehicles?",
                "¿cuál es la mejor inversión en water?", "¿dónde está el water scarcity opportunity?", "¿qué me sugieren para water utilities?",
                "¿en qué carbon credits debo invertir?", "¿dónde está el ESG opportunity?", "¿qué me recomiendan para green bonds?",
                "¿cuál es la mejor inversión sostenible?", "¿dónde está el sustainability opportunity?", "¿qué me dicen de impact investing?",
                "¿en qué ESG debo invertir?", "¿dónde está el environmental opportunity?", "¿qué me recomiendan para social investing?"
            ]
        }
        
        self.sesgos = {
            'ninguno': [
                "¿cuál es el precio de Apple?", "quiero ver mi cartera", "¿cómo funciona el mercado?",
                "explícame qué es un ETF", "¿qué es el P/E ratio?", "necesito revisar mis inversiones",
                "¿cuánto vale mi portafolio?", "¿qué significa diversificar?", "quiero entender los dividendos",
                "¿cómo se calcula el rendimiento?", "¿qué es la volatilidad?", "necesito información sobre Tesla",
                "¿qué es un fondo mutuo?", "¿cómo funciona el trading?", "quiero saber sobre bonos",
                "¿qué significa beta?", "¿cómo funciona el interés compuesto?", "necesito datos del mercado",
                "¿qué es el análisis técnico?", "quiero entender el riesgo", "¿cómo funciona el reequilibrio?",
                "¿qué es el RSI?", "necesito ver mis posiciones", "¿qué significa market cap?",
                "quiero aprender sobre inversiones", "¿cómo funciona el dollar cost averaging?", "¿qué es el sharpe ratio?",
                "necesito información sobre crypto", "¿qué es blockchain?", "quiero entender los índices",
                "¿cómo funciona el análisis fundamental?", "¿qué significa PEG ratio?", "necesito datos de mi cartera",
                "quiero saber sobre REITs", "¿qué es el yield curve?", "¿cómo funciona el valuation?",
                "necesito entender la inflación", "¿qué es EBITDA?", "quiero información sobre commodities",
                "¿cómo funciona el análisis sectorial?", "¿qué es el sentimiento del mercado?", "necesito datos de rendimiento",
                "quiero entender el momentum", "¿qué es el drawdown?", "¿cómo funciona la optimización?",
                "necesito saber sobre CAPM", "¿qué es el WACC?", "quiero información sobre el flujo de caja",
                "¿cómo funciona el análisis de competencia?", "¿qué es el moat económico?", "necesito entender la ventaja competitiva",
                "quiero saber sobre ESG", "¿qué es la inversión sostenible?", "¿cómo funciona el análisis de ratings?",
                "necesito información sobre riesgo de crédito", "¿qué es el spread de crédito?", "quiero entender la tasa de interés",
                "¿cómo funciona el análisis macroeconómico?", "¿qué es el PIB?", "necesito datos de inflación",
                "quiero saber sobre indicadores económicos", "¿qué es el ISM?", "¿cómo funciona el análisis de sentimiento?",
                "necesito información sobre VIX", "¿qué es el put-call ratio?", "quiero entender la liquidez",
                "¿cómo funciona el análisis de volumen?", "¿qué es el open interest?", "necesito saber sobre spread bid-ask",
                "quiero entender el market depth", "¿qué es el order flow?", "¿cómo funciona el arbitraje?",
                "necesito información sobre HFT", "¿qué es el market making?", "quiero saber sobre statistical arbitrage",
                "¿cómo funciona el pairs trading?", "¿qué es el momentum trading?", "necesito entender el swing trading",
                "quiero saber sobre position trading", "¿qué es el day trading?", "¿cómo funciona el scalping?",
                "necesito información sobre algorithmic trading", "¿qué es el backtesting?", "quiero entender el maximum drawdown",
                "¿cómo funciona la frontera eficiente?", "¿qué es la teoría moderna de portafolio?", "necesito saber sobre asset allocation",
                "quiero entender el perfil de riesgo", "¿qué es el horizonte de inversión?", "¿cómo funciona el DCA?",
                "necesito información sobre VPN", "¿qué es la TIR?", "quiero entender el rendimiento anualizado",
                "¿cómo funciona el análisis de opciones?", "¿qué son las Greeks?", "necesito saber sobre volatilidad implícita",
                "quiero entender el valor intrínseco", "¿qué es el rendimiento de dividendos?", "¿cómo funciona el análisis de crecimiento?",
                "necesito información sobre ciclos de mercado", "¿qué es el mean reversion?", "quiero entender el análisis cuantitativo",
                "¿cómo funciona el análisis de riesgos?", "¿qué es la correlación?", "necesito saber sobre alpha",
                "quiero entender la desviación estándar", "¿qué es el reequilibrio de cartera?", "¿cómo funciona el portfolio management?",
                "necesito información sobre diversificación", "¿qué es la concentración?", "quiero entender la asignación de activos",
                "¿cómo funciona el análisis de rendimiento?", "¿qué es el benchmarking?", "necesito saber sobre attribution analysis",
                "quiero entender el risk-adjusted return", "¿qué es el information ratio?", "¿cómo funciona el performance attribution?",
                "necesito información sobre style analysis", "¿qué es el factor investing?", "quiero entender el smart beta",
                "¿cómo funciona el análisis de factores?", "¿qué es el value investing?", "necesito saber sobre growth investing",
                "quiero entender el quality investing", "¿qué es el dividend investing?", "¿cómo funciona el momentum investing?",
                "necesito información sobre size investing?", "¿qué es el low volatility investing?", "quiero entender el factor timing",
                "¿cómo funciona el tactical asset allocation?", "¿qué es el strategic asset allocation?", "necesito saber sobre dynamic allocation",
                "quiero entender el liability-driven investing", "¿qué es el goal-based investing?", "¿cómo funciona el behavioral finance?",
                "necesito información sobre prospect theory", "¿qué es el loss aversion?", "quiero entender el mental accounting",
                "¿cómo funciona el anchoring bias?", "¿qué es el confirmation bias?", "necesito saber sobre overconfidence bias?",
                "quiero entender el herd behavior", "¿qué es the disposition effect?", "¿cómo funciona el home bias?"
            ],
            'panico': [
                "esto se hunde", "voy a perderlo todo", "mejor salirme antes de que sea tarde",
                "¡esto es un desastre!", "no puedo más con estas pérdidas", "voy a vender todo ahora mismo",
                "estoy arruinado", "el mercado se viene abajo", "tengo que salir antes de que sea peor",
                "¡no puedo creer que esté perdiendo tanto!", "esto es una masacre", "voy a liquidar todo",
                "¡estoy quebrando!", "no puedo aguantar más", "el mercado está colapsando",
                "¡voy a perder mi casa!", "esto no tiene fin", "tengo que vender ya mismo",
                "¡es el fin del mundo!", "no puedo ver cómo se desvanece mi dinero", "voy a salirme de todo",
                "¡esto es una pesadilla!", "voy a perder todos mis ahorros", "el mercado está destruyendo todo",
                "¡no puedo más!", "esto es un suicidio financiero", "voy a vender antes de que quede cero",
                "¡estoy acabado!", "no puedo soportar más pérdidas", "el mercado se va al infierno",
                "¡voy a perder todo lo que tengo!", "esto es una catástrofe", "tengo que salir ya",
                "¡no puedo creer lo que está pasando!", "voy a quedar en la ruina", "el mercado está en caída libre",
                "¡esto es terrible!", "no puedo aguantar este dolor", "voy a vender todo lo que tengo",
                "¡estoy destruido!", "esto es un colapso total", "tengo que liquidar mi cartera",
                "¡voy a perder mis sueños!", "no puedo más con esto", "el mercado está muriendo",
                "¡esto es horrible!", "voy a quedar en la calle", "tengo que vender inmediatamente",
                "¡no puedo soportarlo!", "esto es el apocalipsis financiero", "voy a salirme de todo ahora",
                "¡estoy arruinado para siempre!", "no puedo ver cómo se va todo", "el mercado está explotando",
                "¡voy a perder mi futuro!", "esto es una tragedia", "tengo que vender antes del colapso",
                "¡no puedo más con este sufrimiento!", "voy a perder mis ahorros de toda la vida", "el mercado está desmoronándose",
                "¡esto es insoportable!", "voy a quedar en bancarrota", "tengo que liquidar todo ahora mismo",
                "¡estoy perdido!", "esto es un desastre total", "el mercado está cayendo en picado",
                "¡voy a perderlo todo!", "no puedo aguantar más dolor", "tengo que salir ya mismo",
                "¡esto es el fin!", "voy a perder mi patrimonio", "el mercado está destruyendo mi vida",
                "¡no puedo más!", "esto es una locura", "voy a vender todo lo que puedo",
                "¡estoy acabado financieramente!", "no puedo creer esta caída", "el mercado está en ruinas",
                "¡voy a perder mi trabajo por esto!", "esto es una pesadilla sin fin", "tengo que liquidar antes del colapso total",
                "¡no puedo soportar más pérdidas!", "voy a perder mi familia", "el mercado está aniquilando todo",
                "¡esto es devastador!", "voy a quedar sin nada", "tengo que vender ya o muero",
                "¡estoy en el infierno!", "esto es una tortura", "el mercado está acabando conmigo",
                "¡voy a perder mi mente!", "no puedo más con esta angustia", "tengo que salirme de todo inmediatamente",
                "¡esto es un horror!", "voy a perder mi salud por esto", "el mercado está matándome",
                "¡no puedo más con el estrés!", "voy a perderlo todo por completo", "tengo que vender antes del desastre final",
                "¡esto es inaceptable!", "voy a perder mi dignidad", "el mercado está humillándome",
                "¡estoy desesperado!", "esto es una agonía", "tengo que liquidar todo o me muero",
                "¡voy a perder mi alma por esto!", "no puedo más con el sufrimiento", "el mercado está destrozando mi existencia",
                "¡esto es una tragedia griega!", "voy a perder mi razón", "tengo que vender antes de enloquecer",
                "¡no puedo más con el dolor!", "voy a perder mi esperanza", "el mercado está acabando con mi futuro",
                "¡esto es un infierno en vida!", "voy a perder mi fe", "tengo que salirme de todo ahora o nunca",
                "¡estoy al borde del colapso!", "esto es una maldición", "el mercado está castigándome",
                "¡voy a perder mi alma!", "no puedo más con esta tortura", "tengo que liquidar antes del juicio final",
                "¡esto es el fin de mis días!", "voy a perder mi voluntad", "el mercado está consumiéndome",
                "¡no puedo más con esta angustia!", "voy a perder mi esencia", "tengo que vender antes de desaparecer",
                "¡esto es una condena!", "voy a perder mi espíritu", "el mercado está destrozando mi ser",
                "¡estoy en el abismo!", "esto es una oscuridad total", "tengo que salirme de todo o me hundo",
                "¡voy a perder mi existencia!", "no puedo más con este infierno", "el mercado está aniquilando mi alma",
                "¡esto es el vacío!", "voy a perder mi conciencia", "tengo que liquidar antes del olvido",
                "¡no puedo más con este sufrimiento!", "voy a perder mi identidad", "el mercado está borrando mi memoria",
                "¡esto es la nada!", "voy a perder mi ser", "tengo que vender antes del aniquilamiento total"
            ],
            'fomo': [
                "todos están ganando con crypto", "no quiero perderme la subida", "todos mis amigos están ricos con Bitcoin",
                "¡todo el mundo está comprando NVDA!", "me estoy perdiendo la fiesta", "mi vecino compró Tesla y ahora es millonario",
                "no puedo quedarme fuera", "todos están metiendo dinero en IA", "mi primo se hizo rico con GameStop",
                "¡estoy perdiendo la oportunidad de mi vida!", "todo el mundo está ganando menos yo", "no quiero ser el único que no gana",
                "todos mis colegas compraron Apple", "me estoy quedando atrás", "no puedo ver cómo otros se enriquecen",
                "¡la subida va a continuar sin mí!", "todos están entrando al mercado", "mi hermano ya compró su casa con inversiones",
                "no quiero perder el tren", "todos están hablando de las ganancias", "me siento excluido del club de los ganadores",
                "¡voy a arrepentirme si no entro ahora!", "todo el mundo está haciendo dinero fácil", "no puedo ser el tonto que no invierte",
                "todos en Twitter están ganando", "me estoy perdiendo la revolución", "no quiero quedarme mirando desde afuera",
                "¡esta es la oportunidad del siglo!", "todos mis conocidos ya compraron", "me siento idiota por no haber entrado antes",
                "no puedo permitirme perder esto", "todos están celebrando sus ganancias", "voy a odiarme si no participo",
                "¡el mercado se va a la luna sin mí!", "todo el mundo está en la fiesta", "no quiero ser el único pobre",
                "todos los influencers están recomendando comprar", "me estoy quedando en la pobreza", "no puedo soportar ver a otros ganar",
                "¡voy a perder mi chance!", "todos mis amigos ya tienen carteras", "me siento como un perdedor",
                "no quiero ser el último en enterarme", "todos están hablando de sus inversiones", "voy a morir de envidia si no entro",
                "¡esta es la última llamada!", "todo el mundo está en el barco", "no puedo quedarme en el muelle",
                "todos en Reddit están ganando", "me estoy perdiendo el oro", "no quiero ser el único que trabaja por dinero",
                "¡el FOMO me está matando!", "todos mis compañeros ya retiraron", "voy a suicidarme si no compro ahora",
                "no puedo ver más historias de éxito", "todos están viviendo el sueño", "me siento como un completo fracasado",
                "¡tengo que entrar ya!", "todos los que compraron antes son ricos ahora", "no quiero ser el pobre del grupo",
                "todos en Instagram muestran sus ganancias", "me estoy perdiendo la vida", "no puedo más con esta envidia",
                "¡voy a odiarme mañana si no compro!", "todo el mundo está en el movimiento", "me siento invisible sin inversiones",
                "todos mis contactos compraron crypto", "me estoy quedando en el pasado", "no quiero ser el antiguo",
                "¡esta es mi última oportunidad!", "todos los jóvenes ya son millonarios", "voy a morir de vergüenza si no entro",
                "no puedo soportar más FOMO", "todos están celebrando en redes sociales", "me siento como un completo inútil",
                "¡tengo que meter dinero ya!", "todo el mundo está en el futuro", "no quiero quedarse en la prehistoria",
                "todos los que entraron antes ya ganaron", "me estoy perdiendo la historia", "no puedo ser el único tonto",
                "¡voy a perder mi mente con tanto FOMO!", "todos están viviendo la vida de ricos", "me siento miserable sin inversiones",
                "no puedo más viendo a otros ganar", "todos mis amigos ya no trabajan", "voy a deprimirme si no entro",
                "¡esta es la revolución y no estoy en ella!", "todo el mundo está en el paraíso", "no quiero ser el único en el infierno",
                "todos los que compraron Bitcoin en 2020 son libres", "me estoy perdiendo la libertad", "no puedo ser el único esclavo",
                "¡tengo que comprar ahora o nunca!", "todos los influencers ya son ricos", "me siento como un completo perdedor",
                "no puedo más con esta ansiedad", "todos están disfrutando de la vida", "voy a enloquecer si no entro ya",
                "¡el FOMO me está consumiendo!", "todo el mundo está en la cima", "no quiero ser el único en el fondo",
                "todos los que compraron NVDA ya retiraron", "me estoy perdiendo la jubilación", "no puedo trabajar hasta los 65",
                "¡voy a perder mi juventud si no invierto!", "todos los millennials ya son ricos", "me siento como un dinosaurio",
                "no puedo soportar más historias de éxito", "todos están viajando por el mundo", "voy a odiarme si no participo",
                "¡esta es la generación dorada y no estoy en ella!", "todo el mundo está ganando pasivamente", "no quiero ser el único esclavo del trabajo",
                "todos los que compraron crypto ya no pagan impuestos", "me estoy perdiendo la libertad fiscal", "no puedo ser el único burócrata",
                "¡tengo que entrar al club ya!", "todos los que invirtieron ya tienen tiempo libre", "no quiero ser el único esclavo del reloj",
                "no puedo más viendo a otros disfrutar", "todos están viviendo su mejor vida", "voy a explotar si no compro ahora",
                "¡el FOMO es real y me está destruyendo!", "todo el mundo está en el paraíso financiero", "no quiero ser el único en el infierno del trabajo",
                "todos los que compraron acciones ya tienen propiedades", "me estoy perdiendo el sueño americano", "no puedo ser el único inquilino",
                "¡voy a perder mi futuro si no actúo!", "todos los jóvenes ya son independientes", "me siento como un adolescente dependiente",
                "no puedo más con esta presión social", "todos están en el grupo de los ganadores", "voy a morir de vergüenza si no entro",
                "¡esta es la ola y no estoy en ella!", "todo el mundo está surfeando la ola", "no quiero ser el único ahogándose",
                "todos los que compraron antes ya tienen legado", "me estoy perdiendo la inmortalidad financiera", "no puedo ser el único mortal",
                "¡tengo que crear mi fortuna ya!", "todos los que invirtieron ya dejaron herencia", "no quiero ser el único sin nada que dejar",
                "no puedo más con esta mediocridad", "todos están en la liga de los ricos", "voy a odiarme siempre si no entro",
                "¡el FOMO me está volviendo loco!", "todo el mundo está escribiendo su historia de éxito", "no quiero ser el único sin historia",
                "todos los que compraron crypto ya cambiaron el mundo", "me estoy perdiendo la historia", "no puedo ser un simple espectador",
                "¡voy a perder mi lugar en la historia!", "todos los inversionistas ya son legendarios", "no quiero ser un simple mortal",
                "no puedo más siendo invisible", "todos están brillando", "voy a desaparecer si no entro ya",
                "¡esta es la época dorada y me la estoy perdiendo!", "todo el mundo está en la cima del mundo", "no quiero ser el único en la base",
                "todos los que compraron antes ya cambiaron sus vidas", "me estoy perdiendo la transformación", "no puedo seguir siendo el mismo"
            ],
            'overconfidence': [
                "yo sé que esta acción va a subir seguro", "nunca me equivoco", "tengo un sexto sentido para las inversiones",
                "esto es obvio, va a explotar", "mi intuición nunca falla", "soy un genio del mercado",
                "esto es dinero fácil", "nadie conoce este mercado como yo", "voy a ser millonario con esto",
                "es matemático, tiene que subir", "soy el mejor inversor", "esto es una ganga obvia",
                "yo vi esto venir antes que nadie", "mi análisis es perfecto", "nadie puede ganarle al mercado como yo",
                "esto es seguro al 100%", "tengo el don", "voy a duplicar mi dinero en un mes",
                "es obvio que esto va a la luna", "soy un visionario", "nadie entiende esto como yo",
                "mi estrategia es infalible", "esto es garantizado", "voy a retirarme joven con esto",
                "yo sé lo que hago", "nunca pierdo", "esto es mi especialidad",
                "mi instinto es mejor que cualquier análisis", "soy un natural", "esto es obvio para cualquiera con cerebro",
                "voy a ser legendario", "nadie ve las oportunidades como yo", "esto es mi momento",
                "mi talento es innato", "no necesito análisis técnico", "yo siento el mercado",
                "esto es mi superpotencia", "soy un prodigio", "voy a cambiar el juego",
                "mi conocimiento es superior", "esto es evidente", "nadie puede competir conmigo",
                "voy a hacer historia", "soy el elegido", "esto es mi destino",
                "mi inteligencia es incomparable", "esto es fácil dinero", "nadie entiende la dinámica como yo",
                "voy a ser el próximo Buffett", "soy un maestro", "esto es mi arte",
                "mi perspectiva es única", "esto es obvio", "nadie tiene mi visión",
                "voy a dominar el mercado", "soy un genio financiero", "esto es mi territorio",
                "mi intuición es divina", "esto es garantizado", "nadie puede predecir como yo",
                "voy a ser inmortal en las finanzas", "soy un oráculo", "esto es mi legado",
                "mi talento es sobrenatural", "esto es certeza", "nadie puede dudar de mí",
                "voy a revolucionar las inversiones", "soy un innovador", "esto es mi descubrimiento",
                "mi capacidad es ilimitada", "esto es inevitable", "nadie puede detenerme",
                "voy a ser un mito", "soy un fenómeno", "esto es mi creación",
                "mi genio es innegable", "esto es obvio", "nadie puede negar mi talento",
                "voy a ser recordado por siglos", "soy un titán", "esto es mi imperio",
                "mi sabiduría es ancestral", "esto es certeza absoluta", "nadie puede cuestionarme",
                "voy a trascender el tiempo", "soy un iluminado", "esto es mi revelación",
                "mi poder es infinito", "esto es inevitable", "nadie puede competir con mi nivel",
                "voy a ser un dios de las finanzas", "soy un semidiós", "esto es mi dominio",
                "mi conocimiento es cósmico", "esto es obvio", "nadie puede entender mi visión",
                "voy a controlar el mercado", "soy un maestro supremo", "esto es mi juego",
                "mi habilidad es sobrehumana", "esto es garantizado", "nadie puede igualarme",
                "voy a ser inmortal", "soy un legendario", "esto es mi obra maestra",
                "mi talento es divino", "esto es certeza", "nadie puede dudar de mi genio",
                "voy a cambiar las reglas", "soy un revolucionario", "esto es mi revolución",
                "mi capacidad es mágica", "esto es obvio", "nadie puede explicar mi éxito",
                "voy a ser un mito viviente", "soy un fenómeno único", "esto es mi magia",
                "mi intuición es infalible", "esto es garantizado", "nadie puede predecir como yo",
                "voy a ser recordado como el mejor", "soy incomparable", "esto es mi especialidad",
                "mi genio es innegable", "esto es evidente", "nadie puede negar mi talento",
                "voy a ser un referente", "soy un pionero", "esto es mi innovación",
                "mi habilidad es legendaria", "esto es obvio", "nadie puede igualar mi nivel",
                "voy a ser un ícono", "soy un símbolo", "esto es mi marca",
                "mi talento es único", "esto es garantizado", "nadie puede replicar mi éxito",
                "voy a ser un clásico", "soy atemporal", "esto es mi estilo",
                "mi capacidad es extraordinaria", "esto es evidente", "nadie puede cuestionarme",
                "voy a ser un maestro", "soy un experto", "esto es mi campo",
                "mi conocimiento es profundo", "esto es obvio", "nadie puede entender mi profundidad",
                "voy a ser un líder", "soy un guía", "esto es mi camino",
                "mi visión es clara", "esto es garantizado", "nadie puede ver lo que yo veo",
                "voy a ser un inspiración", "soy un modelo", "esto es mi ejemplo",
                "mi sabiduría es infinita", "esto es evidente", "nadie puede agotar mi conocimiento",
                "voy a ser un faro", "soy una luz", "esto es mi iluminación",
                "mi genio es brillante", "esto es obvio", "nadie puede apagar mi luz",
                "voy a ser una leyenda", "soy inmortal", "esto es mi historia"
            ],
            'loss_aversion': [
                "no quiero vender con pérdidas", "prefiero esperar a que suba", "me duele demasiado vender ahora",
                "no puedo vender por debajo de mi precio de compra", "voy a esperar a que recupere", "no voy a realizar esta pérdida",
                "mejor espero a que vuelva a subir", "no vendo con pérdidas nunca", "prefiero mantenerlo a vender perdiendo",
                "voy a aguantar hasta que recupere", "no puedo aceptar esta pérdida", "mejor lo dejo ahí",
                "no voy a vender en rojo", "esperaré a que suba", "prefiero no mirarlo hasta que recupere",
                "no puedo vender así", "voy a esperar pacientemente", "no quiero realizar esta pérdida",
                "mejor lo mantengo", "no vendo con pérdidas", "esperaré a que vuelva a mi precio",
                "no puedo aceptar vender perdiendo", "voy a aguantar", "prefiero esperar",
                "no voy a realizar pérdidas", "mejor espero", "no puedo vender así",
                "prefiero mantener la posición", "no vendo con rojo", "voy a esperar a que recupere",
                "no puedo vender por debajo", "mejor lo dejo", "esperaré a que suba",
                "no quiero aceptar la pérdida", "voy a aguantar", "prefiero no vender",
                "no puedo vender con pérdidas", "esperaré pacientemente", "mejor lo mantengo",
                "no voy a realizar esta pérdida", "prefiero esperar", "no puedo vender así",
                "mejor espero a que recupere", "no vendo con rojo", "voy a aguantar",
                "no puedo aceptar vender perdiendo", "prefiero mantenerlo", "esperaré",
                "no quiero realizar pérdidas", "voy a esperar", "mejor lo dejo ahí",
                "no puedo vender con pérdidas nunca", "prefiero aguantar", "no vendo así",
                "mejor espero pacientemente", "no voy a realizar esta pérdida", "prefiero mantener",
                "no puedo vender con rojo", "voy a esperar a que suba", "no quiero aceptar",
                "prefiero no vender", "no puedo vender con pérdidas", "mejor aguantar",
                "voy a esperar a que recupere", "no vendo con pérdidas", "prefiero mantener",
                "no puedo aceptar esta pérdida", "mejor espero", "no voy a realizar",
                "prefiero mantener la posición", "no puedo vender con rojo", "voy a aguantar",
                "no vendo con pérdidas nunca", "esperaré a que suba", "prefiero no mirar",
                "no puedo vender así", "mejor lo dejo ahí", "voy a esperar pacientemente",
                "prefiero esperar a que recupere", "no quiero realizar esta pérdida", "no puedo vender con rojo",
                "voy a aguantar hasta que suba", "no vendo con pérdidas", "prefiero mantener",
                "no puedo aceptar vender perdiendo", "mejor espero", "no voy a realizar",
                "prefiero no vender", "no puedo vender con pérdidas", "voy a esperar",
                "mejor lo mantengo", "no vendo con rojo", "esperaré pacientemente",
                "no puedo vender por debajo", "prefiero aguantar", "no quiero realizar",
                "voy a esperar a que recupere", "no vendo con pérdidas", "mejor mantener",
                "no puedo aceptar esta pérdida", "prefiero esperar", "no voy a vender",
                "mejor lo dejo ahí", "no puedo vender con rojo", "voy a aguantar",
                "prefiero mantener la posición", "no quiero realizar pérdidas", "esperaré",
                "no puedo vender con pérdidas nunca", "mejor esperar", "no vendo así",
                "voy a aguantar pacientemente", "no vendo con rojo", "prefiero mantener",
                "no puedo aceptar vender perdiendo", "esperaré a que suba", "mejor lo dejo",
                "prefiero no vender", "no puedo vender con pérdidas", "voy a esperar a que recupere",
                "mejor mantener", "no vendo con rojo", "no puedo aceptar",
                "voy a aguantar hasta que suba", "no quiero realizar esta pérdida", "prefiero esperar",
                "no puedo vender con pérdidas", "mejor lo mantengo", "no voy a realizar",
                "prefiero mantener la posición", "no puedo vender con rojo", "esperaré pacientemente",
                "no vendo con pérdidas nunca", "voy a esperar a que suba", "prefiero no mirar",
                "no puedo aceptar vender perdiendo", "mejor aguantar", "no quiero realizar",
                "prefiero esperar", "no puedo vender con rojo", "voy a mantener",
                "mejor lo dejo ahí", "no vendo con pérdidas", "esperaré pacientemente",
                "no puedo vender con pérdidas", "prefiero aguantar", "no voy a realizar",
                "voy a esperar a que recupere", "no vendo con rojo", "mejor mantener",
                "no puedo aceptar esta pérdida", "prefiero esperar", "no quiero vender",
                "mejor mantener la posición", "no puedo vender con pérdidas", "voy a aguantar",
                "prefiero no vender", "no vendo con rojo", "esperaré pacientemente",
                "no puedo vender con pérdidas nunca", "mejor esperar a que suba", "no voy a realizar",
                "voy a aguantar", "no quiero realizar esta pérdida", "prefiero mantener",
                "no puedo vender con rojo", "mejor esperar", "no vendo con pérdidas",
                "prefiero mantener", "no puedo aceptar vender perdiendo", "voy a esperar",
                "mejor lo dejo ahí", "no vendo con rojo", "prefiero aguantar",
                "no puedo vender con pérdidas", "esperaré pacientemente", "no voy a realizar",
                "prefiero esperar a que recupere", "no quiero vender con pérdidas", "mejor mantener",
                "voy a aguantar hasta que suba", "no vendo con rojo", "prefiero no vender",
                "no puedo aceptar esta pérdida", "mejor esperar", "no voy a realizar pérdidas",
                "prefiero mantener la posición", "no puedo vender con rojo", "voy a aguantar pacientemente",
                "no vendo con pérdidas nunca", "esperaré a que suba", "mejor lo mantengo",
                "no puedo vender así", "prefiero esperar", "no quiero realizar esta pérdida",
                "voy a esperar a que recupere", "no vendo con rojo", "prefiero mantener",
                "mejor aguantar", "no puedo vender con pérdidas", "esperaré pacientemente",
                "no voy a realizar esta pérdida", "prefiero no vender", "no puedo vender con rojo",
                "voy a esperar a que suba", "mejor mantener", "no vendo con pérdidas",
                "prefiero aguantar", "no puedo aceptar vender perdiendo", "esperaré pacientemente",
                "no quiero realizar pérdidas", "mejor lo dejo ahí", "no puedo vender con rojo",
                "voy a mantener", "prefiero esperar", "no vendo con pérdidas nunca"
            ],
            'anchoring': [
                "la compré a 200, no vendo por debajo de eso", "la compré a 50, tengo que esperar a que vuelva a 50",
                "mi precio de compra fue 100, no vendo por menos", "compré a 150, necesito que vuelva a ese nivel",
                "la compré a 30, mi punto de equilibrio es 30", "compré a 80, no puedo vender por debajo",
                "mi precio de entrada fue 120, espero ese nivel", "la compré a 25, necesito recuperar mi inversión",
                "compré a 200, ese es mi precio de referencia", "la compré a 60, no vendo hasta que vuelva a 60",
                "mi costo fue 90, ese es mi piso", "compré a 180, necesito ese precio para vender",
                "la compré a 40, ese es mi punto de equilibrio", "mi precio de compra fue 150, espero volver a ese nivel",
                "compré a 70, no vendo por debajo de 70", "la compré a 110, ese es mi precio base",
                "mi costo fue 45, necesito recuperar 45", "compré a 160, no vendo hasta que vuelva a 160",
                "la compré a 35, ese es mi precio de referencia", "mi precio de entrada fue 95, espero ese nivel",
                "compré a 140, necesito ese precio", "la compré a 55, no vendo por debajo de 55",
                "mi costo fue 85, ese es mi piso", "compré a 190, necesito volver a 190",
                "la compré a 28, ese es mi punto de equilibrio", "mi precio de compra fue 125, espero ese nivel",
                "compré a 75, no vendo por debajo", "la compré a 105, ese es mi precio base",
                "mi costo fue 50, necesito recuperar 50", "compré a 170, no vendo hasta ese precio",
                "la compré a 38, ese es mi precio de referencia", "mi precio de entrada fue 88, espero ese nivel",
                "compré a 145, necesito ese precio", "la compré a 58, no vendo por debajo de 58",
                "mi costo fue 92, ese es mi piso", "compré a 195, necesito volver a 195",
                "la compré a 32, ese es mi punto de equilibrio", "mi precio de compra fue 115, espero ese nivel",
                "compré a 78, no vendo por debajo", "la compré a 108, ese es mi precio base",
                "mi costo fue 48, necesito recuperar 48", "compré a 165, no vendo hasta ese precio",
                "la compré a 42, ese es mi precio de referencia", "mi precio de entrada fue 98, espero ese nivel",
                "compré a 148, necesito ese precio", "la compré a 62, no vendo por debajo de 62",
                "mi costo fue 86, ese es mi piso", "compré a 182, necesito volver a 182",
                "la compré a 36, ese es mi punto de equilibrio", "mi precio de compra fue 122, espero ese nivel",
                "compré a 72, no vendo por debajo", "la compré a 102, ese es mi precio base",
                "mi costo fue 52, necesito recuperar 52", "compré a 175, no vendo hasta ese precio",
                "la compré a 46, ese es mi precio de referencia", "mi precio de entrada fue 94, espero ese nivel",
                "compré a 152, necesito ese precio", "la compré a 56, no vendo por debajo de 56",
                "mi costo fue 88, ese es mi piso", "compré a 188, necesito volver a 188",
                "la compré a 34, ese es mi punto de equilibrio", "mi precio de compra fue 118, espero ese nivel",
                "compré a 76, no vendo por debajo", "la compré a 106, ese es mi precio base",
                "mi costo fue 44, necesito recuperar 44", "compré a 168, no vendo hasta ese precio",
                "la compré a 40, ese es mi precio de referencia", "mi precio de entrada fue 96, espero ese nivel",
                "compré a 150, necesito ese precio", "la compré a 60, no vendo por debajo de 60",
                "mi costo fue 84, ese es mi piso", "compré a 185, necesito volver a 185",
                "la compré a 30, ese es mi punto de equilibrio", "mi precio de compra fue 120, espero ese nivel",
                "compré a 74, no vendo por debajo", "la compré a 104, ese es mi precio base",
                "mi costo fue 46, necesito recuperar 46", "compré a 172, no vendo hasta ese precio",
                "la compré a 44, ese es mi precio de referencia", "mi precio de entrada fue 92, espero ese nivel",
                "compré a 146, necesito ese precio", "la compré a 54, no vendo por debajo de 54",
                "mi costo fue 82, ese es mi piso", "compré a 178, necesito volver a 178",
                "la compré a 38, ese es mi punto de equilibrio", "mi precio de compra fue 116, espero ese nivel",
                "compré a 70, no vendo por debajo", "la compré a 100, ese es mi precio base",
                "mi costo fue 42, necesito recuperar 42", "compré a 162, no vendo hasta ese precio",
                "la compré a 48, ese es mi precio de referencia", "mi precio de entrada fue 90, espero ese nivel",
                "compré a 154, necesito ese precio", "la compré a 58, no vendo por debajo de 58",
                "mi costo fue 80, ese es mi piso", "compré a 180, necesito volver a 180",
                "la compré a 32, ese es mi punto de equilibrio", "mi precio de compra fue 112, espero ese nivel",
                "compré a 68, no vendo por debajo", "la compré a 98, ese es mi precio base",
                "mi costo fue 40, necesito recuperar 40", "compré a 158, no vendo hasta ese precio",
                "la compré a 52, ese es mi precio de referencia", "mi precio de entrada fue 86, espero ese nivel",
                "compré a 144, necesito ese precio", "la compré a 50, no vendo por debajo de 50",
                "mi costo fue 78, ese es mi piso", "compré a 176, necesito volver a 176",
                "la compré a 26, ese es mi punto de equilibrio", "mi precio de compra fue 108, espero ese nivel",
                "compré a 66, no vendo por debajo", "la compré a 96, ese es mi precio base",
                "mi costo fue 38, necesito recuperar 38", "compré a 164, no vendo hasta ese precio",
                "la compré a 56, ese es mi precio de referencia", "mi precio de entrada fue 84, espero ese nivel",
                "compré a 142, necesito ese precio", "la compré a 46, no vendo por debajo de 46",
                "mi costo fue 76, ese es mi piso", "compré a 174, necesito volver a 174",
                "la compré a 24, ese es mi punto de equilibrio", "mi precio de compra fue 104, espero ese nivel",
                "compré a 64, no vendo por debajo", "la compré a 94, ese es mi precio base",
                "mi costo fue 36, necesito recuperar 36", "compré a 160, no vendo hasta ese precio",
                "la compré a 60, ese es mi precio de referencia", "mi precio de entrada fue 82, espero ese nivel",
                "compré a 140, necesito ese precio", "la compré a 42, no vendo por debajo de 42",
                "mi costo fue 74, ese es mi piso", "compré a 172, necesito volver a 172",
                "la compré a 22, ese es mi punto de equilibrio", "mi precio de compra fue 100, espero ese nivel",
                "compré a 62, no vendo por debajo", "la compré a 92, ese es mi precio base",
                "mi costo fue 34, necesito recuperar 34", "compré a 156, no vendo hasta ese precio",
                "la compré a 64, ese es mi precio de referencia", "mi precio de entrada fue 80, espero ese nivel",
                "compré a 138, necesito ese precio", "la compré a 38, no vendo por debajo de 38",
                "mi costo fue 72, ese es mi piso", "compré a 170, necesito volver a 170",
                "la compré a 20, ese es mi punto de equilibrio", "mi precio de compra fue 96, espero ese nivel",
                "compré a 60, no vendo por debajo", "la compré a 90, ese es mi precio base",
                "mi costo fue 32, necesito recuperar 32", "compré a 152, no vendo hasta ese precio"
            ]
        }
    
    def generar_dataset_intenciones(self) -> List[Dict]:
        """Generar 100 ejemplos por cada clase de intención"""
        dataset = []
        
        for intencion, ejemplos_base in self.intenciones.items():
            # Generar 100 ejemplos por intención
            for i in range(100):
                # Seleccionar un ejemplo base y modificarlo
                ejemplo_base = random.choice(ejemplos_base)
                
                # Variaciones para hacer más diverso el dataset
                variaciones = [
                    ejemplo_base,  # Original
                    ejemplo_base.lower(),  # Minúsculas
                    ejemplo_base.upper(),  # Mayúsculas
                    ejemplo_base.replace("¿", ""),  # Sin signos de interrogación
                    ejemplo_base + "!",  # Con exclamación
                    ejemplo_base + " por favor",  # Cortés
                    "oye " + ejemplo_base,  # Informal
                    ejemplo_base + " urgente",  # Urgente
                    ejemplo_base.replace("quiero", "necesito"),  # Sinónimo
                    ejemplo_base.replace("¿", "disculpa, ¿"),  # Más formal
                ]
                
                texto = random.choice(variaciones)
                
                # Agregar errores ortográficos aleatorios (10% de probabilidad)
                if random.random() < 0.1:
                    texto = self.agregar_errores_ortograficos(texto)
                
                dataset.append({
                    'texto': texto,
                    'intencion': intencion,
                    'sesgo': 'ninguno'  # Por defecto, los ejemplos de intención no tienen sesgo
                })
        
        return dataset
    
    def generar_dataset_sesgos(self) -> List[Dict]:
        """Generar 80 ejemplos por cada clase de sesgo"""
        dataset = []
        
        for sesgo, ejemplos_base in self.sesgos.items():
            # Generar 80 ejemplos por sesgo
            for i in range(80):
                # Seleccionar un ejemplo base y modificarlo
                ejemplo_base = random.choice(ejemplos_base)
                
                # Variaciones para hacer más diverso el dataset
                variaciones = [
                    ejemplo_base,  # Original
                    ejemplo_base.lower(),  # Minúsculas
                    ejemplo_base.upper(),  # Mayúsculas
                    ejemplo_base + "!!!",  # Múltiples exclamaciones
                    ejemplo_base + " por favor",  # Cortés
                    "ayuda " + ejemplo_base,  # Con ayuda
                    ejemplo_base + " ahora",  # Urgente
                    ejemplo_base.replace("estoy", "estoy muy"),  # Intensificador
                    ejemplo_base.replace("voy a", "tengo que"),  # Obligación
                    ejemplo_base.replace("no", "nunca"),  # Absoluto
                ]
                
                texto = random.choice(variaciones)
                
                # Agregar errores ortográficos aleatorios (15% de probabilidad)
                if random.random() < 0.15:
                    texto = self.agregar_errores_ortograficos(texto)
                
                dataset.append({
                    'texto': texto,
                    'intencion': 'pedir_recomendacion',  # Por defecto, los ejemplos de sesgo son recomendaciones
                    'sesgo': sesgo
                })
        
        return dataset
    
    def agregar_errores_ortograficos(self, texto: str) -> str:
        """Agregar errores ortográficos comunes para simular lenguaje coloquial"""
        errores = {
            'h': '',  # Omitir h
            'que': 'ke',  # Que por ke
            'quiero': 'kiero',  # Quiero por kiero
            'por': 'po',  # Por por po
            'para': 'pa',  # Para por pa
            'también': 'tambien',  # Sin tilde
            'más': 'mas',  # Sin tilde
            'sí': 'si',  # Sin tilde
            'estoy': 'toy',  # Contracción
            'voy': 'boi',  # Error común
            'está': 'ta',  # Contracción
            'con': 'kon',  # Error común
            'mi': 'mi' if random.random() < 0.5 else 'mi',  # Mantener o cambiar
        }
        
        for correcto, error in errores.items():
            if random.random() < 0.3:  # 30% de probabilidad de aplicar cada error
                texto = texto.replace(correcto, error)
        
        return texto
    
    def generar_dataset_completo(self) -> pd.DataFrame:
        """Generar el dataset completo combinando intenciones y sesgos"""
        print("Generando dataset de intenciones...")
        dataset_intenciones = self.generar_dataset_intenciones()
        
        print("Generando dataset de sesgos...")
        dataset_sesgos = self.generar_dataset_sesgos()
        
        # Combinar datasets
        dataset_completo = dataset_intenciones + dataset_sesgos
        
        # Mezclar aleatoriamente
        random.shuffle(dataset_completo)
        
        # Crear DataFrame
        df = pd.DataFrame(dataset_completo)
        
        return df
    
    def guardar_dataset(self, df: pd.DataFrame, ruta: str):
        """Guardar el dataset en formato CSV"""
        df.to_csv(ruta, index=False, encoding='utf-8')
        print(f"Dataset guardado en: {ruta}")
        print(f"Total de ejemplos: {len(df)}")
        print("\nDistribución por intención:")
        print(df['intencion'].value_counts())
        print("\nDistribución por sesgo:")
        print(df['sesgo'].value_counts())

if __name__ == "__main__":
    generator = DatasetGenerator()
    df = generator.generar_dataset_completo()
    generator.guardar_dataset(df, "sipa_v2/data/datasets/bias_intent_dataset.csv")
