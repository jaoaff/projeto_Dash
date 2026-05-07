import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

#Importação de biblioteca via CDN pare estilização do modelo
tailwind_cdn = ["https://cdn.tailwindcss.com"]
options = [{'label': 'Total', 'value': 'Total'}, {'label': 'Até 500 vendas', 'value': 500}, {'label': 'Média de 1 mil vendas', 'value': 2000}, {'label': 'Média de 10 mil vendas', 'value': 10000}, {'label': 'Média de 50 mil vendas', 'value': 50000}]

# Leitura da base csv
df = pd.read_csv('./ecommerce_estatistica.csv')
#pd.set_option('display.max_columns', None)
#pd.set_option('display.width',  None)




def cria_grafico(escala):

    # Tratar materiais e selecionar os mais expressivos
    porcentagens = df['Material'].value_counts() / len(df['Material']) * 100
    materiais_filtrados = porcentagens[porcentagens >= 3].index
    df_modifica = df
    df_modifica['Material'] = df_modifica['Material'].apply(lambda x: x if x in materiais_filtrados else 'Outros')


    fig = px.pie(df_modifica, names='Material', color='Material', hole=0.2, )
    fig.update_layout(
        title='Distribuição por materiais'
    )

    if escala == 'Total':
        titulo='Dispersão - Numero de avaliações por Quantidade de itens vendidos'
        df_altera_escala = df
    elif escala == 500:
        titulo='Dispersão - Numero de avaliações por Quantidade de vendas na faixa 500 vendas'
        df_altera_escala = df[df['Qtd_Vendidos_Cod'] <= 500]
    elif escala == 2000:
        titulo= 'Dispersão - Numero de avaliações por Quantidade de vendas até 1 mil vendas'
        df_altera_escala = df[df['Qtd_Vendidos_Cod'].between(500,1999)]
    elif escala == 10000:
        titulo='Dispersão - Numero de avaliações por Quantidade de vendas na faixa de 10 mil'
        df_altera_escala = df[df['Qtd_Vendidos_Cod'].between(2000,49000)]
    elif escala == 50000:
        titulo='Dispersão - Numero de avaliações por Quantidade de vendas na faixa de 50 mil'
        df_altera_escala = df[df['Qtd_Vendidos_Cod'] >= 50000]



    fig2 = px.scatter(df_altera_escala, x='N_Avaliações', y='Qtd_Vendidos_Cod')
    fig2.update_layout(
        title=titulo,
        xaxis_title='Numero de Avalições',
        yaxis_title='Quantidade de intens vendidos'
    )


    fig3 = px.histogram(df, x='Nota', title='Distribuição de Notas')
    fig3.update_layout(
        title='Distribuição de Notas',
        yaxis_title='Contagem'
    )
    return fig, fig2, fig3


def cria_App():
    app = Dash(__name__, external_scripts=tailwind_cdn)

    app.layout = html.Div(className='flex flex-col items center',children=[
        html.H1("Dashboard ecomerce", className='bg-slate-200 font-bold text-center text-[50px] rounded-b-xl'),
        dcc.Graph(id='id_pie'),
        html.Br(),
        html.H2("Configurações do grafico de Disperção", className='font-bold text-[20px] border-t-2 border-black' ),
        dcc.RadioItems(id='id_escala', options=options, value=options[0]['value'], className='bg-slate-100 , w-30, p-100'),
        html.Br(),
        dcc.Graph(id='id_dispersao', className='w-500'),
        html.Div(className='border-t-2 border-black',children=[
            dcc.Graph(id='id_histograma')
        ])

    ])
    return app







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = cria_App()

    @app.callback([
        Output('id_pie', 'figure'),
        Output('id_dispersao', 'figure'),
        Output('id_histograma', 'figure'),
    ],
        [Input('id_escala', 'value')]
    )
    def atualiza_grafico(id_escala):
        fig, fig2, fig3 = cria_grafico(id_escala)
        return [fig, fig2, fig3]
    app.run(debug=True, port=8050)
