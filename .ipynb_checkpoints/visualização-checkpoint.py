import pandas as pd 
import  matplotlib.pyplot as plt
from main import leitura_csv

def evoluçao_close():
    df = leitura_csv()
    plt.figure(figsize=(12,6))
    plt.plot(df['Date'], df['Close'], label='Preço de Fechamento', color='blue')
    plt.title('Preço de Fechamento da Ação da Google (2015-2024)')
    plt.xlabel('Data')
    plt.ylabel('Preço ($)')
    plt.grid(True)
    plt.legend()
    plt.show()

def media_volume():
    df = leitura_csv()
    df['month'] = df['Date'].dt.month
    df['year'] = df['Date'].dt.year
    media = df.groupby(['year', 'month'])['Volume'].mean()

    plt.figure(figsize=(15, 7)) 
    media.plot(kind='bar', color='skyblue') 
    plt.title('Média Mensal de Volume por Ano')
    plt.xlabel('Ano e Mês')
    plt.ylabel('Volume Médio')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def variacao_preço_ano():
    df = leitura_csv()
    df['year'] = df['Date'].dt.year
    variacao = df.groupby('year')['Close'].agg(lambda x: x.max() - x.min())
    print(variacao)
    plt.figure(figsize=(12,6))
    variacao.plot(kind='bar', color='tomato', edgecolor='black')
    plt.title('Variação Anual do Preço de Fechamento das Ações da Google')
    plt.xlabel('Ano')
    plt.ylabel('Variação de Preço ($)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def desvio_padrao():
    df = leitura_csv()
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    desvio_padrao = df.groupby(['year','month'])['Close'].std().unstack()
    print(desvio_padrao)
    plt.figure(figsize=(15, 6))
    plt.imshow(desvio_padrao, aspect='auto', cmap='hot', interpolation='nearest')
    plt.title('Volatilidade Mensal do Preço de Fechamento (Desvio Padrão)')
    plt.xlabel('Mês')
    plt.ylabel('Ano')
    plt.colorbar(label='Desvio Padrão')
    plt.xticks(ticks=range(12), labels=range(1, 13))
    plt.yticks(ticks=range(len(desvio_padrao.index)), labels=desvio_padrao.index)
    plt.show()
variacao_preço_ano()