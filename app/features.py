import pandas as pd

def calculo_RSI(dados, periodos=14):
    retorno = dados.diff()
    
    ganhos = retorno.clip(lower=0)
    perdas = retorno.clip(upper=0).abs()
    
    media_ganhos = ganhos.rolling(window=periodos, min_periods=periodos).mean()
    media_perdas = perdas.rolling(window=periodos, min_periods=periodos).mean()
    
    rs = media_ganhos / media_perdas
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_MACD(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd - signal_line

def calcular_ATR_percentual(df, period=14):
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()

    return atr / df['Close'] * 100
