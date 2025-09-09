import pandas as pd
from pathlib import Path

def leitura_csv():
    caminho_atual = Path(__file__).parent
    caminho_csv = caminho_atual / "data" / "GoogleStockPrices.csv"
    df = pd.read_csv(caminho_csv) 
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def qualidade_dados():
    df = leitura_csv()
    print(f"Nulos:\n{df.isna().sum()}")
    print(f" duplicados: {df.duplicated().sum()}")
    print(f"{(df[['Open','High','Low','Close','Volume']]<0).sum()}")
    print(f"Inconsistencia:\n{df[df['High'] < df['Low']]}")

def estatisticas_descritivas():
    df = leitura_csv()
    print(df[['Open','High','Low','Close','Volume']].describe())
    print(f"Datas:\n Minima:{df['Date'].min()}\n Maxima:{df['Date'].max()}")