# -*- coding: utf-8 -*-
"""
SIPA v2 - Analizador de Volatilidad, Anomalías y Auditoría de Activos en Tiempo Real
"""

import yfinance as yf
import pandas as pd
import numpy as np
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ---------------------------------------------------------------------------
# Catálogo de tickers con nombre descriptivo
# ---------------------------------------------------------------------------
TICKERS_DICT = {
    # Índices
    "^MXX": "Índice IPC (Bolsa Mexicana)",
    "^GSPC": "S&P 500 (EEUU)",
    "^IXIC": "NASDAQ Composite",
    "^DJI": "Dow Jones Industrial",
    "^STOXX50E": "Euro Stoxx 50 (Europa)",
    # ETFs
    "SXR8.DE": "iShares Core S&P 500 ETF (Alemania)",
    "EUNL.DE": "iShares Core MSCI World ETF (Alemania)",
    "SPY": "SPDR S&P 500 ETF Trust",
    "QQQ": "Invesco QQQ Trust (NASDAQ)",
    "VWRA.L": "Vanguard FTSE All-World ETF",
    # Acciones globales
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "GOOGL": "Alphabet (Google)",
    "AMZN": "Amazon.com Inc.",
    "NVDA": "NVIDIA Corp.",
    "META": "Meta Platforms (Facebook)",
    "TSLA": "Tesla Inc.",
    "NFLX": "Netflix Inc.",
    "BRKB": "Berkshire Hathaway B",
    "JPM": "JPMorgan Chase & Co.",
    "V": "Visa Inc.",
    "WMT": "Walmart Inc.",
    # España / Europa
    "SAN.MC": "Banco Santander (España)",
    "BBVA.MC": "BBVA (España)",
    "ITX.MC": "Inditex / Zara (España)",
    "AMS.MC": "Amadeus IT Group",
    "ASML.AS": "ASML Holding (Países Bajos)",
    "SAP.DE": "SAP SE (Alemania)",
    # LATAM
    "CEMEXCPO.MX": "Cemex CPO (México)",
    "WALMEX.MX": "Walmart de México",
    "AMXL.MX": "América Móvil (México)",
    # Cripto
    "BTC-USD": "Bitcoin (BTC)",
    "ETH-USD": "Ethereum (ETH)",
    "SOL-USD": "Solana (SOL)",
    "BNB-USD": "BNB (Binance Coin)",
}

# ---------------------------------------------------------------------------
# Mapa de sinónimos en texto libre → ticker Yahoo Finance
# ---------------------------------------------------------------------------
SYNONYM_MAP = {
    # Apple
    r"\bapple\b|\baapl\b|\baaple\b": "AAPL",
    # Microsoft
    r"\bmicrosoft\b|\bmsft\b|\bwindows stock\b": "MSFT",
    # Google / Alphabet
    r"\bgoogle\b|\bgoogol\b|\balphabet\b|\bgoogl\b|\bgoog\b": "GOOGL",
    # Amazon
    r"\bamazon\b|\bamzn\b|\baws stock\b": "AMZN",
    # NVIDIA
    r"\bnvidia\b|\bnvda\b|\bnvidea\b": "NVDA",
    # Meta / Facebook
    r"\bmeta\b|\bfacebook\b|\binstagram stock\b|\bfb\b": "META",
    # Tesla
    r"\btesla\b|\btsla\b|\belon stock\b": "TSLA",
    # Netflix
    r"\bnetflix\b|\bnflx\b": "NFLX",
    # Visa
    r"\bvisa\b|\b\bv\b": "V",
    # Walmart
    r"\bwalmart\b|\bwmt\b": "WMT",
    # Bitcoin
    r"\bbitcoin\b|\bbtc\b|\bbtc-usd\b|\bbitcoi\b": "BTC-USD",
    # Ethereum
    r"\bethereum\b|\beth\b|\beth-usd\b|\bether\b": "ETH-USD",
    # Solana
    r"\bsolana\b|\bsol\b|\bsol-usd\b": "SOL-USD",
    # S&P 500 / SPY
    r"\bs&p\b|\bsp500\b|\bspx\b|\bspy\b|\bsnp500\b|\bsp 500\b|\bstandard.{0,5}poors\b": "SPY",
    # NASDAQ
    r"\bnasdaq\b|\bqqq\b|\btech index\b": "QQQ",
    # Santander
    r"\bsantander\b|\bsan\b": "SAN.MC",
    # BBVA
    r"\bbbva\b": "BBVA.MC",
    # Inditex / Zara
    r"\binditex\b|\bzara\b|\bitx\b": "ITX.MC",
    # ASML
    r"\basml\b": "ASML.AS",
    # Berkshire
    r"\bberkshire\b|\bbrk\b|\bwarren buffett stock\b": "BRKB",
    # JPMorgan
    r"\bjpmorgan\b|\bjpm\b|\bjp morgan\b": "JPM",
}


