import streamlit as st
import pandas as pd
import plotly.express as px

# Configura PX para Wide
st.set_page_config(layout="wide")

# Lê o arquivo CSV
data_base = pd.read_csv('J:/Dashboard_invoice/Rel_Fatura1.csv', sep=";", encoding='UTF-8')
data_base["Ref"] = pd.to_datetime(data_base["Ref"], format='%d/%m/%Y', dayfirst=True)
data_base = data_base.sort_values("Ref")

data_base["Month"] = data_base["Ref"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês de Referência", data_base["Month"].unique())

# Adiciona o filtro para "Produto"
produtos_disponiveis = data_base["Produto"].unique()
produtos_disponiveis = ["Todos"] + list(produtos_disponiveis)
produto = st.sidebar.selectbox("Produto", produtos_disponiveis)

# Adiciona o filtro para "Filial"
filiais_disponiveis = data_base["Filial"].unique()
filiais_disponiveis = ["Todas"] + list(filiais_disponiveis)
filial = st.sidebar.selectbox("Filial", filiais_disponiveis)

# Aplica os filtros
if produto == "Todos" and filial == "Todas":
    data_base_filtered = data_base[data_base["Month"] == month].copy()
elif produto == "Todos":
    data_base_filtered = data_base[(data_base["Month"] == month) & (data_base["Filial"] == filial)].copy()
elif filial == "Todas":
    data_base_filtered = data_base[(data_base["Month"] == month) & (data_base["Produto"] == produto)].copy()
else:
    data_base_filtered = data_base[(data_base["Month"] == month) & (data_base["Produto"] == produto) & (data_base["Filial"] == filial)].copy()

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

col1.dataframe(data_base_filtered[["Filial", "Subtotal", "Desconto", "Total", "Status Pagamento"]])

# Converta a coluna 'Total' para o tipo numérico antes de agrupar
data_base_filtered['Total'] = pd.to_numeric(data_base_filtered['Total'].str.replace(',', '.'), errors='coerce')

# Agrupe por 'Status Pagamento' e calcule a soma do 'Total'
data_pie = data_base_filtered.groupby('Status Pagamento')['Total'].sum().reset_index()

# Exiba os dados para verificar se estão corretos
col2.write(data_pie)

# Crie o gráfico de pizza usando Plotly Express
fig_pie = px.pie(data_pie, names='Status Pagamento', values='Total', title=f'Soma Total por Status de Pagamento ({month}, {produto}, {filial})')

# Exiba o gráfico de pizza na col2 do Streamlit
col2.plotly_chart(fig_pie, use_container_width=True)

