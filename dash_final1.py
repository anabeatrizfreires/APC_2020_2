#!/usr/bin/env python
#--------------------------------------Importando bibliotecas---------------------------------------
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import xlrd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
py.init_notebook_mode(connected=True)

#--------------------------------------Geração e Consumo---------------------------------------
# abre o arquivo
f = open("Anuário Estatístico de Energia Elétrica 2020 - Workbook.xlsx - Tabela 2.4.csv",encoding="utf8")
# f.read lê todo o conteúdo do arquivo e retorna uma string
# .split("\n") divide essa string do conteudo em linhas
content = f.read().split("\n")
#lista vazia que armazena os anos
years = []
#for lê a oitava linha que contem os anos dentro do arquivo csv
#.split(",") separa elementos por vírgula da lista, começando pelo elemento 2 e excluindo os últimos 4
for y in content[8].split(",")[2:-4]:
    #insere na lista years cada elemento de y transformado de string para inteiro
    years.append (int(y))

#função que armazena as regiões na lista data
def filtra_dados(regiao):
    #lista vazia que armazena regiões
    data = []
    #for lê todas as linhas da lista
    for l in content:
        #.split(",") separa por vírgula
        ls = l.split(",")
        #condiciona que se o elemento 1 da lista for igual uma região prossigo
        if ls[1] == regiao:
            #determina o começo e fim da lista, partindo do elemento 2 e excluindo os últimos 5
            dt = ls[2:-5]
            #lê cada elemento da lista filtrada
            for l in dt:
                #insere na lista data cada elemento l transformado de string para float
                data.append(float(l))
    return data

#lista das regiões
regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sul', 'Sudeste']

#--------------------------------------Consumo Livre---------------------------------------
# Leitura do arquivo.csv
df = pd.read_csv('consumo.csv', encoding='UTF-8', sep=';') # Ler o arquivo em csv, o UTF-8 Ler os acentos cedilhas
dados=df.values  # Transformação do dataframe em array

# Criação das listas vazias que armazenam os dados de cada ano
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

# Exclusão dos elementos desnecessários 
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

# Atribuição dos elementos que vão aparecer no gráfico
figura_consumo_livre =go.Figure(go.Sunburst(labels=labels,parents=parents,values=values))
figura_consumo_livre.update_traces(hoverinfo="label+value+percent parent") # Informações do hover
figura_consumo_livre.update_layout(title=dict(    #Função dict atribui uma série de caracteristicas a variável(dicionário)
    text='Consumo Livre por Região [GWh]',
    font=dict(size=20),
    xref='paper', # Área central do gráfico
    yref='container', # Área externa ao paper
    x=0.5, # Faz o posicionamento horizontal do texto de acordo com o xref
    y=0.95 # Faz o posicionamento vertical do texto de acordo com yref
),
height=700, # Condicionamento do tamanho do texto
sunburstcolorway =colors,
extendsunburstcolors = True) # Concede aos filhos do elemento pai uma variação da mesma cor

#--------------------------------------------Consumo e PIB-----------------------------------------------
#xlrd Abre o arquivo xls
wb= xlrd.open_workbook('base_consumo.xls') 
#xlrd Abre o arquivo xls 
wc= xlrd.open_workbook('base_pibcorrente.xls')  
 #sheet Escolhe a tabela a partir do nome      
p= wb.sheet_by_name('Tabela 3.1')  
 #sheet Escolhe a tabela a partir do nome                   
p1=wc.sheet_by_name('Tabela')                          

#Filtrando valores de Consumo
#Declara uma lista vazia
dados_consumo=[]              
#Declara uma lista vazia                                
coluna_consumo=[] 
 #Executa o ciclo criando uma lista de 0 a 7
for i in range(7):    
    #Receberá os valores das colunas das tabelas e define o que acontece depois de receber um número  
    j=i+2   
    #Recebe os valores das tabelas
    coluna_consumo=p.col_values(j)      
    #Adiciona os valores a lista partindo do elemento 10 até o elemento 15                       
    dados_consumo.append(coluna_consumo[10:15])                        

