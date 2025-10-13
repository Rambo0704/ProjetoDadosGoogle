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
    page_title="Google Stocks Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    /* Fundo e fonte */
    .stApp {
        background-color: #0e1117;
        color: #e6e6e6;
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    /* Títulos */
    h1, h2, h3, h4 {
        color: #f8f9fa !important;
        font-weight: 600;
    }

    /* Divider */
    hr {
        border: 1px solid #2a2d35;
    }

    /* Métricas */
    div[data-testid="stMetricValue"] {
        color: #00b4d8;
        font-weight: bold;
        font-size: 1.6em;
    }
    div[data-testid="stMetricLabel"] {
        color: #bdbdbd;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #e6e6e6 !important;
        border: none !important;
        padding: 8px 20px !important;
        font-weight: 500;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00b4d8 !important;
        border-bottom: 2px solid #00b4d8 !important;
    }

    /* Rodapé */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .footer {
        text-align: center;
        color: gray;
        font-size: 13px;
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Google Stocks Dashboard (GOOGL)")
st.caption("Painel de análise financeira da ação GOOGL.")

st.divider()

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
col1.metric("Preço Atual", f"${preco_atual:.2f}", f"{variacao_pct:+.2f}%")
col2.metric("Volume Médio (3M)", f"{volume_medio:,}")
col3.metric("Última Atualização", datetime.date.today().strftime("%d/%m/%Y"))

st.divider()
df = pd.read_csv("../data/GoogleStockPrices.csv")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
    "📁 DataFrame",
    "📈 Fechamento",
    "📊 Volume Médio",
    "📉 Variação %",
    "📏 Desvio Padrão",
    "📎 Média Móvel",
    "📆 Tendências",
    "💹 Retornos",
    "⚡ Volatilidade",
    "💼 Sharpe Ratio",
    "🔻 Drawdowns"
])

with tab1:
    with st.spinner("Carregando DataFrame..."):
        time.sleep(1)
    num_linhas = st.slider("Número de linhas a exibir", 5, 2515)
    st.dataframe(df.head(num_linhas), use_container_width=True)

with tab2:
    with st.spinner("Gerando gráfico..."):
        time.sleep(1)
    functions.evolucao_close()

with tab3:
    with st.spinner("Carregando..."):
        time.sleep(1)
    functions.media_volume()

with tab4:
    with st.spinner("Calculando..."):
        time.sleep(1)
    functions.variacao_preço_ano()

with tab5:
    with st.spinner("Calculando..."):
        time.sleep(1)
    functions.desvio_padrao()

with tab6:
    with st.spinner("Analisando..."):
        time.sleep(1)
    functions.analise_de_tendencias()

with tab7:
    with st.spinner("Processando..."):
        time.sleep(1)
    functions.prev_tendencias()

with tab8:
    with st.spinner("Calculando retornos..."):
        time.sleep(1)
    functions.retorno_diario()

with tab9:
    with st.spinner("Calculando volatilidade..."):
        time.sleep(1)
    functions.volatilidade_anual()

with tab10:
    with st.spinner("Calculando Sharpe Ratio..."):
        time.sleep(1)
    functions.sharpe_ratio_anual()

with tab11:
    with st.spinner("Identificando drawdowns..."):
        time.sleep(1)
    functions.identificar_drawdowns()

st.divider()

st.markdown("""
<div class="footer">
    Desenvolvido por <b>Gabriel Rambo</b><br>
    <a href="https://github.com/Rambo0704/ProjetoDadosGoogle" target="_blank" style="color:#00b4d8; text-decoration:none;">
        Acesse o código no GitHub
    </a>
</div>
""", unsafe_allow_html=True)