def extract_ticker_from_text(text: str) -> str | None:
    """
    Detecta si el usuario menciona un activo conocido en su mensaje.
    Devuelve el ticker de Yahoo Finance o None si no se detecta nada.
    """
    text_lower = text.lower()
    for pattern, ticker in SYNONYM_MAP.items():
        if re.search(pattern, text_lower):
            return ticker
    # Buscar tickers en formato $TICKER o TICKER en mayúsculas (ej. $NVDA, AAPL)
    dollar_match = re.search(r'\$([A-Z]{1,5})', text)
    if dollar_match:
        candidate = dollar_match.group(1)
        if candidate in TICKERS_DICT:
            return candidate
    caps_match = re.search(r'\b([A-Z]{2,5})\b', text)
    if caps_match:
        candidate = caps_match.group(1)
        if candidate in TICKERS_DICT:
            return candidate
    return None


def _calc_rsi(series: pd.Series, period: int = 14) -> float:
    """Calcula el RSI (Relative Strength Index) del último valor disponible."""
    delta = series.diff().dropna()
    if len(delta) < period:
        return 50.0  # valor neutro si no hay datos suficientes
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean().iloc[-1]
    avg_loss = loss.rolling(window=period, min_periods=period).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100.0 - (100.0 / (1.0 + rs)), 2)


