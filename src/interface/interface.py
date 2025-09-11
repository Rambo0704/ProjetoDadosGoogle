import streamlit as st
import sys
import os
import datetime
import yfinance as yf
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

import functions


st.set_page_config(
    page_title="Dashboard Google Stocks",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("📊 Dashboard de Ações da Google (GOOGL)")
st.markdown(
    """
    Este painel interativo apresenta análises financeiras da Google, 
    incluindo **preço de fechamento histórico**, **volume de negociações**
    e **variações percentuais** ao longo do tempo.  
    Use o menu lateral para navegar entre as seções.
    """
)

st.divider()

googl = yf.Ticker("GOOGL")
info = googl.info

preco_atual = info.get("currentPrice", 0)
volume_medio = info.get("averageVolume", 0)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Preço Atual", f"${preco_atual:.2f}", "+1.2%")
with col2:
    st.metric("Volume Médio (3 meses)", f"{volume_medio:,}", "-3%")
with col3:
    st.metric("Última Atualização", datetime.date.today().strftime("%d/%m/%Y"))

st.divider()

st.sidebar.header(" Menu de Navegação")
options = {
    "Preço de fechamento": " Evolução do preço de fechamento",
    "Media Mensal de Volume por ano": " Volume médio mensal",
    "Variação do Preço de Fechamento": " Variação percentual"
}

choice = st.sidebar.radio("Selecione a análise:", list(options.keys()))

st.subheader(options[choice])

if choice == "Preço de fechamento":
    functions.evolucao_close()

elif choice == "Media Mensal de Volume por ano":
    functions.media_volume_mensal()

elif choice == "Variação do Preço de Fechamento":
    functions.variacao_close()

st.divider()
st.markdown(
    "<p style='text-align:center; color:gray'>Desenvolvido por Gabriel • Projeto Acadêmico</p>",
    unsafe_allow_html=True
)
