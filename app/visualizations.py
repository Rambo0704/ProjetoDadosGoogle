
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from utils import leitura_csv 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def evolucao_close(ano_inicial=None, ano_final=None):
    df = leitura_csv()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Year'] = df['Date'].dt.year

    if ano_inicial is not None:
        df = df[df['Year'] >= ano_inicial]
    if ano_final is not None:
        df = df[df['Year'] <= ano_final]

    st.subheader(f"Evolução do Preço de Fechamento")
    st.line_chart(df.set_index('Date')['Close'])
    
def media_volume(ano_escolhido=None):
    df = leitura_csv()
    df['month'] = df['Date'].dt.month
    df['year'] = df['Date'].dt.year
    if ano_escolhido is not None:
        df = df[df['year'] == ano_escolhido]

    media = df.groupby(['year', 'month'])['Volume'].mean().reset_index()

    media['AnoMes'] = pd.to_datetime(media['year'].astype(str) + '-' + media['month'].astype(str) + '-01')

    st.bar_chart(media.set_index('AnoMes')['Volume'])

def variacao_preço_ano():
    df = leitura_csv()
    df['year'] = df['Date'].dt.year
    variacao = df.groupby('year')['Close'].agg(lambda x: x.max() - x.min())
    st.bar_chart(variacao)

def desvio_padrao(ano_escolhido=None):
    df = leitura_csv()
    df['Date'] = pd.to_datetime(df['Date'])
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month

    if ano_escolhido is not None:
        df = df[df['year'] == ano_escolhido]

    desvios = (df.groupby(['year', 'month'])['Close'].std().reset_index())
    desvios['mes_nome'] = desvios['month'].map({
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    })

    if ano_escolhido is not None:
        st.bar_chart(desvios.set_index('mes_nome')['Close'])
    else:
        desvios['AnoMes'] = pd.to_datetime(desvios['year'].astype(str) + '-' + desvios['month'].astype(str) + '-01')
        st.bar_chart(desvios.set_index('AnoMes')['Close'])

def analise_de_tendencias(data_inicio=None, data_final=None):
    df = leitura_csv()
    df['Date'] = pd.to_datetime(df['Date'])

    if data_inicio is not None:
        df = df[df['Date'] >= data_inicio]
    if data_final is not None:
        df = df[df['Date'] <= data_final]

    df = df.set_index('Date')
    df['media_movel'] = df['Close'].rolling(window=30).mean()
    st.line_chart(df[['Close', 'media_movel']])

def detecta_anomalias(ano_escolhido): #desenvolvido para fins de estudos,mas nao necessaria,pois nao possue anomalias
    df = leitura_csv()
    df['year'] = df['Date'].dt.year
    df = df[df['year'] == ano_escolhido]
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    medias = df.groupby(['month', 'day'])['Close'].mean()
    desvios = df.groupby(['month', 'day'])['Close'].std()

    df['media_dia'] = df.apply(lambda row: medias.loc[(row['month'], row['day'])], axis=1)
    df['std_dia'] = df.apply(lambda row: desvios.loc[(row['month'], row['day'])], axis=1)

    df['anomalia'] = (df['Close'] > df['media_dia'] + 2 * df['std_dia']) | \
                     (df['Close'] < df['media_dia'] - 2 * df['std_dia'])

    df_anomalia = df[df['anomalia']].set_index('Date')[['Close']]
    st.subheader('Anomalias')
    st.bar_chart(df_anomalia)
        
def prev_tendencias():
    df = leitura_csv()
    df['media_curta'] = df['Close'].rolling(window=20).mean()
    df['media_longa'] = df['Close'].rolling(window=50).mean()
    df['compra'] = (df['media_curta'] > df['media_longa']) & (df['media_curta'].shift(1) <= df['media_longa'].shift(1))
    df['venda'] = (df['media_curta'] < df['media_longa']) & (df['media_curta'].shift(1) >= df['media_longa'].shift(1))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Close'],
        mode='lines', name='Preço Fechamento',
        line=dict(color='lightgray', width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['media_curta'],
        mode='lines', name='Média Curta (20)',
        line=dict(color='#00BFFF', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['media_longa'],
        mode='lines', name='Média Longa (50)',
        line=dict(color='#FFA500', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df.loc[df['compra'], 'Date'],
        y=df.loc[df['compra'], 'Close'],
        mode='markers',
        name='Compra',
        marker=dict(symbol='triangle-up', size=10, color='lime', line=dict(color='black', width=1))
    ))
    fig.add_trace(go.Scatter(
        x=df.loc[df['venda'], 'Date'],
        y=df.loc[df['venda'], 'Close'],
        mode='markers',
        name='Venda',
        marker=dict(symbol='triangle-down', size=10, color='red', line=dict(color='black', width=1))
    ))
    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Preço ($)',
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1
        ),
        font=dict(color='white'),
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

