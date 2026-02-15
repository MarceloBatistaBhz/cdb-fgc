import streamlit as st
import os

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔒 Login")
        password = st.text_input("Senha:", type="password")
        if st.button("Entrar"):
            if password == os.environ.get("APP_PASSWORD", ""):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Senha incorreta")
        st.stop()

check_password()

st.set_page_config(
    page_title="CDB / FGC",
    page_icon="💸",
    layout="wide"
)

st.title("Escolha o investidor no menu à esquerda")