def get_ticker_audit(ticker: str) -> dict:
    """
    Descarga los últimos 90 días de cotización de un activo y devuelve
    un diccionario con métricas técnicas y un veredicto cualitativo.

    Métricas calculadas:
      - precio_actual, retorno_hoy (%)
      - rsi_14: RSI de 14 días
      - sma_50: Media Móvil Simple de 50 días
      - distancia_sma (%): Cuánto está el precio por encima/debajo de la SMA50
      - zscore_hoy: Z-Score del retorno de hoy vs historial 90d
      - vol_anualizada: Volatilidad anualizada (21d)
      - estado_tecnico: "sobrecomprado" | "sobrevendido" | "neutral"
      - alerta_tecnica: Texto diagnóstico para el coach
      - nombre: Nombre descriptivo
      - ticker: Ticker confirmado
      - simulado: bool (True si los datos son simulados por falta de conexión)
    """
    nombre = TICKERS_DICT.get(ticker, ticker)
    resultado_base = {
        "ticker": ticker,
        "nombre": nombre,
        "simulado": False,
        "precio_actual": None,
        "retorno_hoy": None,
        "rsi_14": None,
        "sma_50": None,
        "distancia_sma": None,
        "zscore_hoy": None,
        "vol_anualizada": None,
        "estado_tecnico": "desconocido",
        "alerta_tecnica": "No se pudieron obtener datos suficientes para este activo.",
    }

    try:
        df = yf.download(ticker, period="6mo", progress=False)
        # Flatten MultiIndex si existe (yfinance >= 0.2.x devuelve MultiIndex siempre)
        if isinstance(df.columns, pd.MultiIndex):
            # Nivel 0 = campo (Close, Open, ...), nivel 1 = ticker
            df.columns = df.columns.get_level_values(0)
        if df.empty or "Close" not in df.columns or len(df) < 15:
            raise ValueError("Datos insuficientes")
        df.index = pd.to_datetime(df.index)
        close = df["Close"].squeeze().dropna()

        # Métricas básicas
        precio_actual = float(close.iloc[-1])
        precio_anterior = float(close.iloc[-2]) if len(close) > 1 else precio_actual
        retorno_hoy = round((precio_actual - precio_anterior) / precio_anterior * 100, 3)

        # RSI 14
        rsi_14 = _calc_rsi(close, period=14)

        # SMA 50 (si no hay 50 días, usamos lo que hay)
        sma_window = min(50, len(close) - 1)
        sma_50 = round(float(close.rolling(window=sma_window).mean().iloc[-1]), 4)
        distancia_sma = round((precio_actual - sma_50) / sma_50 * 100, 2) if sma_50 else None

        # Z-Score del retorno de hoy
        returns = close.pct_change().dropna()
        ret_mean = float(returns.mean())
        ret_std = float(returns.std())
        ret_hoy = float(returns.iloc[-1]) if len(returns) > 0 else 0.0
        zscore_hoy = round((ret_hoy - ret_mean) / ret_std, 3) if ret_std > 0 else 0.0

        # Volatilidad anualizada 21d
        vol_anualizada = round(float(returns.rolling(21).std().iloc[-1]) * (252 ** 0.5) * 100, 2)

        # ---- Diagnóstico técnico ----
        alertas = []
        if rsi_14 >= 75:
            estado = "sobrecomprado"
            alertas.append(
                f"el RSI de 14 días está en **{rsi_14}** (sobrecompra severa >75): "
                "estadísticamente el activo ha subido muy rápido y la presión compradora comienza a agotarse."
            )
        elif rsi_14 >= 65:
            estado = "sobrecomprado"
            alertas.append(
                f"el RSI de 14 días está en **{rsi_14}** (zona de sobrecompra moderada): "
                "no es inminente una corrección, pero el margen de seguridad es reducido."
            )
        elif rsi_14 <= 25:
            estado = "sobrevendido"
            alertas.append(
                f"el RSI de 14 días está en **{rsi_14}** (sobreventa severa <25): "
                "el activo ha caído con fuerza y podría acercarse a un suelo técnico temporal."
            )
        elif rsi_14 <= 35:
            estado = "sobrevendido"
            alertas.append(
                f"el RSI de 14 días está en **{rsi_14}** (zona de sobreventa moderada): "
                "el precio ha caído más rápido de lo normal aunque no es un extremo histórico."
            )
        else:
            estado = "neutral"
            alertas.append(f"el RSI de 14 días está en **{rsi_14}**, en zona neutral (35-65).")

        if distancia_sma is not None:
            if distancia_sma > 20:
                alertas.append(
                    f"El precio está un **{distancia_sma:.1f}%** por encima de su media móvil de 50 días "
                    "(SMA50={:.2f}$): extensión extrema, históricamente asociada a reversiones.".format(sma_50)
                )
            elif distancia_sma > 10:
                alertas.append(
                    f"El precio está un **{distancia_sma:.1f}%** por encima de su SMA50 "
                    "(${sma_50:.2f}): notable desviación alcista respecto a la tendencia de largo plazo.".format(sma_50=sma_50)
                )
            elif distancia_sma < -15:
                alertas.append(
                    f"El precio está un **{abs(distancia_sma):.1f}%** por debajo de su SMA50 "
                    "(${sma_50:.2f}): fuerte descuento técnico.".format(sma_50=sma_50)
                )

        if abs(zscore_hoy) > 2.5:
            dir_str = "alcista" if zscore_hoy > 0 else "bajista"
            alertas.append(
                f"El retorno de HOY tiene un Z-Score de **{zscore_hoy:.2f}** "
                f"({dir_str} extremo): el movimiento de hoy es estadísticamente inusual respecto a los últimos 6 meses."
            )

        alerta_tecnica = "; ".join(alertas) if alertas else "Sin señales técnicas extremas detectadas."

        resultado_base.update({
            "precio_actual": round(precio_actual, 4),
            "retorno_hoy": retorno_hoy,
            "rsi_14": rsi_14,
            "sma_50": round(sma_50, 4),
            "distancia_sma": distancia_sma,
            "zscore_hoy": zscore_hoy,
            "vol_anualizada": vol_anualizada,
            "estado_tecnico": estado,
            "alerta_tecnica": alerta_tecnica,
            "simulado": False,
        })

    except Exception as e:
        # Si falla yfinance generamos datos simulados para no romper la app
        resultado_base["simulado"] = True
        resultado_base["alerta_tecnica"] = (
            "Los datos de mercado en tiempo real no están disponibles ahora mismo "
            "(posible fallo de conexión). El análisis psicológico se aplica igualmente."
        )

    return resultado_base


