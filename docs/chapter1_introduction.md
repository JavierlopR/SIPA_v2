# Capítulo 1: Introducción y Motivación

## 1.1 Por qué el análisis técnico falla en retail

### Limitaciones del Análisis Técnico Tradicional

**Literatura existente:**
- **Malkiel (1973)**: "A Random Walk Down Wall Street" - evidencia de eficiencia de mercados
- **Fama (1970)**: Efficient Market Hypothesis - precios reflejan toda información disponible
- **Lo & MacKinlay (1999)**: "A Non-Random Walk Down Wall Street" - algunas anomalías pero limitadas

**Problemas específicos para inversores retail:**
1. **Sesgos de confirmación**: tendencia a interpretar señales que confirman creencias previas
2. **Overfitting**: exceso de optimización en backtests históricos
3. **Costes de transacción**: erosionan ganancias de estrategias de alta frecuencia
4. **Latencia de información**: retail accede información después de institucionales

### Evidencia Empírica de Fracaso

- **Barber & Odean (2000)**: "Trading is hazardous to your wealth" - inversores activos underperforman
- **Statman (2014)**: "What Investors Really Want" - gap entre racionalidad y comportamiento real

## 1.2 Limitaciones de Robo-Advisors Actuales

### Enfoques Tradicionales

**Markowitz (1952) - Modern Portfolio Theory:**
- ```python
  # Optimización media-varianza clásica
  minimize: σ²_p = w'Σw
  subject to: w'μ = μ_target, Σw = 1
  ```
- Limitaciones: asume normalidad de retornos, varianza como única medida de riesgo

**Black-Litterman (1992):**
- Incorpora views del inversor
- Problema: requiere calibración compleja de parámetros

### Robo-Advisors Comerciales

**Limitaciones identificadas:**
1. **Estrategias pasivas**: principalmente ETF-based, sin adaptación dinámica
2. **Modelos simplificados**: ignoran tail risks y correlaciones no-lineales
3. **One-size-fits-all**: perfiles de riesgo demasiado genéricos
4. **Sin detección de sesgos**: no monitorean comportamiento del inversor

## 1.3 Hipótesis: Combinar DL Multimodal + Behavioral Finance

### Propuesta de Valor

**Hipótesis principal:**
> La combinación de Deep Learning multimodal con principios de behavioral finance puede crear un sistema de asesoramiento financiero que supera tanto las limitaciones del análisis técnico tradicional como las de los robo-advisors actuales.

### Componentes Clave

1. **Análisis multimodal**: Combina datos de mercado, sentimiento, y comportamiento del usuario
2. **Detección de sesgos**: Identificación en tiempo real de sesgos cognitivos
3. **Adaptación dinámica**: Rebalanceo basado en condiciones de mercado y perfil del usuario
4. **Explicabilidad**: Interfaces conversacionales que explican decisiones

### Contribuciones Esperadas

1. **Académicas**: Primera arquitectura que integra DL multimodal + behavioral finance
2. **Prácticas**: Sistema accesible para inversores retail con costes reducidos
3. **Metodológicas**: Framework de evaluación que combina métricas financieras y de usabilidad

## 1.4 Objetivos de la Investigación

### Objetivo General
Desarrollar y validar una arquitectura de coach financiero personal que democratice el asesoramiento de inversión mediante deep learning multimodal y detección de sesgos cognitivos.

### Objetivos Específicos

1. **OD1**: Diseñar e implementar predictores de volatilidad con Bi-LSTM que superen modelos GARCH tradicionales
2. **OD2**: Desarrollar sistemas de detección de anomalías con VAE para identificación de riesgos extremos
3. **OD3**: Crear clasificadores de sesgos cognitivos con Transformers fine-tuned para behavioral finance
4. **OD4**: Implementar sistema conversacional con LLM + RAG para explicabilidad y educación
5. **OD5**: Optimizar carteras con Deep RL (PPO) que adapten estrategias dinámicamente
6. **OD6**: Validar experimentalmente la superioridad del sistema propuesto vs benchmarks

## 1.5 Estructura del Documento

- **Capítulo 2**: Estado del arte y gap identificado
- **Capítulo 3**: Arquitectura técnica detallada
- **Capítulo 4**: Implementación y pipeline de datos
- **Capítulo 5**: Evaluación experimental y resultados
- **Capítulo 6**: Aplicaciones empresariales y consideraciones éticas
- **Capítulo 7**: Conclusiones y trabajo futuro
