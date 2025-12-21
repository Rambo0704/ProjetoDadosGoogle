import yfinance as yf
import pandas as pd
import features as ft
import joblib
def api_dados():
    df = yf.download('GOOGL', period='1year')
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    df['Return'] = df['Close'].pct_change()

    df['SMA5'] = df['Close'].rolling(5).mean()
    df['SMA20'] = df['Close'].rolling(20).mean()
    df['SMA50'] = df['Close'].rolling(50).mean()
    df['SMA200'] = df['Close'].rolling(200).mean()

    df['EMA10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

    df['RSI14'] = ft.calculo_RSI(df['Close'])
    df['MACD'] = ft.calculate_MACD(df['Close'])

    df['Momentum_5'] = df['Close'] / df['Close'].shift(5) - 1
    df['Momentum_10'] = df['Close'] / df['Close'].shift(10) - 1
    df['Momentum_20'] = df['Close'] / df['Close'].shift(20) - 1

    df['Volatility_20'] = df['Return'].rolling(20).std()

    df['Price_Range'] = df['High'] - df['Low']
    df['Price_Change'] = df['Close'] - df['Open']
    df['Upper_Shadow'] = df['High'] - df[['Open', 'Close']].max(axis=1)
    df['Lower_Shadow'] = df[['Open', 'Close']].min(axis=1) - df['Low']

    df['BB_middle'] = df['Close'].rolling(20).mean()
    df['BB_std'] = df['Close'].rolling(20).std()
    df['BB_width'] = (4 * df['BB_std']) / df['BB_middle']

    df['Volume_MA5'] = df['Volume'].rolling(5).mean()
    df['Volume_MA20'] = df['Volume'].rolling(20).mean()
    df['Volume_Ratio'] = df['Volume'] / df['Volume_MA20']

    df['ROC_10'] = df['Close'].pct_change(10)

    df['ATR_pct'] = ft.calcular_ATR_percentual(df, period=14)

    return df


def prever_compra():
    df = api_dados()

    modelo = joblib.load("../models/modelo_xgb.pkl")
    scaler = joblib.load("../models/scaler.pkl")
    features = joblib.load("../models/features.pkl")
    imputer = joblib.load("../models/imputer.pkl")
    config = joblib.load("../models/config.pkl")
    threshold = joblib.load("../models/threshold.pkl")

    ultima_linha = df.iloc[[-1]].copy()
    data_analise = ultima_linha.index[0]    

    X = ultima_linha[features]
    X = imputer.transform(X)
    X = scaler.transform(X)
  
    prob = modelo.predict_proba(X)[:, 1][0]
    if prob >= threshold:
            decisao = "COMPRA"
            mensagem = f"Sinal forte! Probabilidade ({prob:.1%}) acima da nota de corte ({threshold:.1%})."
    else:
        decisao = "AGUARDAR"
        mensagem = f"Risco alto. Probabilidade ({prob:.1%}) abaixo da nota de corte ({threshold:.1%})."

    horizonte = config.get('horizonte', '?')
    meta_lucro = config.get('movimento_minimo', 0) * 100
    
    detalhes = f"Modelo treinado para buscar +{meta_lucro:.1f}% em {horizonte} dias."
    
    return {
        "decisao": decisao,
        "probabilidade": prob,
        "threshold_usado": threshold,
        "mensagem_explicativa": mensagem,
        "detalhes_modelo": detalhes,
        "data_referencia" : data_analise
    }