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

evoluçao_close()