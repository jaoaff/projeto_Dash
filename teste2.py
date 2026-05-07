import pandas as pd
import plotly.express as px


# Leitura da base csv
df = pd.read_csv('./ecommerce_estatistica.csv')
pd.set_option('display.max_columns', None)
pd.set_option('display.width',  None)

#print(df)
print(df[df['Qtd_Vendidos_Cod'].between(5000,49000)])