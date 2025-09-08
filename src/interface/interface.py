import streamlit as st  
from src import utils,functions

st.set_page_config(page_title="Text Summarization", page_icon=":guardsman:", layout="wide")
st.title("Analise de Dados Google")
st.write("Interface para visualizção e anallise de dados das açoes da Big Tech Google")
st.sidebar.title("Menu")
st.sidebar.write("Navegue pelas opções abaixo")
options = ["Preço de fechamento", "Media Mensal de Volume por ano", "Variação do Preço de Fechamento"]
choice = st.sidebar.selectbox("Selecione uma opção", options)
if choice == "Preço de fechamento":
    st.subheader("Evolução do Preço de Fechamento")
    functions.evoluçao_close()