#Filtrando valores de PIB
#Inicialização de variáveis
i=0                        
#Inicialização de variáveis                            
j=0   
#Declara uma lista vazia                                                 
dados_PIB=[]  
#Declara uma lista vazia                                           
coluna_PIB=[]
#Executa o ciclo criando uma lista de 0 a 7                                             
for i in range(7):  
    #Receberá os valores das colunas das tabelas e define o que acontece depois de receber um número                                   
    j=i+1  
    #Recebe os valores das tabelas                                           
    coluna_PIB=p1.col_values(j)      
    #Adiciona os valores a lista partindo do elemento 4 até o elemento 9                   
    dados_PIB.append(coluna_PIB[4:9])                        



#--------------------------------------------Tarifa Média-----------------------------------------------
#Abre o arquivo xls
df = xlrd.open_workbook('202.xls')
#sheet Escolhe a tabela a partir do nome  
tabela = df.sheet_by_name('Tabela 2.14')
#Declara uma lista vazia 
dados_tarifa_media = []    
#Declara uma lista vazia                                 
coluna_tarifa_media = []
# Executa o ciclo de acordo com a quantidade de anos 
for i in range(8): 
    #Variável que receberá os valores da coluna                                               
    j = i + 1                           
    #col_values recebe os valores das tabelas e vai colocar na coluna      
    coluna_tarifa_media = tabela.col_values(j)             
    #Adiciona os valores a lista partindo do elemento 10 até o elemento 15 
    dados_tarifa_media.append(coluna_tarifa_media[10:15])               


#--------------------------------------------Luz para Todos-----------------------------------------------
#Renomeia as siglas para relacionar as do arquivo json com as do arquivo csv
def name_to_sigla(name):                                                                
    if name == "Norte":                                                                 
        return "N"                                                                      
    if name == "Nordeste":                                                              
        return "NE"                                                                     
    if name == "Centro-Oeste":                                                          
        return "CO"                                                                     
    if name == "Sudeste":                                                               
        return "SE"                                                                    
    if name == "Sul":                                                                   
        return "S"                                                                     

#Abre o arquivo GEOJSON dividindo o mapa por região
f = open("brazil_reg.json")  
#Lê o arquivo json                                                          
br = json.loads(f.read())                                                              

#-------------------------------------------------Dash--------------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX]) 

