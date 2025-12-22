import yfinance as yf
import pandas as pd
import features as ft
import joblib

def api_dados():

    df = yf.download('GOOGL', period='2y', auto_adjust=False, multi_level_index=False)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df.index = pd.to_datetime(df.index)
    
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
        
    df['Date'] = df.index

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
    
    df = df.dropna()

    return df


def prever_tendencia():

    df = api_dados()

    ultima_linha = df.iloc[[-1]].copy()
    data_analise = ultima_linha.index[0]


    try:
        modelo_c = joblib.load("../models/ml_compra/modelo_compra.pkl")
        scaler_c = joblib.load("../models/ml_compra/scaler_compra.pkl")
        imputer_c = joblib.load("../models/ml_compra/imputer_compra.pkl")
        features_c = joblib.load("../models/ml_compra/features_compra.pkl")
        config_c = joblib.load("../models/ml_compra/config_compra.pkl")
        threshold_c = joblib.load("../models/ml_compra/threshold_compra.pkl")

        X_c = ultima_linha[features_c]
        X_c = imputer_c.transform(X_c)
        X_c = scaler_c.transform(X_c)

        prob_compra = modelo_c.predict_proba(X_c)[:, 1][0]
    except Exception as e:
        print(f"Erro ao carregar modelo de compra: {e}")
        prob_compra = 0
        threshold_c = 1.0

    try:
        modelo_q = joblib.load("../models/ml_queda/modelo_queda.pkl")
        scaler_q = joblib.load("../models/ml_queda/scaler_queda.pkl")
        imputer_q = joblib.load("../models/ml_queda/imputer_queda.pkl")
        features_q = joblib.load("../models/ml_queda/features_queda.pkl")
        config_q = joblib.load("../models/ml_queda/config_queda.pkl")
        threshold_q = joblib.load("../models/ml_queda/threshold_queda.pkl")

        X_q = ultima_linha[features_q]
        X_q = imputer_q.transform(X_q)
        X_q = scaler_q.transform(X_q)

        prob_queda = modelo_q.predict_proba(X_q)[:, 1][0]
    except Exception as e:
        print(f"Erro ao carregar modelo de queda: {e}")
        prob_queda = 0
        threshold_q = 1.0


    
    decisao = "NEUTRO"
    mensagem = "Mercado indefinido. Aguardar."
    detalhes = ""


    if prob_compra >= threshold_c:

        if prob_compra >= (threshold_c + 1/100):
            intensidade = "FORTE"
        else:
            intensidade = "MODERADA"

        decisao = "COMPRA"
        mensagem = f"Sinal de ALTA {intensidade}. Probabilidade estimada pelo modelo ({prob_compra:.1%}) supera o limiar de decisão ({threshold_c:.1%})."
        
        horizonte = config_c.get('horizonte', '?')
        lucro = config_c.get('movimento_minimo', 0) * 100
        detalhes = f"Modelo prevê alta de +{lucro:.1f}% em {horizonte} dias."

    elif prob_queda >= threshold_q:
        
        if prob_queda >= (threshold_q + 1/100):
            intensidade = "FORTE"
        else:
            intensidade = "MODERADA"

        decisao = "VENDA"
        mensagem = f"Sinal de BAIXA {intensidade}. Probabilidade estimada pelo modelo ({prob_queda:.1%}) supera o limiar de decisão ({threshold_q:.1%})."
        
        horizonte = config_q.get('horizonte', '?')
        perda = config_q.get('movimento_minimo', 0) * 100
        detalhes = f"Modelo prevê queda de -{perda:.1f}% em {horizonte} dias."

    else:
        decisao = "AGUARDAR"
        mensagem = f"Sem sinais claros. Alta: {prob_compra:.1%}(Probabilidade estimada pelo modelo) (Corte: {threshold_c:.1%}) | Baixa: {prob_queda:.1%}(Probabilidade estimada pelo modelo) (Corte: {threshold_q:.1%})"
        detalhes = "O mercado não apresentou os padrões estatísticos treinados."

    if (prob_compra >= threshold_c) and (prob_queda >= threshold_q):
        forca_compra = prob_compra / threshold_c
        forca_queda = prob_queda / threshold_q
        
        if forca_queda > forca_compra:
            decisao = "VENDA (Volatilidade Alta)"
            mensagem = "Conflito de sinais, mas a tendência de QUEDA é estatisticamente mais forte."
        else:
            decisao = "COMPRA (Volatilidade Alta)"
            mensagem = "Conflito de sinais, mas a tendência de ALTA é estatisticamente mais forte."

    return {
        "decisao": decisao,
        "prob_alta": prob_compra,
        "prob_queda": prob_queda,
        "mensagem": mensagem,
        "detalhes_modelo": detalhes,
        "data_referencia": data_analise
    }
test = prever_tendencia()
print(test)