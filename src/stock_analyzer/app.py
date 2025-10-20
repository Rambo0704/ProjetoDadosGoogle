import streamlit as st
import datetime
import yfinance as yf
import time
import pandas as pd
import numpy as np
from utils import leitura_csv
import visualizations

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

st.title("📊 Google Stocks Dashboard ")
st.caption("Painel de análise financeira de ações GOOGL.")

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
df = leitura_csv()

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13= st.tabs([
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
    "🔻 Drawdowns",
    "🆚 Retorno vs Volatilidade",
    "📉 Melhores e Piores Dias"
])

with tab1:
    with st.spinner("Carregando DataFrame..."):
        time.sleep(1)
    st.caption("Esta área apresenta os dados brutos e tratados (tabela) que alimentam todo o dashboard. Sua função é garantir a transparência e a rastreabilidade das informações, " \
    "permitindo que o usuário verifique a fonte exata de cada cálculo e a integridade dos dados históricos da ação.")
    num_linhas = st.slider("Número de linhas a exibir", 5, 2515)
    st.dataframe(df.head(num_linhas), width="stretch")

with tab2:
    with st.spinner("Gerando gráfico..."):
        time.sleep(1)
    st.caption("Visualiza o histórico do preço de fechamento da ação em um gráfico de linha." \
    " Permite filtrar o período pelos anos inicial e final, mostrando claramente a tendência de valorização ou desvalorização da Google no tempo.")
    anos = df['Date'].dt.year.unique()
    ano_inicial,ano_final = st.slider("Selecionae o intervalo de anos",min_value=min(anos),max_value=max(anos),value=(min(anos), max(anos)))
    visualizations.evolucao_close(ano_inicial,ano_final)

with tab3:
    with st.spinner("Carregando..."):
        time.sleep(1)
    st.caption("Calcula e mostra a média mensal do volume negociado em um gráfico de barras." \
    " Ajuda a identificar a liquidez e o interesse do mercado na ação, com opção de filtrar por ano.")

    geral = st.checkbox("Todos os anos", value = True)

    if geral:
        ano_escolhido = None
    else:    
        ano_escolhido = st.number_input("Selecione o ano", min_value=int(min(anos)), max_value=int(max(anos)), value=int(max(anos)),key="dp_filtro_desvio")
    visualizations.media_volume(ano_escolhido)

with tab4:
    with st.spinner("Calculando..."):
        time.sleep(1)
    st.caption("Calcula e mostra, em um gráfico de barras, " \
    "a diferença entre o preço máximo e mínimo da ação em cada ano. Indica a volatilidade anual, destacando os anos de maior amplitude de preços.")
    visualizations.variacao_preço_ano()

with tab5:
    with st.spinner("Calculando..."):
        time.sleep(1)
    st.caption("Calcula o desvio padrão mensal do preço de fechamento ('Close') em um gráfico de barras. Essencial para medir o risco e a volatilidade da ação." \
    "Permite filtrar o cálculo por ano para analisar a instabilidade em períodos específicos.")

    geral = st.checkbox("Todos os anos", value = True,key="dp_todos_anos_checkbox")

    if geral:
        ano_escolhido = None
    else: 
        ano_escolhido = st.number_input("Selecione o ano", min_value=int(min(anos)), max_value=int(max(anos)), value=int(max(anos)))
    visualizations.desvio_padrao(ano_escolhido)

with tab6:
    with st.spinner("Analisando..."):
        time.sleep(1)
    st.caption("Calcula e exibe a Média Móvel de 30 dias do preço de fechamento ('Close') em um gráfico de linha, junto ao preço real. É uma ferramenta essencial para filtrar o ruído do mercado e identificar a tendência principal (alta, baixa ou lateralização) da ação da Google. " \
    "Permite filtrar o período de análise pelas datas inicial e final.")
    dia_ano = np.array(df["Date"].dt.to_pydatetime())
    ano_inicial,ano_final = st.slider("Selecionae o intervalo de anos",min_value=min(dia_ano),max_value=max(dia_ano),value=(min(dia_ano), max(dia_ano)),key="dp_filtro_media_movel")
    visualizations.analise_de_tendencias(ano_inicial,ano_final)

with tab7:
    with st.spinner("Processando..."):
        time.sleep(1)

    st.caption("Implementa a estratégia de Cruzamento de Médias Móveis (20 e 50 períodos)." \
    " Esta ferramenta de análise técnica plota o preço e as médias, gerando sinais visuais de Compra (cruzamento ascendente) ou Venda (cruzamento descendente)." \
    " Seu objetivo é fornecer indicadores técnicos acionáveis para a identificação de reversões e a confirmação da direção do mercado.")

    visualizations.prev_tendencias()

with tab8:
    with st.spinner("Calculando retornos..."):
        time.sleep(1)
    visualizations.retorno_diario()

with tab9:
    with st.spinner("Calculando volatilidade..."):
        time.sleep(1)
    visualizations.volatilidade_anual()

with tab10:
    with st.spinner("Calculando Sharpe Ratio..."):
        time.sleep(1)
    visualizations.sharpe_ratio_anual()

with tab11:
    with st.spinner("Identificando drawdowns..."):
        time.sleep(1)
    visualizations.identificar_drawdowns()

with tab12:
    with st.spinner("Comparando retorno e volatilidade..."):
        time.sleep(1)
    visualizations.comparativo_ano_perfomance()

with tab13:
    with st.spinner("Analisando melhores e piores dias..."):
        time.sleep(1)
    visualizations.melhores_piores_dias()

st.divider()

st.markdown("""
<div class="footer">
    Desenvolvido por <b>Gabriel Rambo</b><br>
    <a href="https://github.com/Rambo0704/ProjetoDadosGoogle" target="_blank" style="color:#00b4d8; text-decoration:none;">
        Acesse o código no GitHub
    </a>
</div>
""", unsafe_allow_html=True)
