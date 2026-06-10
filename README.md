# SIPA v2 — Coach Financiero Personal con Deep Learning Multimodal

Una arquitectura para democratizar el asesoramiento de inversión con detección de sesgos cognitivos.

## Estructura del Proyecto

```
sipa_v2/
├── docs/                    # Documentación y capítulos
├── src/                     # Código fuente
│   ├── models/             # Modelos de Deep Learning
│   ├── data/               # Pipeline de datos
│   ├── evaluation/         # Evaluación y métricas
│   └── orchestration/      # Capa de orquestación
├── experiments/            # Experimentos y resultados
├── tests/                  # Tests unitarios
└── requirements.txt        # Dependencias
```

## Arquitectura Propuesta

### Componentes Principales
1. **Predictor de volatilidad con Bi-LSTM**
2. **Detector de anomalías con VAE**
3. **Clasificador de sesgos cognitivos con Transformer**
4. **Sistema conversacional con LLM + RAG**
5. **Optimizador de cartera con Deep RL (PPO)**
6. **Capa de orquestación y guardrails**

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

Ver documentación en `docs/` para detalles de implementación y evaluación.
