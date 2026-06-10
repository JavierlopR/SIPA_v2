# -*- coding: utf-8 -*-
"""
SIPA v2 - Analizador de Volatilidad y Anomalías de Mercado
Módulo encargado de descargar o simular datos financieros, calcular
volatilidad móvil y realizar detección estadística de anomalías (Z-Score).
"""

import yfinance as yf
import pandas as pd
import numpy as np
import os
import sys

# Forzar codificación UTF-8 para evitar caídas de consola en Windows
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Nombres descriptivos para los tickers principales
TICKERS_DICT = {
    # LATAM / México (GBM+, Fintual, Hey Banco)
    "^MXX": "Índice IPC (Bolsa Mexicana)",
    "CEMEXCPO.MX": "Cemex CPO (Construcción)",
    "WALMEX.MX": "Walmart de México (Consumo)",
    # Europa (Trade Republic, Scalable Capital, BBVA Trader, Openbank)
    "SXR8.DE": "iShares Core S&P 500 ETF (Alemania)",
    "EUNL.DE": "iShares Core MSCI World ETF (Alemania)",
    "SAN.MC": "Banco Santander (España)",
    # Global / EEUU (Revolut, Interactive Brokers, Robinhood)
    "AAPL": "Apple Inc. (Tecnología)",
    "TSLA": "Tesla Inc. (Automotriz/IA)",
    "BTC-USD": "Bitcoin USD (Criptomonedas)",
    "ETH-USD": "Ethereum USD (Criptomonedas)"
}

def generate_fallback_data(ticker: str, period: str = "2y") -> pd.DataFrame:
    """
    Genera un dataset de datos simulados realista si falla yfinance.
    Esto garantiza la robustez 'Zero-Setup' y que la app funcione offline.
    """
    print(f"⚠️ Generando datos simulados de respaldo para el ticker: {ticker} ({period})")
    
    # Determinar longitud de fechas en base al período solicitado
    days = 504 if period == "2y" else (252 if period == "1y" else 1260)
    end_date = pd.Timestamp.now().normalize() # Normalizar para evitar problemas de horas
    dates = pd.date_range(end=end_date, periods=days, freq='B') # Días hábiles
    days = len(dates) # Ajuste dinámico a la longitud real del índice de fechas
    
    # Semilla fija basada en el ticker para que siempre devuelva el mismo gráfico simulado
    seed_val = sum(ord(c) for c in ticker)
    np.random.seed(seed_val)
    
    # Parámetros base del ticker
    base_price = 100.0
    drift = 0.0002  # Pequeña tendencia alcista diaria
    volatility = 0.015 # Volatilidad diaria base
    
    # Personalización según activo
    if "BTC" in ticker or "ETH" in ticker:
        volatility = 0.035 # Cripto es muy volátil
        drift = 0.0006
        base_price = 45000.0 if "BTC" in ticker else 2800.0
    elif "TSLA" in ticker:
        volatility = 0.025
        base_price = 180.0
    elif "AAPL" in ticker:
        volatility = 0.012
        base_price = 175.0
    elif "^MXX" in ticker:
        volatility = 0.009
        base_price = 56000.0
    elif "ETF" in ticker or "SXR8" in ticker or "EUNL" in ticker:
        volatility = 0.008
        base_price = 450.0
        drift = 0.0003
        
    # Caminata aleatoria geométrica (Geometric Brownian Motion)
    # Log-retornos normales
    log_returns = np.random.normal(drift - 0.5 * volatility**2, volatility, days)
    
    # Introducir algunas anomalías artificiales brutales (para fines educativos)
    # 3 anomalías negativas extremas (pánicos) y 2 positivas (euforia)
    panic_idx = np.random.choice(days, 3, replace=False)
    for idx in panic_idx:
        log_returns[idx] = -volatility * 4.5 # Caída extrema
        
    euphoria_idx = np.random.choice(days, 2, replace=False)
    for idx in euphoria_idx:
        log_returns[idx] = volatility * 4.0 # Subida extrema
        
    # Calcular precios acumulados
    price_multipliers = np.exp(np.cumsum(log_returns))
    prices = base_price * price_multipliers
    
    # Crear DataFrame
    df = pd.DataFrame(index=dates)
    df['Open'] = prices * (1 - np.random.uniform(0, 0.003, days))
    df['High'] = prices * (1 + np.random.uniform(0, 0.01, days))
    df['Low'] = prices * (1 - np.random.uniform(0, 0.01, days))
    df['Close'] = prices
    
    # Asegurar mínimos lógicos
    df['High'] = np.maximum(df['High'], np.maximum(df['Open'], df['Close']))
    df['Low'] = np.minimum(df['Low'], np.minimum(df['Open'], df['Close']))
    
    # Generar volumen realista con picos en días anómalos
    base_volume = 1000000.0
    volumes = np.random.lognormal(np.log(base_volume), 0.5, days)
    # El volumen se dispara 4x en días de anomalías
    for idx in list(panic_idx) + list(euphoria_idx):
        volumes[idx] = volumes[idx] * np.random.uniform(3.5, 6.0)
        
    df['Volume'] = volumes.astype(int)
    
    return df

