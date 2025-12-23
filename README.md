# 📊 Google Stock Analysis & Prediction Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red)
![XGBoost](https://img.shields.io/badge/Machine%20Learning-XGBoost-green)
![License](https://img.shields.io/badge/License-MIT-purple)

## 📝 Sobre o Projeto

O **Projeto Dados Google** é uma aplicação de análise financeira e *Machine Learning* desenvolvida para monitorizar, analisar e prever tendências das ações da Alphabet Inc. (GOOGL).

O sistema opera com uma **arquitetura de dados híbrida**:
1.  **Treinamento Robusto:** Os modelos são treinados com um *dataset* histórico consolidado (`GoogleStockPrices.csv`), garantindo aprendizado consistente de padrões de longo prazo.
2.  **Predição em Tempo Real:** Para a inferência no dia a dia, o dashboard conecta-se diretamente à **API do Yahoo Finance (yfinance)**, obtendo os preços mais recentes do mercado para gerar sinais de compra ou venda atualizados.

---

## 🚀 Funcionalidades Principais

### 1. 📈 Análise Exploratória e Técnica
Visualizações interativas utilizando **Plotly** e **Pandas**:
* **Histórico de Preços:** Gráficos de linha com filtros de data.
* **Indicadores Técnicos:** Médias Móveis (SMA/EMA), Bandas de Bollinger, RSI, MACD.
* **Volatilidade e Retorno:** Análise de distribuição de retornos diários e desvio padrão.
* **Sazonalidade:** Identificação de padrões mensais de rentabilidade.

### 2. 🤖 Inteligência Artificial (Machine Learning)
O sistema utiliza **dois modelos XGBoost Classifier independentes** para evitar viés e capturar nuances do mercado:

* **📈 Modelo de Alta (Compra):** Treinado especificamente para identificar padrões gráficos e técnicos que precederam movimentos de valorização consistente no passado.
* **📉 Modelo de Queda (Venda):** Um modelo distinto, focado exclusivamente em detectar configurações de mercado que historicamente resultaram em desvalorização.
* **⚖️ Consenso e Conflito:** O sistema avalia as probabilidades de ambos os modelos simultaneamente.
    * Se ambos derem sinais fortes (Alta e Queda), o sistema alerta para **"Conflito/Volatilidade"**.
    * Se apenas um disparar, gera um sinal direcional ("Compra" ou "Venda").
    * Se nenhum atingir o limiar de confiança, mantém-se "Neutro".

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface (Frontend):** Streamlit
* **Machine Learning:** XGBoost, Scikit-Learn
* **Processamento de Dados:** Pandas, NumPy
* **Visualização:** Plotly, Matplotlib
* **Dados Financeiros:** Yahoo Finance (yfinance)

---

## ⚙️ Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o **Python 3.10+** instalado.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/SEU_USUARIO/ProjetoDadosGoogle.git](https://github.com/SEU_USUARIO/ProjetoDadosGoogle.git)
cd ProjetoDadosGoogle
2. Criar um Ambiente Virtual (Recomendado)
Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
3. Instalar Dependências
Bash

pip install -r requirements.txt
4. ⚠️ Treinar os Modelos (Passo Obrigatório)
Os modelos de Inteligência Artificial (.pkl) não estão incluídos no repositório para garantir que tenhas a versão mais recente treinada com dados frescos. Antes de rodar o dashboard, precisas gerá-los:

Abra o notebook de treino:

Arquivo: notebooks/training.ipynb

Certifique-se de que o arquivo data/GoogleStockPrices.csv está presente (para treino histórico).

Execute todas as células ("Run All").

O script irá ler o CSV, treinar o XGBoost e salvar os arquivos .pkl nas pastas models/ml_compra e models/ml_queda.

5. Executar o Dashboard
Após o treino estar concluído, inicie a aplicação que usará a API do Yahoo Finance para previsões atuais:

Bash

streamlit run app/main.py
O navegador abrirá automaticamente no endereço http://localhost:8501.

⚠️ Disclaimer (Aviso Legal)
Este projeto tem fins estritamente educacionais e académicos. As previsões geradas pelos modelos de Inteligência Artificial baseiam-se em padrões estatísticos passados e não constituem recomendação de investimento. O mercado financeiro é volátil e imprevisível; não utilize esta ferramenta para tomar decisões financeiras reais.

📜 Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.

👨‍💻 Autor
Desenvolvido por Gabriel Rambo
