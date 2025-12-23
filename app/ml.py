import yfinance as yf
import pandas as pd
import features as ft
import joblib
import os
import streamlit as st

@st.cache_resource(show_spinner=False)
def carregar_modelo_compra():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(base_dir, "..", "models", "ml_compra")
        return (
            joblib.load(os.path.join(model_dir, "modelo_compra.pkl")),
            joblib.load(os.path.join(model_dir, "scaler_compra.pkl")),
            joblib.load(os.path.join(model_dir, "imputer_compra.pkl")),
            joblib.load(os.path.join(model_dir, "features_compra.pkl")),
            joblib.load(os.path.join(model_dir, "config_compra.pkl")),
            joblib.load(os.path.join(model_dir, "threshold_compra.pkl"))
        )
    except Exception:
        return None

@st.cache_resource(show_spinner=False)
def carregar_modelo_queda():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(base_dir, "..", "models", "ml_queda")
        return (
            joblib.load(os.path.join(model_dir, "modelo_queda.pkl")),
            joblib.load(os.path.join(model_dir, "scaler_queda.pkl")),
            joblib.load(os.path.join(model_dir, "imputer_queda.pkl")),
            joblib.load(os.path.join(model_dir, "features_queda.pkl")),
            joblib.load(os.path.join(model_dir, "config_queda.pkl")),
            joblib.load(os.path.join(model_dir, "threshold_queda.pkl"))
        )
    except Exception:
        return None

