# Importação das bibliotecas
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go 
py.init_notebook_mode(connected=True)

# Leitura do arquivo.csv
df = pd.read_csv('consumo.csv', encoding='UTF-8', sep=';') # Ler o arquivo em csv, o UTF-8 Ler os acentos cedilhas
dados=df.values  # Transformação do dataframe em array

# Criação das listas vazias
dados_2012=[]
dados_2013=[]
dados_2014=[]
dados_2015=[]
dados_2016=[]
dados_2017=[]
dados_2018=[]
regioes=[]
colors=['#07325a','#135090','#2178bb','#6ca1cf','#91b0d8'] # Atribuição das cores

# Filtragem de dados em listas usando o laço for
for dado in dados:
    # Adicionando os elementos de acordo com a posição
    regioes.append(dado[0]) 
    dados_2012.append(dado[1])
    dados_2013.append(dado[2])
    dados_2014.append(dado[3])
    dados_2015.append(dado[4])
    dados_2016.append(dado[5])
    dados_2017.append(dado[6])
    dados_2018.append(dado[7])

# exclusão dos elementos desnecessários 
del regioes[0:6]  
del dados_2012[0:6]
del dados_2013[0:6]
del dados_2014[0:6]
del dados_2015[0:6]
del dados_2016[0:6]
del dados_2017[0:6]
del dados_2018[0:6]

# Criação do gráfico Sunburst
# Criação da lista para atribuição dos nomes que aparecem no gráfico 
labels=['REGIÕES']+ regioes+['2012']*5+['2013']*5+['2014']*5+['2015']*5+['2016']*5+['2017']*5+['2018']*5
# Atribuição de quais elementos da lista label são filhos de quem
parents=['']+['REGIÕES']*5+regioes*7 
# Atribuição dos valores referente a lista label
values=['']+[0]*5+dados_2012 +dados_2013 +dados_2014+dados_2015+dados_2016+dados_2017+dados_2018
'''print (labels)
print (parents)
print (values)'''

# Atribuição dos elementos que vão aparecer no gráfico
consumo_livre =go.Figure(go.Sunburst(labels=labels,parents=parents,values=values))
consumo_livre.update_traces(hoverinfo="label+value+percent parent") # Informações do hover
consumo_livre.update_layout(title=dict(    #"dict()"Função que atribui uma série de caracteristicas a variável(dicionário)
    text='<b>Consumo Livre por Região 2012-2018 [GWh]<b>',
    font=dict(size=20),
    xref='paper', # Área central do gráfico
    yref='container', # Área externa ao paper
    x=0.5, # Faz o posicionamento horizontal do texto de acordo com o xref
    y=0.95 # Faz o posicionamento vertical do texto de acordo com yref
),
height=700, # Condicionamento do tamanho do texto
sunburstcolorway =colors,
extendsunburstcolors = True) # Concede aos filhos do elemento pai uma variação da mesma cor

py.iplot(consumo_livre)

# Abre a página em html para plotagem do gráfico
import dash 
import dash_core_components as dcc # Biblioteca que identifica o gráfico e pemite recurso de filtro
import dash_html_components as html # Permite utilização das tags html 
app = dash.Dash() # Variável para armazena uma página
app.layout = html.Div([dcc.Graph(figure = consumo_livre)]) # Recebe as configurações da página do dash
app.run_server(debug = True) # (debug= True) Faz a verificação de erros
