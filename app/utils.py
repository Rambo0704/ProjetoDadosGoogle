import pandas as pd
import os

def leitura_csv():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, "..", "data", "GoogleStockPrices.csv")
    try:
        df = pd.read_csv(caminho_arquivo)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        return pd.read_csv("data/GoogleStockPrices.csv")

def qualidade_dados():
    df = leitura_csv()
    print(f"Nulos:\n{df.isna().sum()}")
    print(f" duplicados: {df.duplicated().sum()}")
    cols_numericas = ['Open','High','Low','Close','Volume']
    print(f"{(df[cols_numericas]<0).sum()}")
    print(f"Inconsistencia:\n{df[df['High'] < df['Low']]}")

def estatisticas_descritivas():
    df = leitura_csv()
    print(df[['Open','High','Low','Close','Volume']].describe())
    print(f"Datas:\n Minima:{df['Date'].min()}\n Maxima:{df['Date'].max()}")