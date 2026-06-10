# 🧠 SIPA v2 — Personal Finance & Psychological Investment Coach

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JavierlopR/SIPA_v2/blob/main/notebooks/SIPA_v2_Colab.ipynb)

**SIPA v2** es una plataforma educativa interactiva premium diseñada para inversores principiantes. Su propósito central es **desmitificar la ilusión de predecir el futuro del mercado** y orientar al usuario hacia la gestión de riesgos, la diversificación y la comprensión de su propia psicología financiera mediante inteligencia artificial.

---

## 💎 Características Principales

*   **Brain NLP Local (Scikit-Learn):** Un clasificador de alta velocidad que analiza tu texto en tiempo real y detecta **5 sesgos cognitivos financieros** (FOMO, Pánico, Exceso de Confianza, Aversión a la Pérdida, Anclaje) con más del **95.8% de precisión**.
*   **Coach Psicológico Híbrido:** Te brinda asesoramiento conductual empático. Funciona 100% gratis en local mediante un sistema experto de reglas, y soporta modo híbrido conectando **OpenAI GPT-4o-mini** si introduces tu API Key.
*   **Guía de 10 Brokers Online:** Análisis conductual detallado de las trampas de diseño de interfaces (UX) y guías de inicio para **GBM+, Trade Republic, Revolut, Scalable Capital, Interactive Brokers, Fintual, Hey Banco, BBVA Trader, Openbank y Robinhood**.
*   **Laboratorio de Volatilidad y Anomalías:** Gráficos interactivos de Plotly que muestran precios en tiempo real con **anomalías estadísticas marcadas vía Z-Score** e históricos de volatilidad rodante anualizada (21 y 252 días).
*   **Simulador de Respaldo Auto-sanable:** Generador de cotizaciones realista basado en Movimiento Browniano Geométrico por si falla Yahoo Finance o estás sin conexión a internet.

---

## 🚀 Ejecución en Google Colab

Puedes arrancar y usar SIPA v2 de manera inmediata sin instalar nada en tu computadora:

1.  Haz clic en el botón de arriba **"Open In Colab"**.
2.  Ejecuta las celdas en orden.
3.  La última celda generará un túnel público seguro a través de Cloudflare. Haz clic en el enlace que termina en `.trycloudflare.com` para abrir la aplicación web.

---

## 💻 Ejecución Local

### 1. Requisitos Previos

Asegúrate de tener Python 3.10+ instalado. Instala las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt
```

### 2. Entrenar el Modelo NLP

Antes de iniciar la app por primera vez, genera el dataset limpio y entrena el clasificador local:

```bash
python data/generate_dataset_corrected.py
python src/classifier.py
```

### 3. Arrancar la Aplicación

Inicia el servidor local de Streamlit mediante el script de arranque rápido:

```bash
python run_sipa_v2.py
```

Si no se abre automáticamente en tu navegador, ingresa a: **[http://localhost:8501](http://localhost:8501)**

