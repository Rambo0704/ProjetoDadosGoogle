#ESTE ARQUIVO DEVE SER IDENTICO AO USADO NO TREINAMENTO.
# SE ALTERAR A LOGICA AQUI, RETREINE O MODELO.
import pandas as pd

def leitura_csv():
    df = pd.read_csv("../data/GoogleStockPrices.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def qualidade_dados():
    df = leitura_csv()
    print(f"Nulos:\n{df.isna().sum()}")
    print(f" duplicados: {df.duplicated().sum()}")
    print(f"{(df[['Open','High','Low','Close','Volume']]<0).sum()}")
    print(f"Inconsistencia:\n{df[df['High'] < df['Low']]}")

def estatisticas_descritivas():
    df = leitura_csv()
    print(df[['Open','High','Low','Close','Volume']].describe())
    print(f"Datas:\n Minima:{df['Date'].min()}\n Maxima:{df['Date'].max()}")


def calculo_RSI(close, window=14):
    retorno = close.diff()
    ganhos = retorno.apply(lambda x: x if x > 0 else 0)
    perdas = retorno.apply(lambda x: -x if x < 0 else 0)

    media_ganhos = ganhos.rolling(window=window).mean()
    media_perdas = perdas.rolling(window=window).mean()

    RS = media_ganhos / media_perdas
    RSI = 100 - (100 / (1 + RS))


    return RSI

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