# ---------------------------------------------------------------------------
# Funciones existentes mantenidas sin cambios de interfaz
# ---------------------------------------------------------------------------

def generate_fallback_data(ticker: str, period: str = "2y") -> pd.DataFrame:
    days_map = {"2y": 504, "1y": 252, "5y": 1260}
    days = days_map.get(period, 504)
    end_date = pd.Timestamp.now().normalize()
    dates = pd.date_range(end=end_date, periods=days, freq='B')
    days = len(dates)

    seed_val = sum(ord(c) for c in ticker) % (2**31)
    np.random.seed(seed_val)

    base_price, drift, volatility = 100.0, 0.0002, 0.015
    if "BTC" in ticker or "ETH" in ticker or "SOL" in ticker:
        volatility, drift, base_price = 0.035, 0.0006, (45000.0 if "BTC" in ticker else 2800.0)
    elif "TSLA" in ticker:
        volatility, base_price = 0.025, 180.0
    elif "NVDA" in ticker:
        volatility, base_price = 0.028, 480.0
    elif "AAPL" in ticker:
        volatility, base_price = 0.012, 175.0
    elif "^MXX" in ticker:
        volatility, base_price = 0.009, 56000.0
    elif any(x in ticker for x in ["SXR8", "EUNL", "SPY", "QQQ", "VWRA"]):
        volatility, base_price, drift = 0.008, 450.0, 0.0003

    log_returns = np.random.normal(drift - 0.5 * volatility**2, volatility, days)
    panic_idx = np.random.choice(days, 3, replace=False)
    euphoria_idx = np.random.choice(days, 2, replace=False)
    for i in panic_idx:
        log_returns[i] = -volatility * 4.5
    for i in euphoria_idx:
        log_returns[i] = volatility * 4.0

    prices = base_price * np.exp(np.cumsum(log_returns))
    df = pd.DataFrame(index=dates)
    df['Open'] = prices * (1 - np.random.uniform(0, 0.003, days))
    df['High'] = prices * (1 + np.random.uniform(0, 0.01, days))
    df['Low'] = prices * (1 - np.random.uniform(0, 0.01, days))
    df['Close'] = prices
    df['High'] = np.maximum(df['High'], np.maximum(df['Open'], df['Close']))
    df['Low'] = np.minimum(df['Low'], np.minimum(df['Open'], df['Close']))
    volumes = np.random.lognormal(np.log(1_000_000), 0.5, days)
    for i in list(panic_idx) + list(euphoria_idx):
        volumes[i] *= np.random.uniform(3.5, 6.0)
    df['Volume'] = volumes.astype(int)
    return df