def api_dados():
    try:
        df = yf.download('GOOGL', period='2y', auto_adjust=False, multi_level_index=False, progress=False)
        
        if df.empty: return pd.DataFrame()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        df.index = pd.to_datetime(df.index)
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df['Date'] = df.index

        df['Return'] = df['Close'].pct_change()

        df['Dist_SMA5'] = (df['Close'] / df['Close'].rolling(5).mean()) - 1
        df['Dist_SMA20'] = (df['Close'] / df['Close'].rolling(20).mean()) - 1
        df['Dist_SMA50'] = (df['Close'] / df['Close'].rolling(50).mean()) - 1
        df['Dist_SMA200'] = (df['Close'] / df['Close'].rolling(200).mean()) - 1

        df['Dist_EMA10'] = (df['Close'] / df['Close'].ewm(span=10, adjust=False).mean()) - 1
        df['Dist_EMA20'] = (df['Close'] / df['Close'].ewm(span=20, adjust=False).mean()) - 1

        df['RSI14'] = ft.calculo_RSI(df['Close'])
        df['MACD'] = ft.calculate_MACD(df['Close']) 

        df['Momentum_5'] = df['Close'] / df['Close'].shift(5) - 1
        df['Momentum_10'] = df['Close'] / df['Close'].shift(10) - 1
        df['Momentum_20'] = df['Close'] / df['Close'].shift(20) - 1

        df['Volatility_20'] = df['Return'].rolling(20).std()

        df['Price_Range_Pct'] = (df['High'] - df['Low']) / df['Close']
        df['Price_Change_Pct'] = (df['Close'] - df['Open']) / df['Open']
        
        df['Upper_Shadow_Pct'] = (df['High'] - df[['Open', 'Close']].max(axis=1)) / df['Close']
        df['Lower_Shadow_Pct'] = (df[['Open', 'Close']].min(axis=1) - df['Low']) / df['Close']

        df['BB_width'] = (4 * df['Close'].rolling(20).std()) / df['Close'].rolling(20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume'].rolling(20).mean()
        
        df['ROC_10'] = df['Close'].pct_change(10)
        df['ATR_pct'] = ft.calcular_ATR_percentual(df, period=14)
        
        df = df.dropna()
        
        cols_to_drop = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close', 'SMA5', 'SMA20', 'SMA50', 'SMA200', 'EMA10', 'EMA20']
        cols_existentes = [c for c in cols_to_drop if c in df.columns]
        df = df.drop(columns=cols_existentes)

        return df
    except Exception:
        return pd.DataFrame()

def prever_tendencia():
    df = api_dados()
    
    if df is None or df.empty:
        return {
            "decisao": "ERRO",
            "prob_alta": 0.0,
            "prob_queda": 0.0,
            "mensagem": "Erro de conexão API.",
            "threshold_compra": 0.0,
            "threshold_queda": 0.0,
            "detalhes_modelo": "",
            "data_referencia": "N/A"
        }

    ultima_linha = df.iloc[[-1]].copy()
    data_analise = ultima_linha.index[0]

    try:
        artifacts_c = carregar_modelo_compra()
        if artifacts_c is None: raise Exception("Modelo não encontrado")
        
        modelo_c, scaler_c, imputer_c, features_c, config_c, threshold_c = artifacts_c

        X_c = ultima_linha[features_c]
        X_c = imputer_c.transform(X_c)
        X_c = scaler_c.transform(X_c)
        prob_compra = modelo_c.predict_proba(X_c)[:, 1][0]
    except Exception as e:
        print(f"Erro Compra: {e}")
        prob_compra = 0; threshold_c = 1.0

    try:
        artifacts_q = carregar_modelo_queda()
        if artifacts_q is None: raise Exception("Modelo não encontrado")

        modelo_q, scaler_q, imputer_q, features_q, config_q, threshold_q = artifacts_q

        X_q = ultima_linha[features_q]
        X_q = imputer_q.transform(X_q)
        X_q = scaler_q.transform(X_q)
        prob_queda = modelo_q.predict_proba(X_q)[:, 1][0]
    except Exception as e:
        print(f"Erro Queda: {e}")
        prob_queda = 0; threshold_q = 1.0

    decisao = "NEUTRO"
    mensagem = "Mercado indefinido ou contraditório. Aguardar."
    detalhes = ""
    
    sinal_compra = prob_compra >= threshold_c
    sinal_venda = prob_queda >= threshold_q

    if sinal_compra and sinal_venda:
        decisao = "AGUARDAR (Conflito)"
        mensagem = f"ALERTA: Sinais mistos! Compra ({prob_compra:.1%}) e Venda ({prob_queda:.1%}) ativos simultaneamente. Alta volatilidade."
        detalhes = "O sistema detectou forças opostas. Operação cancelada por segurança."

    elif sinal_venda:
        if prob_queda >= (threshold_q + 0.10):
            intensidade = "FORTE"
        else:
            intensidade = "MODERADA"
            
        decisao = "VENDA"
        mensagem = f"Sinal de BAIXA {intensidade}. Probabilidade ({prob_queda:.1%}) Limiar ({threshold_q:.1%})."
        
        hz = config_q.get('horizonte', '?')
        pct = config_q.get('movimento_minimo', 0) * 100
        detalhes = f"Modelo prevê queda de -{pct:.1f}% em {hz} dias."

    elif sinal_compra:
        if prob_compra >= (threshold_c + 0.10):
            intensidade = "FORTE"
        else:
            intensidade = "MODERADA"

        decisao = "COMPRA"
        mensagem = f"Sinal de ALTA {intensidade}.Probabilidade ({prob_compra:.1%}) Limiar ({threshold_c:.1%})."
        
        hz = config_c.get('horizonte', '?')
        pct = config_c.get('movimento_minimo', 0) * 100
        detalhes = f"Modelo prevê alta de +{pct:.1f}% em {hz} dias."

    else:
        decisao = "AGUARDAR"
        mensagem = f"Sem direção clara. Compra: {prob_compra:.1%} | Venda: {prob_queda:.1%}"
        detalhes = "Aguardando definição de tendência."
    
    return {
        "decisao": decisao,
        "prob_alta": prob_compra,
        "prob_queda": prob_queda,
        "mensagem": mensagem,
        "threshold_compra": threshold_c,
        "threshold_queda": threshold_q,
        "detalhes_modelo": detalhes,
        "data_referencia": data_analise
    }