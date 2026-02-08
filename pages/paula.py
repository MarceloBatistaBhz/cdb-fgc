import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CDB / FGC",
    page_icon="💸",
    layout="wide"
)

lateral = st.sidebar

st.title("Dados")

@st.cache_data
def carregar_dados():
    dados = pd.read_csv("RF_mab.csv")
    return dados
    

st.title("Controle Renda Fixa / FGC :beetle: :moneybag:")

dados = carregar_dados()
tabela_dados = st.data_editor(
    dados,
    num_rows="dynamic",
    use_container_width=True)

salvar = st.button("Salvar Dados")
if salvar:
    tabela_dados.to_csv("RF_mab.csv" , index=False)
    st.success("Dados atualizados com sucesso :smile:")
    valor_por_emissor = dados.groupby("Emissor")["Valor Apl"].sum()
    st.balloons()

mostrar_grafico = st.toggle("Mostrar Gráfico por Emissor")

if mostrar_grafico:
    valor_por_emissor = dados.groupby("Emissor")["Valor Apl"].sum()
    st.bar_chart(valor_por_emissor)

