# -*- coding: utf-8 -*-
"""
SIPA v2 - Entrenador del Clasificador de Intención y Sesgos Cognitivos
Entrena un modelo de alta precisión utilizando el dataset verificado
para categorizar el estado psicológico y la intención del usuario.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Forzar codificación UTF-8
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Directorios de SIPA v2
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'datasets', 'bias_intent_dataset_corrected.csv')
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models', 'intent_bias')

def train_classifier():
    print("=" * 60)
    print("🧠 ENTRENANDO EL CEREBRO DE SIPA V2: INTENCIONES Y SESGOS")
    print("=" * 60)
    
    # 1. Cargar el dataset
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: No se encontró el dataset en {DATA_PATH}")
        sys.exit(1)
        
    print(f"📥 Cargando datos desde: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"📊 Registros totales: {len(df)}")
    
    # Mostrar la distribución del dataset
    print("\n📈 Distribución de Intenciones:")
    print(df['intencion'].value_counts())
    print("\n📈 Distribución de Sesgos Cognitivos:")
    print(df['sesgo'].value_counts())
    
    # 2. División de datos (80% entrenamiento, 20% prueba)
    print("\n✂️ Dividiendo datos para entrenamiento y validación...")
    
    X = df['texto'].astype(str)
    y_intent = df['intencion']
    y_bias = df['sesgo']
    
    # Split para Intenciones
    X_train_int, X_test_int, y_train_int, y_test_int = train_test_split(
        X, y_intent, test_size=0.2, random_state=42, stratify=y_intent
    )
    
    # Split para Sesgos
    X_train_bias, X_test_bias, y_train_bias, y_test_bias = train_test_split(
        X, y_bias, test_size=0.2, random_state=42, stratify=y_bias
    )
    
    # 3. Construir pipelines con TF-IDF y Regresión Logística
    # Usamos n-gramas (1, 2) para capturar frases completas como "vendo todo" o "no quiero"
    print("\n⚙️ Construyendo pipelines de Machine Learning...")
    
    intent_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=2,
            max_df=0.8
        )),
        ('clf', LogisticRegression(
            C=2.0,
            class_weight='balanced',
            max_iter=500,
            random_state=42
        ))
    ])
    
    bias_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=2,
            max_df=0.8
        )),
        ('clf', LogisticRegression(
            C=2.0,
            class_weight='balanced',
            max_iter=500,
            random_state=42
        ))
    ])
    
    # 4. Entrenar modelos
    print("🏋️ Entrenando clasificador de INTENCIÓN...")
    intent_pipeline.fit(X_train_int, y_train_int)
    
    print("🏋️ Entrenando clasificador de SESGOS COGNITIVOS...")
    bias_pipeline.fit(X_train_bias, y_train_bias)
    
    # 5. Evaluar modelos
    print("\n" + "=" * 50)
    print("📊 RESULTADOS DE LA EVALUACIÓN (TEST)")
    print("=" * 50)
    
    # Evaluación Intención
    y_pred_int = intent_pipeline.predict(X_test_int)
    acc_int = accuracy_score(y_test_int, y_pred_int)
    print(f"\n🎯 CLASIFICADOR DE INTENCIÓN — Accuracy: {acc_int * 100:.2f}%")
    print(classification_report(y_test_int, y_pred_int))
    
    # Evaluación Sesgo
    y_pred_bias = bias_pipeline.predict(X_test_bias)
    acc_bias = accuracy_score(y_test_bias, y_pred_bias)
    print(f"\n🧠 CLASIFICADOR DE SESGOS — Accuracy: {acc_bias * 100:.2f}%")
    print(classification_report(y_test_bias, y_pred_bias))
    
    # 6. Crear el directorio de modelos si no existe y guardar
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    intent_model_path = os.path.join(MODEL_DIR, 'intent_model.joblib')
    bias_model_path = os.path.join(MODEL_DIR, 'bias_model.joblib')
    
    print(f"\n💾 Guardando modelos en: {MODEL_DIR}...")
    joblib.dump(intent_pipeline, intent_model_path)
    joblib.dump(bias_pipeline, bias_model_path)
    print("✅ Modelos guardados con éxito!")
    
    # 7. Prueba rápida de predicción
    print("\n🔮 PRUEBA RÁPIDA DE PREDICCIÓN:")
    test_phrases = [
        "¡VENDO TODO! Esto se hunde de inmediato",
        "¿Debería meter dinero en NVDA? Todos están ganando menos yo",
        "¿Cuánto vale mi cartera actual?",
        "Tengo una buena sensación sobre Tesla, sé que va a subir seguro",
        "¿Me explicas qué es el RSI y cómo se usa?"
    ]
    
    for phrase in test_phrases:
        pred_i = intent_pipeline.predict([phrase])[0]
        pred_b = bias_pipeline.predict([phrase])[0]
        probs_b = bias_pipeline.predict_proba([phrase])[0]
        max_prob_b = max(probs_b)
        classes_b = bias_pipeline.classes_
        
        print("-" * 50)
        print(f"Texto: \"{phrase}\"")
        print(f"👉 Intención detectada: {pred_i}")
        print(f"👉 Sesgo detectado:      {pred_b} ({max_prob_b * 100:.1f}% confianza)")
        
    print("\n🚀 Fase 1 completada exitosamente.")

if __name__ == "__main__":
    train_classifier()
