import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.colab import drive
import delta


# Conecta do Google Drive para uso no colab.research.google.com
drive.mount('/content/drive')

# Lê o arqivo CSV
data_base = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Rel_Fatura_Geral.csv', sep=";", encoding='UTF-8')

# Converte a coluna Date para data no modelo dd/mm/aaaa
data_base['Date'] = data_base['Date'].apply(lambda x: pd.to_datetime(x, format='%d/%m/%Y'))

# Configura PX para Wide
st.set_page_config(layout="wide")

#Plota o gráfico
fig = px.pie(data_base, values='Desconto', names='Filial', title='Total de vendas por filial')
st.plotly_chart(fig)

# Mosta o gráfico na tela
fig