def retorno_diario():
    df = leitura_csv()
    df['retorno_diario'] = df['Close'].pct_change().dropna()

    fig = px.histogram(
        df,
        x='retorno_diario',
        title = "",
        nbins=40,
        labels={'retorno_diario': 'Retorno Diário (%)'},
        opacity=0.8,
    )
    fig.update_layout(
        bargap=0.05,
        title = "",
        xaxis_title="Retorno Diário (%)",
        yaxis_title="Frequência",
        template="plotly_white",
        title_x=0.5,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    st.plotly_chart(fig, use_container_width=True)

def volatilidade_anual():
    df = leitura_csv()
    df['retorno_diario'] = df['Close'].pct_change()
    df['year'] = df['Date'].dt.year
    volatilidade_anual = df.groupby('year')['retorno_diario'].std()*np.sqrt(252) #multiplicando pelo numero medio de pregoes(dias uteis da bolsa) por ano
    st.bar_chart(volatilidade_anual)

def sharpe_ratio_anual():
    df = leitura_csv()
    df['retorno_diario'] = df['Close'].pct_change()
    df['year'] = df['Date'].dt.year
    retorno_medio_anual = df.groupby('year')['retorno_diario'].mean()*253
    volatilidade_anual = df.groupby('year')['retorno_diario'].std()*np.sqrt(252)
    sharpe_ratio = retorno_medio_anual/volatilidade_anual
    st.bar_chart(sharpe_ratio)

def identificar_drawdowns():
    df = leitura_csv()
    df['retorno_diario'] = df['Close'].pct_change()
    df['valor_acumulado'] = (1 + df['retorno_diario']).cumprod()
    df['pico'] = df['valor_acumulado'].cummax()
    df['drawdown'] = (df['valor_acumulado'] - df['pico']) / df['pico']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'], 
        y=df['valor_acumulado'],
        mode='lines',
        name='Valor Acumulado',
        line=dict(color='#00b4d8', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['drawdown'],
        fill='tozeroy',
        mode='lines',
        name='Drawdown',
        line=dict(color='rgba(255, 99, 71, 0.0)'),
        fillcolor='rgba(255, 99, 71, 0.4)'
    ))

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Data",
        yaxis_title="Valor Acumulado / Drawdown",
        legend=dict(orientation="h", y=-0.2, x=0.3),
        height=500,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="#e6e6e6")
    )

    st.plotly_chart(fig, use_container_width=True)

def comparativo_ano_perfomance():
    df = leitura_csv()
    df['retorno_diario'] = df['Close'].pct_change()
    df['year'] = df['Date'].dt.year

    retorno_anual = df.groupby('year')['retorno_diario'].mean() * 253
    volatilidade_anual = df.groupby('year')['retorno_diario'].std() * np.sqrt(252)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=retorno_anual.index,
        y=retorno_anual.values,
        name="Retorno Anual",
        marker_color="#1f77b4",
        text=[f"{v:.2%}" for v in retorno_anual.values],
        textposition="outside"
    ))

    fig.add_trace(go.Bar(
        x=volatilidade_anual.index,
        y=volatilidade_anual.values,
        name="Volatilidade Anual",
        marker_color="orange",
        text=[f"{v:.2%}" for v in volatilidade_anual.values],
        textposition="outside"
    ))

    fig.update_layout(
        barmode="group",
        title="Retorno vs Volatilidade por Ano",
        xaxis_title="Ano",
        yaxis_title="Valor",
        template="plotly_dark",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)


def melhores_piores_dias():
    df = leitura_csv()
    df['retorno_diario'] = df['Close'].pct_change()
    df['year'] = df['Date'].dt.year

    melhores_idx = df.groupby('year')['retorno_diario'].idxmax()
    melhores_dias = df.loc[melhores_idx, ['Date', 'year', 'retorno_diario', 'Close']].dropna()

    piores_idx = df.groupby('year')['retorno_diario'].idxmin()
    piores_dias = df.loc[piores_idx, ['Date', 'year', 'retorno_diario', 'Close']].dropna()

    comparativo = pd.DataFrame({
        'Ano': list(melhores_dias['year']) + list(piores_dias['year']),
        'Tipo': ['Melhor Dia'] * len(melhores_dias) + ['Pior Dia'] * len(piores_dias),
        'Retorno (%)': list(melhores_dias['retorno_diario'] * 100) + list(piores_dias['retorno_diario'] * 100),
        'Data': list(melhores_dias['Date'].dt.strftime('%Y-%m-%d')) + list(piores_dias['Date'].dt.strftime('%Y-%m-%d'))
    })

    fig = px.bar(
        comparativo,
        x='Ano',
        y='Retorno (%)',
        color='Tipo',
        barmode='group',
        text='Data',
        labels={'Retorno (%)': 'Retorno (%)'},
        title='Melhor e Pior Dia por Ano'
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis=dict(type='category'))

    st.plotly_chart(fig)

def padroes_mensais(ano_escolhido=None):
    df = leitura_csv()
    df['Date'] = pd.to_datetime(df['Date'])
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['retorno_diario'] = df['Close'].pct_change()

    if ano_escolhido is not None:
        df = df[df['year'] == ano_escolhido]

    retorno_medio = (df.groupby(['year', 'month'])['retorno_diario'].mean().reset_index())

    retorno_medio['retorno_diario'] *= 100
    retorno_medio['mes_nome'] = retorno_medio['month'].map({
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    })

    if ano_escolhido is not None:
        st.bar_chart(retorno_medio.set_index('mes_nome')['retorno_diario'])
    else:
        retorno_medio['AnoMes'] = pd.to_datetime(
            retorno_medio['year'].astype(str) + '-' + retorno_medio['month'].astype(str) + '-01'
        )
        st.bar_chart(retorno_medio.set_index('AnoMes')['retorno_diario'])
