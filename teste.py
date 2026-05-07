import pandas as pd
import plotly.express as px


# Leitura da base csv
df = pd.read_csv('./ecommerce_estatistica.csv')
pd.set_option('display.max_columns', None)
pd.set_option('display.width',  None)


porcentagens = df['Material'].value_counts() / len(df['Material']) * 100
materiais_filtrados = porcentagens[porcentagens >= 3].index
df_modifica = df
df_modificado = df_modifica[~df_modifica['Material'].isin(materiais_filtrados)]
titulo = 'Distribuição dos Materiais dentro de da categoria Outros'

fig = px.pie(df_modificado, names='Material', hole=0.2, )
fig.show()
