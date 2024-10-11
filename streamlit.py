from dotenv import load_dotenv
import streamlit as st
import requests
import os

load_dotenv()

API_URL = os.getenv("API_URL")

if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

if 'history' not in st.session_state:
    st.session_state.history = []

def send_query(query):
    headers = {
        "x-api-key": st.session_state.api_key
    }
    body = {
        "user_input": query,
        "history": st.session_state.history
    }
    response = requests.post(API_URL, json=body, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro: " + response.text)
        return None

def format_response(response):
    if isinstance(response, dict) and "message" in response:
        return response["message"]
    return "Resposta não encontrada."

st.image("https://www.calcme.com.br/wp-content/uploads/2022/12/logo-calcme-fundo-claro.png", width=150)

col1, col2 = st.columns([3, 1])

with col1:
    st.write("Interaja com a API Calcme para obter informações financeiras.")

with col2:
    st.session_state.api_key = st.text_input("Digite a API Key:", st.session_state.api_key, type="password")


query = st.text_input("Digite sua pergunta:")

if st.button("Enviar"):
    if query:
        if st.session_state.api_key:
            with st.spinner("Enviando..."):
                result = send_query(query)
                if result:
                    formatted_result = format_response(result)

                    st.session_state.history.append({
                        "User": query,
                        "IA": formatted_result
                    })
        else:
            st.warning("Por favor, insira sua API Key antes de enviar.")
    else:
        st.warning("Por favor, insira uma consulta antes de enviar.")

# Exibir histórico de conversas
if st.session_state.history:
    for chat in st.session_state.history:
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**User:** {chat['User']}")

        with col2:
            st.markdown(f"**IA:** {chat['IA']}")
