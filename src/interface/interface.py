import streamlit as st  
import sys
import os
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)


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