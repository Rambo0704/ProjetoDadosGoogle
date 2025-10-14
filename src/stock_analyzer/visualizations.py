
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from utils import leitura_csv 
import streamlit as st
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
    
def media_volume():
    df = leitura_csv()
    df['month'] = df['Date'].dt.month
    df['year'] = df['Date'].dt.year
    media = df.groupby(['year', 'month'])['Volume'].mean().reset_index()

    media['AnoMes'] = pd.to_datetime(media['year'].astype(str) + '-' + media['month'].astype(str) + '-01')

    st.bar_chart(media.set_index('AnoMes')['Volume'])

def variacao_preço_ano():
    df = leitura_csv()
    df['year'] = df['Date'].dt.year
    variacao = df.groupby('year')['Close'].agg(lambda x: x.max() - x.min())
    st.bar_chart(variacao)

def desvio_padrao():
    df = leitura_csv()
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    desvios = df.groupby(['year','month'])['Close'].std().reset_index()
    desvios['AnoMes'] = pd.to_datetime(desvios['year'].astype(str) + '-' + desvios['month'].astype(str) + '-01')
    st.bar_chart(desvios.set_index('AnoMes')['Close'])

def analise_de_tendencias():
    df = leitura_csv()
    df['Date'] = pd.to_datetime(df['Date'])
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
    df['retorno_diario'] = df['Close'].pct_change()
    plt.figure(figsize=(10, 6))
    plt.hist(df['retorno_diario'].dropna(), bins=50, color='skyblue', edgecolor='black')
    plt.title('Distribuição dos Retornos Diários')
    plt.xlabel('Retorno Diário (%)')
    plt.ylabel('Frequência')
    plt.grid(True)
    plt.tight_layout()
    fig = plt.gcf()
    st.pyplot(fig)

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
    sharpe_ratio = retorno_anual / volatilidade_anual

    comparativo = pd.DataFrame({
        'Retorno Anual(%)': retorno_anual*100,
        'Volatilidade(%)': volatilidade_anual*100,
        'Sharpe Ratio': sharpe_ratio
    })
    comparativo = comparativo.round(2)
    print(comparativo)
    comparativo[['Retorno Anual(%)', 'Volatilidade(%)']].plot(kind='bar', figsize=(14,6))
    plt.title('Comparação de Anos: Retorno vs Volatilidade')
    plt.ylabel('Percentual (%)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    comparativo['Sharpe Ratio'].plot(kind='line', marker='o', color='green', linewidth=2)
    plt.title('Sharpe Ratio por Ano')
    plt.ylabel('Sharpe Ratio')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def melhores_piores_dias():
    df = leitura_csv()
    df['retorno_diario'] = df['Close'].pct_change()
    df['year'] = df['Date'].dt.year

    melhores_idx = df.groupby('year')['retorno_diario'].idxmax()
    melhores_dias = df.loc[melhores_idx, ['Date', 'year', 'retorno_diario', 'Close']]
    print("Melhores dias por ano:")
    print(melhores_dias.sort_values('year'))

    piores_idx = df.groupby('year')['retorno_diario'].idxmin()
    piores_dias = df.loc[piores_idx, ['Date', 'year', 'retorno_diario', 'Close']]
    print("\nPiores dias por ano:")
    print(piores_dias.sort_values('year'))
    plt.figure(figsize=(14, 6))
    plt.scatter(melhores_dias['Date'], melhores_dias['retorno_diario'] * 100, color='green', label='Melhores Dias')
    plt.scatter(piores_dias['Date'], piores_dias['retorno_diario'] * 100, color='red', label='Piores Dias')
    plt.axhline(0, color='gray', linestyle='--')
    plt.title('Melhores e Piores Dias por Ano (% Retorno Diário)')
    plt.xlabel('Data')
    plt.ylabel('Retorno Diário (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def padroes_mensais(): #Identificar Padrões Sazonais Mensais nos Retornos
    df = leitura_csv()
    df['month'] = df['Date'].dt.month
    df['retorno_diario'] = df['Close'].pct_change()
    retorno_medio_mensal = df.groupby('month')['retorno_diario'].mean()*100
    plt.figure(figsize=(12, 6))
    retorno_medio_mensal.plot(kind='bar', color='cornflowerblue', edgecolor='black')
    plt.title('Retorno Médio por Mês')
    plt.xlabel('Mês')
    plt.ylabel('Retorno Médio (%)')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.xticks(ticks=range(0, 12), labels=[
        'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
    ], rotation=0)
    plt.tight_layout()
    plt.show()

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


from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

def random_forest(anos_prev=20):
    df = leitura_csv()
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df['Return'] = df['Close'].pct_change()
    df['SMA5'] = df['Close'].rolling(5).mean()
    df['SMA10'] = df['Close'].rolling(10).mean()
    df['EMA10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['RSI14'] = calculo_RSI(df['Close'])
    df['MACD'] = calculate_MACD(df['Close'])
    df['Return_1'] = df['Return'].shift(1)
    df['Return_2'] = df['Return'].shift(2)
    df['Target'] = (df['Return'].shift(-1) > 0).astype(int)
    df = df.dropna()

    X = df.drop(['Target'], axis=1).select_dtypes(include=[np.number])
    y = df['Target']

    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X, y)

    model = RandomForestClassifier(
        n_estimators=300, max_depth=8, min_samples_leaf=5, random_state=42
    )
    model.fit(X_res, y_res)

    previsoes = []
    datas_prev = []

    last_date = df.index[-1]
    ultimo_preco = df['Close'].iloc[-1]
    volatilidade = df['Return'].std()

    for i in range(anos_prev):
        ultima_linha = df.iloc[-1:].copy()
        X_input = ultima_linha.drop(['Target'], axis=1).select_dtypes(include=[np.number])
        y_pred = model.predict(X_input)[0]

        if y_pred == 1:
            retorno = abs(np.random.normal(loc=volatilidade/2, scale=volatilidade))
        else:
            retorno = -abs(np.random.normal(loc=volatilidade/2, scale=volatilidade))

        novo_preco = ultima_linha['Close'].values[0] * (1 + df['Return'].mean() + np.random.normal(0, df['Return'].std()))
        nova_data = last_date + pd.DateOffset(years=i+1)

        previsoes.append(novo_preco)
        datas_prev.append(nova_data)

        ultima_linha.loc[ultima_linha.index[0], 'Close'] = novo_preco
        df.loc[nova_data] = ultima_linha.iloc[0]
        df['Return'] = df['Close'].pct_change()
        df['SMA5'] = df['Close'].rolling(5).mean()
        df['SMA10'] = df['Close'].rolling(10).mean()
        df['EMA10'] = df['Close'].ewm(span=10, adjust=False).mean()
        df['RSI14'] = calculo_RSI(df['Close'])
        df['MACD'] = calculate_MACD(df['Close'])
        df['Return_1'] = df['Return'].shift(1)
        df['Return_2'] = df['Return'].shift(2)

        ultimo_preco = novo_preco

    plt.figure(figsize=(14,7))
    plt.plot(df.index, df['Close'], label='Histórico', color='blue')
    plt.plot(datas_prev, previsoes, label='Previsão futura', color='orange', marker='o')
    plt.title(f'Previsão {anos_prev} anos à frente')
    plt.xlabel("Date")
    plt.ylabel("Preço")
    plt.legend()
    plt.grid(True)
    plt.show()

    return pd.DataFrame({"Date": datas_prev, "Preco_Previsto": previsoes})


if __name__ == "__main__":
    random_forest()