import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="CDB / FGC",
    page_icon="💸",
    layout="wide"
)

lateral = st.sidebar

CAMINHO_CSV = os.path.join(os.path.dirname(__file__), "..", "RF_mab.csv")

@st.cache_data
def carregar_dados():
    dados = pd.read_csv(CAMINHO_CSV)
    return dados


st.title("Controle Renda Fixa / FGC :beetle: :moneybag:")

dados = carregar_dados()
tabela_dados = st.data_editor(
    dados,
    num_rows="dynamic",
    use_container_width=True)

salvar = st.button("Salvar Dados")
if salvar:
    tabela_dados.to_csv(CAMINHO_CSV, index=False)
    st.cache_data.clear()
    st.success("Dados atualizados com sucesso :smile:")
    st.balloons()

mostrar_grafico = st.toggle("Mostrar Gráfico por Emissor")

if mostrar_grafico:
    valor_por_emissor = tabela_dados.groupby("Emissor")["Valor Apl"].sum().reset_index()
    valor_por_emissor["Cor"] = valor_por_emissor["Valor Apl"].apply(
        lambda x: "Acima de 250k" if x > 250000 else "Abaixo de 250k"
    )
    grafico = alt.Chart(valor_por_emissor).mark_bar().encode(
        x=alt.X("Emissor", sort="-y"),
        y=alt.Y("Valor Apl"),
        color=alt.Color("Cor", scale=alt.Scale(
            domain=["Abaixo de 250k", "Acima de 250k"],
            range=["steelblue", "red"]
        ))
    )
    st.altair_chart(grafico, use_container_width=True)

mostrar_grafico_venc = st.toggle("Mostrar Gráfico por Vencimento")

if mostrar_grafico_venc:
    dados_venc = tabela_dados[["Venc", "Valor Apl", "Tipo", "Emissor"]].copy()
    dados_venc["Venc"] = pd.to_datetime(dados_venc["Venc"])
    dados_venc = dados_venc.sort_values("Venc")

    grafico_venc = alt.Chart(dados_venc).mark_bar().encode(
        x=alt.X("Venc:T", title="Data de Vencimento", sort="ascending"),
        y=alt.Y("Valor Apl:Q", title="Valor Aplicado"),
        tooltip=["Venc:T", "Valor Apl:Q", "Tipo:N", "Emissor:N"],
    )
    st.altair_chart(grafico_venc, use_container_width=True)

mostrar_grafico_12m = st.toggle("Mostrar Gráfico Vencimentos 12 meses")

if mostrar_grafico_12m:
    hoje = datetime.today()
    limite_12m = hoje + relativedelta(months=12)

    dados_12m = tabela_dados[["Venc", "Valor Apl", "Tipo", "Emissor"]].copy()
    dados_12m["Venc"] = pd.to_datetime(dados_12m["Venc"])

    proximos = dados_12m[dados_12m["Venc"] <= limite_12m].copy()
    proximos["Label"] = proximos["Venc"].dt.strftime("%Y-%m-%d")
    proximos["Status"] = proximos["Venc"].apply(
        lambda x: "Vencido" if x.date() <= hoje.date() else "A vencer"
    )
    proximos = proximos.sort_values("Venc")

    distantes = dados_12m[dados_12m["Venc"] > limite_12m]
    if not distantes.empty:
        acumulado = pd.DataFrame({
            "Venc": [limite_12m],
            "Valor Apl": [distantes["Valor Apl"].sum()],
            "Tipo": ["Diversos"],
            "Emissor": ["Diversos"],
            "Label": ["Após 12 meses"],
            "Status": ["A vencer"],
        })
        proximos = pd.concat([proximos, acumulado], ignore_index=True)

    grafico_12m = alt.Chart(proximos).mark_bar().encode(
        x=alt.X("Label:N", title="Vencimento", sort=list(proximos["Label"])),
        y=alt.Y("Valor Apl:Q", title="Valor Aplicado"),
        color=alt.Color("Status:N", scale=alt.Scale(
            domain=["A vencer", "Vencido"],
            range=["steelblue", "green"]
        )),
        tooltip=["Label:N", "Valor Apl:Q", "Tipo:N", "Emissor:N"],
    )
    st.altair_chart(grafico_12m, use_container_width=True)