app.layout = html.Div(children=[                                                        
    html.H1(children= 'Panorama da Energia Elétrica no Brasil', style = {'background':'#ffffff',"text-align":"center"}), 
        dcc.Dropdown(
            id = "classe_geracao_consumo",
            options = [{'label': regiao, 'value': regiao} for regiao in regioes],
            value = "Norte",
            clearable = False
            ),
        dcc.Graph(id = "fig_geracao_consumo"),
        
    
    
    html.Hr(),
    html.Div([dcc.Graph(figure = figura_consumo_livre),
        dcc.Dropdown(
            id='classe_consumo_pib',
            options=[
                {'label': 'N', 'value': 'Nor'},
                {'label': 'NE', 'value': 'Nord'},
                {'label': 'SE', 'value': 'Sd'},
                {'label': 'S', 'value': 'Sl'},
                {'label': 'CO', 'value': 'CO'}],
            value='Nor'
            ),
        dcc.Graph(id='fig_consumo_pib'), 
    ], style={'background':'#ffffff','display':'flex'}),
    
        
    html.Hr(),
    html.Div([
        dcc.Dropdown(
            id='classe_tarifa_media',
            options=[
                {'label': '2012', 'value': '2012'},
                {'label': '2013', 'value': '2013'},
                {'label': '2014', 'value': '2014'},
                {'label': '2015', 'value': '2015'},
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'}],
            value='2012',
            ),
        dcc.Graph(id='fig_tarifa_media'),
    ]),
        
    html.Div([                                                                         
        dcc.Dropdown(
            id='classe_luz_para_todos',                                                     
            options=[
                {'label': '2012', 'value': '2012'},                                        
                {'label': '2013', 'value': '2013'},                                         
                {'label': '2014', 'value': '2014'},                                         
                {'label': '2015', 'value': '2015'},                                         
                {'label': '2016', 'value': '2016'},                                         
                {'label': '2017', 'value': '2017'},                                         
                {'label': '2018', 'value': '2018'}],
            value='2012',
            ),                                                                  
        dcc.Graph(id='fig_luz_para_todos'),
    ]),            
])



#-------------------------------------------------Plotagem Luz para Todos--------------------------------------------------------------
#Declaração de entradas e saída   
@app.callback(  
    #As entradas são os valores atribuidos nas labels e as saídas são os gráficos selecionados pelo valor da label                                                                             
    Output('fig_luz_para_todos', 'figure'),                                                   
    Input('classe_luz_para_todos', 'value') 
)
#Função de plotagem do gráfico luz para todos
def luz_para_todos(year):
    #Abre anuário
    f = open("Anuário Estatístico de Energia Elétrica 2020 - Workbook.xlsx - Tabela 2.24.csv",encoding="utf8")
    # f.read lê todo o conteúdo do arquivo e retorna uma string
    # .split("\n") divide essa string do conteudo em linhas
    lines = f.read().split("\n")                                                           
    #Lista vazia que armazena as siglas                          
    siglas = []                                                                            
    #Lista vazia que armazena os valores de energia
    populations = []                                                                       
    #Lê as linhas começando da linha 10 e excluindo as duas últimas linhas
    for l in lines[10:-2]:   
        #.split(",") separa elementos por vírgula da lista                                                             
        ls = l.split(",") 
        #Insere na lista siglas cada elemento de name_to_sigla que esteja na posição 1 da lista                                                                 
        siglas.append(name_to_sigla(ls[1]))    
        #.strip retira todos os espaços do começo e do inicio da string então '   -    ' fica '-'                                            
        population_str = ls[int(year[-1])].strip()     
        #Compara a string recebida com o '-'                                    
        if population_str == '-':    
            #Se True '-' é igual a 0                                                     
            population = 0                                                                 
        else:
            #Se False transforma a string recebida num float
            population = float(population_str)                                             
        #Insere na lista population cada elemento de population
        populations.append(population)                                                     
    #Dicionário que determina que região está associado as siglas e população ao valores
    d = {"regiao": siglas, "populacao": populations}  
    #Grafico de heatmap, com geojson dividido por região do br
    figura_luz_para_todos = px.choropleth(d, geojson=br, locations='regiao', color='populacao',             
                                color_continuous_scale="PuBu", #Cor definida
                                featureidkey="properties.SIGLA",#Chave de interesse 
                                range_color=(0, 200),#A internsidade das cores, o range
                                scope="south america",#Mapa da america do sul
                                labels={'populacao':'População (mil)'},#Label do gráfico
                          )
    figura_luz_para_todos.update_layout(title = dict(
                                text='Distribuição Regional do Programa Luz Para Todos no Ano de {} [por mil habitantes]'.format(year),#.format responsável por associar o {} ao número de acordo com as labels
                                font=dict(size=20),#Determina o tamanho da letra
                                xref='paper', # Área central do gráfico
                                yref='container', # Área externa ao paper
                                x=0.5, # Faz o posicionamento horizontal do texto de acordo com o xref
                                y=0.95),# Faz o posicionamento vertical do texto de acordo com o yref
  
    )

    #Plota gráfico
    return figura_luz_para_todos
                                                        

#-------------------------------------------------Plotagem Tarifa Média--------------------------------------------------------------
#Declaração de entradas e saída   
@app.callback(  
   #As entradas são os valores atribuidos nas labels e as saídas são os gráficos selecionados pelo valor da label                                                                             
   Output('fig_tarifa_media', 'figure'),
   Input('classe_tarifa_media', 'value')
)
#Função tarifa_media determina o valor de x a partir dos valores de anos
def tarifa_media(anos_tarifa_media):
    if anos_tarifa_media == '2012':
        contador=1
    if anos_tarifa_media == '2013':
        contador=2
    if anos_tarifa_media == '2014':
        contador=3
    if anos_tarifa_media == '2015':
        contador=4
    if anos_tarifa_media == '2016':
        contador=5
    if anos_tarifa_media == '2017':
        contador=6
    if anos_tarifa_media == '2018':
        contador=7    
    # Variável vazia para coluna                                             
    h = 0 
    # Variável vazia para coluna                                              
    m = 0                      
    # Matriz 5 x 2                          
    tabela_tarifa_media = [[1 for i in range(2)] for i in range(5)]  
    #Armazena as regiões, o loop acontece 5 vezes para cobrir todas as regiões                            
    for q in range(5): 
        #Formando a matriz 5x2                                 
        for l in range(1):      
            #Preechendo a tabela com os dados definidos                       
           tabela_tarifa_media[h][0] = dados_tarifa_media[0][q]                   
           tabela_tarifa_media[h][1] = dados_tarifa_media[contador][q]                 
           h += 1
           m += 1
    #Lista vazia para armazenar anos
    anos = []     
    #Armazena os anos da tabela preenchida anteriormente
    for dado in tabela_tarifa_media:  
        #Adiciona os valores dos dados aos anos                            
        anos.append(dado[1])     
    #Lista vazia para armazenar os valores                    
    valor = []
    #Armazena os dados de energia da tabela preenchida anteriormente
    for dado in tabela_tarifa_media:
        #Adiciona os valores de energia 
        valor.append(dado[0])
    #Lógica de funcionamento dos anos
    z = 2011 + contador                
    #Plotagem de tarifa média                     
    barra = go.Bar(x= anos,# eixo x, em anos
                y= valor,# eixo y, região
                orientation='h', # gráfico na horizontal
                name='Tarifa Média [R$/MWh]',# Nome dos gráficos
                marker={'color': '#38AECC'}) # Cor dos gráficos   
    #Título do gráfico 
    config = go.Layout(title='Tarifa Média por Região [R$/MWh]- {}'.format(z), #.format responsável por nomear os anos de acordo com as labels
                    yaxis={'title': 'região'},# Título do eixo y 
                    xaxis={'title': ''}
                    )                                   
    trace = [barra]# Variável que armazena o tipo de gráfico
    figura_tarifa_media = go.Figure(data=trace, layout=config)# Transforma em fig as informações
    
    #Plota gráfico
    return figura_tarifa_media

#-------------------------------------------------Plotagem Consumo vs PIB--------------------------------------------------------------
#Declaração de entradas e saída   
@app.callback(  
   #As entradas são os valores atribuidos nas labels e as saídas são os gráficos selecionados pelo valor da label                                                                             
    Output('fig_consumo_pib', 'figure'),
    Input('classe_consumo_pib', 'value')
)
#Função que determina as regiões e dispara classe_tarifa_media
def consumo_pib(local):
    if local=='Nor':
        counter=0
        regiao_consumo_pib='Norte'
    if local=='Nord':
        counter=1
        regiao_consumo_pib='Nordeste'
    if local=='Sd':
        counter=2
        regiao_consumo_pib='Sudeste'
    if local=='Sl':
        counter=3
        regiao_consumo_pib='Sul'
    if local=='CO':
        counter=4
        regiao_consumo_pib='Centro-Oeste'
    #Declara variável vazia
    h=0                    
    #Declara matriz que será preenchida pelos dados 3x7
    tabela_consumo = [[1 for i in range(3)] for i in range(7)]     
    #Variável armazena os dados da região, determinando q receba e finalize em 7
    for q in range (7):
         #Formando a matriz, determinando q l receba dado e siga as instruções seguintes                                    
        for l in range (1):
            #Adiciona a tabela os valores dos dados de consumo em cada posição                               
            tabela_consumo[h][0]= dados_consumo[q][l+counter]             
            #Adiciona a tabela os valores relacionado aos anos           
            tabela_consumo[h][1]= (2012+q)                         
            h=h+1   
            
    #Lista vazia
    anos= []
    #Procura o dado na tabela
    for data_consumo_pib in tabela_consumo: 
        #Adiciona os valores do dados aos anos                        
        anos.append(data_consumo_pib[1])    
    #Lista_vazia                           
    valor_consumo= []     
    #Procura dado na tabela    
    for data_consumo_pib in tabela_consumo:    
        #Adiciona os valores do dados aos anos                                
        valor_consumo.append(data_consumo_pib[0])                              

        
    #Filtrar dados de PIB
    #Declara variável vazia
    h=0     
    
    #Declara matriz que será preenchida pelos dados 3x7                                               
    tabela_pib = [[1 for i in range(3)] for i in range(7)]   
    #Variável armazena os dados da região, determinando q receba e finalize em 7
    for q in range (7):                                    
        for l in range (1): 
            #Adiciona a tabela os valores dos dados pib em cada posição                               
            tabela_pib[h][0]= dados_PIB[q][l+counter]
            #Adiciona a tabela os valores dos dados relacionados aos anos
            tabela_pib[h][1]= (2012+q)
            h=h+1  
    #Lista vazia                        
    valor_pib= []
    #Procura dado na tabela
    for dadopib in tabela_pib:  
        #Adiciona os valores dos dados ao pib                             
        valor_pib.append(dadopib[0])                          

    
    # Criar grafico com dois eixos y
    #Para criar gráfico com dois eixos, é necessário implementar do Boolean para make_subplots e eixos

    figura_consumo_pib = make_subplots(specs=[[{"secondary_y": True}]])   #Cria a fig com dois eixos y

    # Add traces/linhas
    figura_consumo_pib.add_trace(
        go.Scatter(x=anos, y=valor_consumo, name="consumo",line = {'color': '#07325a'}),
        secondary_y=False,                                 #Determina uma linha como False para a fig de dois y
    )

    figura_consumo_pib.add_trace(
        go.Scatter(x=anos, y=valor_pib, name="PIB",line = {'color': '#2178bb'}),
        secondary_y=True,                                  #Determina uma linha como False para a fig de dois y
    )

    # Add figure title/título
    figura_consumo_pib.update_layout(title = dict(
                                    text='Consumo e PIB na Região {} [MWh/R$]'.format(regiao_consumo_pib),
                                    font=dict(size=20),
                                    xref='paper', # Área central do gráfico
                                    yref='container', # Área externa ao paper
                                    x=0.5, # Faz o posicionamento horizontal do texto de acordo com o xref
                                    y=0.95),
    )

    # Set x-axis title
    figura_consumo_pib.update_xaxes(title_text="Anos")                    #Nomeia linha x como anos

    # Set y-axes titles
    figura_consumo_pib.update_yaxes(title_text="Consumo", secondary_y=False)
    figura_consumo_pib.update_yaxes(title_text="PIB", secondary_y=True)
    figura_consumo_pib.update_layout(plot_bgcolor="#e8ecf4")              #Background grafico
    #fig.update_layout(paper_bgcolor="#A9E0ED")            #Background grafico
    figura_consumo_pib.update_layout(font_color="black")                  #Cor da legenda 

    #Plota gráfico
    return figura_consumo_pib

#-------------------------------------------------Plotagem Geracao vs Consumo--------------------------------------------------------------
@app.callback(
    Output("fig_geracao_consumo","figure"),
    Input("classe_geracao_consumo","value")
)

def graficos(regiao):
    f = open("Anuário Estatístico de Energia Elétrica 2020 - Workbook.xlsx - Tabela 2.4.csv",encoding="utf8")
    # f.read lê todo o conteúdo do arquivo e retorna uma string
    # .split("\n") divide essa string do conteudo em linhas
    content = f.read().split("\n")
    #lista que armazena energia de cada região
    armazena_data = filtra_dados(regiao)

    #variável que armazena informações do gráfico      
    linha = go.Scatter(x = years, #anos do gráfico, eixo x
                       y = armazena_data, #energia do gráfico, eixo y
                       mode = 'lines', #modo do gráfico, tipo linhas
                       name = 'Geracao [GWh]', #nome das linhas
                       line = {'color': '#2178bb'}) #cor das linhas

    # abre o arquivo
    f = open("Anuário Estatístico de Energia Elétrica 2020 - Workbook.xlsx - Tabela 3.1.csv",encoding="utf8")
    # f.read lê todo o conteúdo do arquivo e retorna uma string
    # .split("\n") divide essa string do conteudo em linhas
    content = f.read().split("\n")
    
    #lista que armazena energia de cada região
    armazena_data = filtra_dados(regiao)
    #variável que armazena informações do gráfico
    barra = go.Bar(x = years,#anos do gráfico, eixo x
                       y = armazena_data, #energia do gráfico, eixo y
                       name = 'Consumo [GWh]',#nome das barras
                       marker = {'color': '#07325a'})#cor das barras


    config = go.Layout( title = dict(
                                text='Consumo Vs Geração na Região '+ regiao + ' [GWh]',
                                font=dict(size=20),
                                xref='paper', # Área central do gráfico
                                yref='container', # Área externa ao paper
                                x=0.5, # Faz o posicionamento horizontal do texto de acordo com o xref
                                y=0.95), # Faz o posicionamento vertical do texto de acordo com yref#título do gráfico
                                yaxis={'title':'Geração/Consumo [GWh]'}, #título eixo y
                                xaxis={'title':''}) #título eixo x
    trace = [linha, barra] #variável que armazena gráficos
    figura_geracao_consumo = go.Figure(data=trace, layout=config)
   
    return figura_geracao_consumo

if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)