def get_market_data(ticker: str, period: str = "2y") -> pd.DataFrame:
    """
    Descarga cotizaciones desde Yahoo Finance de forma segura.
    Si hay un fallo de red o el ticker no existe, recurre al simulador.
    """
    # Limpiar ticker
    ticker = ticker.strip()
    
    try:
        print(f"📥 Intentando descargar datos reales de Yahoo Finance para {ticker} ({period})...")
        # Descarga con hilos apagados para mayor estabilidad local
        df = yf.download(ticker, period=period, progress=False, group_by='ticker')
        
        # yfinance con Pandas 2.0+ a veces devuelve un MultiIndex si es un solo ticker
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(1)
            
        if df.empty or 'Close' not in df.columns:
            raise ValueError("Datos descargados vacíos o corruptos.")
            
        print("✅ Descarga exitosa de datos reales!")
        # Forzar que el índice sea DatetimeIndex
        df.index = pd.to_datetime(df.index)
        return df
        
    except Exception as e:
        print(f"❌ Error al descargar datos reales para {ticker}: {str(e)}")
        return generate_fallback_data(ticker, period)

def calculate_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula los retornos diarios y la volatilidad histórica móvil
    anualizada a corto plazo (21 días hábiles, ~1 mes) y largo plazo (252 días, ~1 año).
    """
    # 1. Copiar df para no mutar el original
    df = df.copy()
    
    # 2. Retorno diario porcentual
    df['Return'] = df['Close'].pct_change()
    
    # 3. Volatilidad móvil de 21 días (anualizada)
    # Multiplicamos por la raíz cuadrada de 252 (días de negociación anuales)
    df['Vol_21'] = df['Return'].rolling(window=21).std() * np.sqrt(252)
    
    # 4. Volatilidad móvil de 252 días (anualizada)
    df['Vol_252'] = df['Return'].rolling(window=252).std() * np.sqrt(252)
    
    # Rellenar los primeros valores NaN creados por las medias móviles
    df['Return'] = df['Return'].fillna(0)
    df['Vol_21'] = df['Vol_21'].ffill().bfill().fillna(0)
    df['Vol_252'] = df['Vol_252'].ffill().bfill().fillna(0)
    
    return df

def detect_anomalies(df: pd.DataFrame, z_threshold: float = 2.5) -> pd.DataFrame:
    """
    Detecta anomalías de precios (Z-Score extremo del retorno)
    y anomalías de volumen (volumen > 3 veces el promedio móvil de 21 días).
    """
    df = df.copy()
    
    # Evitar división por cero en activos planos
    ret_std = df['Return'].std()
    if ret_std == 0 or np.isnan(ret_std):
        df['Return_Z'] = 0
    else:
        df['Return_Z'] = (df['Return'] - df['Return'].mean()) / ret_std
        
    # Clasificación de anomalías de precio
    df['Anomaly_Type'] = 'Normal'
    df.loc[df['Return_Z'] > z_threshold, 'Anomaly_Type'] = 'Euforia'
    df.loc[df['Return_Z'] < -z_threshold, 'Anomaly_Type'] = 'Pánico'
    
    # Anomalía numérica de precio (guarda el valor de retorno si es anomalía, 0 si es normal)
    df['Anomaly_Price'] = np.where(df['Anomaly_Type'] != 'Normal', df['Return'], 0)
    
    # Detección de anomalía de volumen
    # Volumen promedio móvil de 21 días
    df['Vol_MA21'] = df['Volume'].rolling(window=21).mean()
    df['Vol_MA21'] = df['Vol_MA21'].ffill().bfill().fillna(1.0) # Evitar ceros
    
    # Anomalía si el volumen del día actual supera 3 veces el promedio móvil
    df['Anomaly_Volume'] = df['Volume'] > (3.0 * df['Vol_MA21'])
    
    return df

def get_educational_explanation(anomaly_type: str, z_score: float, ticker: str) -> str:
    """
    Devuelve explicaciones conductuales y científicas detalladas de una anomalía
    específica en lenguaje sencillo y amigable para un principiante.
    """
    nombre_activo = TICKERS_DICT.get(ticker, ticker)
    z_abs = abs(z_score)
    
    if anomaly_type == 'Pánico':
        return (
            f"📉 **¿Qué pasó aquí? (Anomalía de Pánico):** El retorno de {nombre_activo} se desvió "
            f"**{z_abs:.2f} veces** por debajo de su promedio diario normal. \n"
            f"💡 **La Psicología del Mercado:** Este tipo de caída extrema suele ser provocado por la "
            f"**Aversión a la Pérdida colectiva**. Ante malas noticias o caídas iniciales, los inversores "
            f"sufren pánico psicológico y deciden vender de golpe para evitar más dolor, empujando el precio "
            f"irracionalmente hacia abajo. \n"
            f"🛡️ **Lección SIPA:** Vender en estos días de capitulación congela pérdidas definitivas. Históricamente, "
            f"los mercados se recuperan en el mediano y largo plazo. ¡Mantén tu tesis y respira antes de actuar!"
        )
    elif anomaly_type == 'Euforia':
        return (
            f"📈 **¿Qué pasó aquí? (Anomalía de Euforia):** El retorno de {nombre_activo} se disparó "
            f"**{z_abs:.2f} veces** por encima de su promedio diario normal. \n"
            f"💡 **La Psicología del Mercado:** Este estallido alcista suele estar impulsado por el "
            f"**FOMO colectivizado**. El miedo de quedarse fuera de las ganancias hace que multitudes "
            f"de inversores minoristas e institucionales compren de forma masiva e impulsiva, creyendo que subirá "
            f"para siempre. \n"
            f"🛡️ **Lección SIPA:** Comprar en máximos históricos inducido por la euforia expone tu cartera "
            f"a un alto riesgo de retroceso. Nadie puede predecir la cima; invierte con un plan recurrente y diversificado."
        )
    else:
        return "El mercado se comporta dentro de los parámetros normales de fluctuación aleatoria."

# Prueba local del módulo
if __name__ == "__main__":
    print("Testing market analysis module...")
    # Probar con un ticker real
    df_real = get_market_data("AAPL", period="1y")
    df_real = calculate_volatility(df_real)
    df_real = detect_anomalies(df_real)
    
    print("\n--- Apple Inc. Real Data Summary ---")
    print(f"Data shape: {df_real.shape}")
    print(f"Average Annual Volatility (252d): {df_real['Vol_252'].mean() * 100:.2f}%")
    anom_counts = df_real['Anomaly_Type'].value_counts()
    print(f"Anomalies detected: {anom_counts.to_dict()}")
    
    # Probar con ticker inválido (debe disparar fallback)
    df_fake = get_market_data("INVALID_TICKER", period="1y")
    df_fake = calculate_volatility(df_fake)
    df_fake = detect_anomalies(df_fake)
    
    print("\n--- Invalid Ticker Fallback Summary ---")
    print(f"Fallback Data shape: {df_fake.shape}")
    print(f"Average Annual Volatility (252d): {df_fake['Vol_252'].mean() * 100:.2f}%")
    anom_counts_fake = df_fake['Anomaly_Type'].value_counts()
    print(f"Fallback Anomalies detected: {anom_counts_fake.to_dict()}")
