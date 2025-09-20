import streamlit as st
import sys
import os
import datetime
import yfinance as yf
import time
import pandas as pd
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

import functions

st.set_page_config(
    page_title="Dashboard Google Stocks",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

st.title("📊 Dashboard de Ações da Google (GOOGL)")
st.markdown(
    """
    Este painel interativo apresenta análises financeiras da **Google**.
    """
)

st.divider()

with st.container():
    st.markdown("### 📌 Resumo Atual")

    googl = yf.Ticker("GOOGL")
    info = googl.info

    preco_atual = info.get("currentPrice", 0)
    volume_medio = info.get("averageVolume", 0)

    hist = googl.history(period="2d")
    if len(hist) >= 2:
        preco_ontem = hist["Close"].iloc[-2]
        variacao_pct = ((preco_atual - preco_ontem) / preco_ontem) * 100
    else:
        variacao_pct = 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Preço Atual", f"${preco_atual:.2f}", f"{variacao_pct:+.2f}%")
    with col2:
        st.metric("Volume Médio (3M)", f"{volume_medio:,}")
    with col3:
        st.metric("Última Atualização", datetime.date.today().strftime("%d/%m/%Y"))

st.divider()

st.sidebar.header("Menu de Navegação")
menu = st.sidebar.selectbox(
    "Escolha a análise:",
    [
        "Exibir DataFrame",
        "Preço de Fechamento",
        "Volume Médio Mensal",
        "Variação Percentual",
        "Desvio Padrão",
        "Média Móvel",
        "Tendências Passadas",
        "Retorno Diário",
        "Volatilidade Anual",
        "Sharpe Ratio",
        "Drawdowns",
    ]
)

df = pd.read_csv("../data/GoogleStockPrices.csv")

if menu == "Exibir DataFrame":
    with st.spinner("Carregando"):
        time.sleep(3)
    st.subheader("Veja o DataFrame completo")
    num_linhas = st.slider("Numero de linha a exibir", 5,2515)
    st.dataframe(df.head(num_linhas))

elif menu == "Preço de Fechamento":
    with st.spinner("Carregando"):
        time.sleep(3)
    st.subheader("Evolução do preço de fechamento")
    functions.evolucao_close()

elif menu == "Volume Médio Mensal":
    with st.spinner("Carregando"):
        time.sleep(3)    
    st.subheader("Volume médio mensal")
    functions.media_volume()

elif menu == "Variação Percentual":
    with st.spinner("Carregando"):
        time.sleep(3)    
    st.subheader("Variação percentual do preço")
    functions.variacao_preço_ano()

elif menu == "Desvio Padrão":
    with st.spinner("Carregando"):
        time.sleep(3)
    st.subheader("Desvio Padrão")
    functions.desvio_padrao()

elif menu == "Média Móvel":
    with st.spinner("Carregando"):
        time.sleep(3)
    st.subheader("Média Móvel para análise de tendencias ")
    functions.analise_de_tendencias()

elif menu == "Tendências Passadas":
    with st.spinner("Carregando"):
        time.sleep(3)
    st.subheader("Tendências Passadas")
    functions.prev_tendencias()

elif menu == "Retorno Diário":
    with st.spinner("Carregando"):
        time.sleep(3)
    st.subheader("Retorno Diário do Fechamento de Ações")
    functions.retorno_diario()

elif menu == "Volatilidade Anual":
    with st.spinner("Carregando"):
        time.sleep(3)
    st.subheader("Volatilidade Anual")
    functions.volatilidade_anual()

elif menu == "Sharpe Ratio":
    with st.spinner("Carregando"):
        time.sleep(3)
    st.subheader("Sharpe Ratio Anual")
    functions.sharpe_ratio_anual()

elif menu == "Drawdowns":
    with st.spinner("Carregando"):
        time.sleep(3)
    st.subheader("Identificar Drawdowns")
    functions.identificar_drawdowns()
  
st.divider()

st.markdown(
    """
    <div style='text-align:center; padding:10px; color:gray; font-size:14px'>
        Desenvolvido por <b>Gabriel Rambo</b><br>
        <b>-- https://github.com/Rambo0704 --<b>
    </div>
    """,
    unsafe_allow_html=True
)