def get_market_data(ticker: str, period: str = "2y") -> pd.DataFrame:
    ticker = ticker.strip()
    try:
        df = yf.download(ticker, period=period, progress=False, group_by='ticker')
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(1)
        if df.empty or 'Close' not in df.columns:
            raise ValueError("Datos vacíos")
        df.index = pd.to_datetime(df.index)
        return df
    except Exception:
        return generate_fallback_data(ticker, period)


def calculate_volatility(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Return'] = df['Close'].pct_change()
    df['Vol_21'] = df['Return'].rolling(window=21).std() * np.sqrt(252)
    df['Vol_252'] = df['Return'].rolling(window=252).std() * np.sqrt(252)
    df['Return'] = df['Return'].fillna(0)
    df['Vol_21'] = df['Vol_21'].ffill().bfill().fillna(0)
    df['Vol_252'] = df['Vol_252'].ffill().bfill().fillna(0)
    return df


def detect_anomalies(df: pd.DataFrame, z_threshold: float = 2.5) -> pd.DataFrame:
    df = df.copy()
    ret_std = df['Return'].std()
    df['Return_Z'] = 0.0 if (ret_std == 0 or np.isnan(ret_std)) else (
        (df['Return'] - df['Return'].mean()) / ret_std
    )
    df['Anomaly_Type'] = 'Normal'
    df.loc[df['Return_Z'] > z_threshold, 'Anomaly_Type'] = 'Euforia'
    df.loc[df['Return_Z'] < -z_threshold, 'Anomaly_Type'] = 'Pánico'
    df['Anomaly_Price'] = np.where(df['Anomaly_Type'] != 'Normal', df['Return'], 0)
    df['Vol_MA21'] = df['Volume'].rolling(window=21).mean().ffill().bfill().fillna(1.0)
    df['Anomaly_Volume'] = df['Volume'] > (3.0 * df['Vol_MA21'])
    return df


def get_educational_explanation(anomaly_type: str, z_score: float, ticker: str) -> str:
    nombre = TICKERS_DICT.get(ticker, ticker)
    z_abs = abs(z_score)
    if anomaly_type == 'Pánico':
        return (
            f"**Anomalía de Pánico en {nombre}:** retorno de {z_abs:.2f}σ bajo la media. "
            "La Aversión a la Pérdida colectiva empuja a los inversores a vender en masa, "
            "amplificando la caída más allá del valor real. "
            "Históricamente, vender en días de capitulación congela pérdidas que se habrían recuperado."
        )
    elif anomaly_type == 'Euforia':
        return (
            f"**Anomalía de Euforia en {nombre}:** retorno de {z_abs:.2f}σ sobre la media. "
            "El FOMO colectivo impulsa compras masivas que elevan el precio muy por encima de su valor fundamental. "
            "Comprar en estos extremos implica el mayor riesgo de drawdown."
        )
    return "Fluctuación dentro de los rangos normales del activo."


# ---------------------------------------------------------------------------
# Test autónomo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== TEST get_ticker_audit ===")
    for t in ["NVDA", "BTC-USD", "SAN.MC", "XXXX_INVALID"]:
        audit = get_ticker_audit(t)
        print(f"\n[{t}] precio={audit['precio_actual']} retorno={audit['retorno_hoy']}% "
              f"RSI={audit['rsi_14']} distSMA={audit['distancia_sma']}% "
              f"Z={audit['zscore_hoy']} vol={audit['vol_anualizada']}% simulado={audit['simulado']}")
        print(f"  Diagnóstico: {audit['alerta_tecnica'][:120]}...")

    print("\n=== TEST extract_ticker_from_text ===")
    frases = [
        "Compré nvidia hace poco y está cayendo, ¿vendo?",
        "¿Qué piensas del SP500 ahora?",
        "Metí todo en Bitcoin, ¿estoy loco?",
        "Tengo acciones de Inditex en Trade Republic",
        "Debería comprar $AAPL ahora que cayó?",
    ]
    from market_analysis import extract_ticker_from_text
    for f in frases:
        t = extract_ticker_from_text(f)
        print(f"  '{f[:60]}...' -> {t}")
