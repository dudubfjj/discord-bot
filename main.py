import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound, CommandInvokeError
from decouple import config
from time import sleep

import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import http.client
import json
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#I'M READY!
@client.event
async def on_ready():
    print(f'Estou conectado como {client.user}!')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Coloque o id da Gamersclub após o comando. Digite !help para ver os comandos.')
    elif isinstance(error, CommandNotFound):
        await ctx.send('O comando não existe. Digite !help para ver os comandos.')
    elif isinstance(error, CommandInvokeError):
        await ctx.send('Não foi possível obter essa informação. Verifique se os dados foram digitados corretamente.')
    else:
        raise error


#OLÁ
@client.command(name='oi', help='Receba um olá do Bot :)')
async def send_hello(ctx):
    name = ctx.author.name
    response = "Olá, " + name

    await ctx.send(response)


#MUNDI UP
@client.command(name='fm', help="!fm para saber como conseguir o update mais recente do Football Manager.")
async def get_fm_update(ctx):
    url = 'https://www.facebook.com/BrasilMundiUP'
    response = f"Para comprar o update mais recente do FM, acesse {url} e mande uma mensagem no chat da Brasil MundiUP"
    await ctx.send(response)


#HORA
@client.command('hora', help="!hora informa a Data e Hora atual.")
async def send_time(ctx):
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y às %H:%M:%S")
    

    await ctx.send("Data e hora atual: " + now)


#GAMERSCLUB LAST GAME
@client.command(name='gc', help="Digite o id da GamersClub após o comando. Ex: !gc 322861")
async def get_url(ctx, id_gc):
    #options = ChromeOptions()
    #options.headless = True
    
    
    #user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    #options = webdriver.ChromeOptions()
    #options.headless = True
    #options.add_argument(f'user-agent={user_agent}')
    #options.add_argument("--window-size=1920,1080")
    #options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--allow-running-insecure-content')
    #options.add_argument("--disable-extensions")
    #options.add_argument("--proxy-server='direct://'")
    #options.add_argument("--proxy-bypass-list=*")
    #options.add_argument("--start-maximized")
    #options.add_argument('--disable-gpu')
    #options.add_argument('--disable-dev-shm-usage')
    #options.add_argument('--no-sandbox')
    
    #servico = Service(ChromeDriverManager().install())
    #navegador = webdriver.Chrome(service=servico, options=options)
    sleep(40)
    navegador.get(f'https://gamersclub.com.br/player/{id_gc}')

    nickname = navegador.find_element(By.CLASS_NAME, 'gc-profile-user-name').text

    stats_nome = navegador.find_elements(By.CLASS_NAME, 'StatsBoxPlayerInfoItem__name')
    stats_dado = navegador.find_elements(By.CLASS_NAME, 'StatsBoxPlayerInfoItem__value')

    lista_nome = []
    lista_dado = []
    dict_stats = {}

    for stat in stats_nome:
        estatistica = stat.text
        lista_nome.append(estatistica)

    for stat2 in stats_dado:
        estatistica2 = stat2.text
        lista_dado.append(estatistica2)

    for i, j in zip(lista_nome, lista_dado):
        dict_stats[i] = j

    await ctx.send(f'As stats da última partida do {nickname} são: ')

    for k, v in dict_stats.items():
        await ctx.send(f'{k} = {v}')
    
    navegador.quit()


#GAMERSCLUB HISTORICO MENSAL
@client.command(name='gcmes', help="Digite o id da GamersClub após o comando. Ex: !gcmes 322861")
async def get_url(ctx, id_gc):
    conn = http.client.HTTPSConnection("gamersclub.com.br")

    payload = ""

    headers = {
        'cookie': "_gcl_au=1.1.209042485.1667412074; _tt_enable_cookie=1; _ttp=07c8a5b2-ddbe-4b57-8db6-68428cd18630; language=pt-br; sib_cuid=69ba150b-aa6a-481d-b287-e81cb7879e92; _hjSessionUser_2263196=eyJpZCI6IjM5YzhlYjVjLTcyODctNWNlMy1hZmMzLWFhOWVlNDVmMGY1MSIsImNyZWF0ZWQiOjE2Njc0MTIxNTgyNTIsImV4aXN0aW5nIjp0cnVlfQ==; _hjMinimizedPolls=864076; _hjSessionUser_1963917=eyJpZCI6IjU4N2MzMzlkLTJkMWUtNTlmNS1iNzE2LTZmODljMmU1YTZmMyIsImNyZWF0ZWQiOjE2Njc0MTIwNzQ1MjEsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.3.195961545.1673814267; _hjDonePolls=864076%2C865658%2C872356%2C873600; gclubsess=46d3a3b97b4d88b68482b7f966d79ae373ea65d0; _hjHasCachedUserAttributes=true; SL_C_23361dd035530_VID=LFlRfyq_0v; SL_C_23361dd035530_KEY=a14d3638cda988422792e3613234743b983fdd9e; _gat_UA-187315934-4=1; _gat_UA-187315934-3=1; _gat_UA-64910362-1=1; _gat_UA-64910362-39=1; _ga_H7ETJY03DT=GS1.1.1674147919.225.1.1674147921.58.0.0; _ga_GDBFGFR1PC=GS1.1.1674147919.226.1.1674147921.58.0.0; _ga=GA1.3.159586927.1667412074",
        'authority': "gamersclub.com.br",
        'accept': "application/json, text/javascript, */*; q=0.01",
        'accept-language': "en-US,en;q=0.9,pt;q=0.8,fr;q=0.7",
        'referer': f"https://gamersclub.com.br/player/{id_gc}",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        'x-requested-with': "XMLHttpRequest"
        }

    conn.request("GET", f"/api/box/history/{id_gc}?json=", payload, headers)

    res = conn.getresponse()
    data = res.read()

    dict = data.decode("utf-8")

    stats = json.loads(dict)

    estatisticas = stats['stat']

    dados = []
    for itens_of_list in estatisticas:
        for key_of_dict, value_of_dict in itens_of_list.items():
            dados.append(value_of_dict)

    nome = []
    dado = []
    for i, v in enumerate(dados):
        if i % 2 == 0:
            nome.append(v)
        else:
            dado.append(v)

    for n, d in zip(nome, dado):
        await ctx.send(f'{n} = {d}')

#INFORMANDO LEVEL E PONTOS
@client.command(name='level', help='!level id para ver o level atual e quantos pontos faltam para subir.')
async def get_level(ctx, id_gc):
    options = ChromeOptions()
    options.headless = True
    navegador = webdriver.Chrome(options=options)
    navegador.get(f'https://gamersclub.com.br/player/{id_gc}')
    #sleep(30)
    #PEGANDO NICKNAME
    nickname = navegador.find_element(By.CLASS_NAME, 'gc-profile-user-name').text

    level_now = int(navegador.find_element(By.CLASS_NAME, 'PlayerLevel__text').text)
    if level_now < 21:
        next_level = level_now + 1
    rating = int(navegador.find_element(By.CLASS_NAME, 'StatsBoxRating__Score').text)
    if level_now < 20:
        max_rating = int(navegador.find_element(By.CLASS_NAME, 'StatsBoxProgressBar__maxRating').text)
    elif level_now >= 20:
        max_rating = 0
    
    #PONTOS QUE FALTAM PRA SUBIR DE LEVEL
    pontos_faltam = max_rating - rating

    if level_now < 20:
        await ctx.send(f'{nickname} atualmente é level {level_now} e faltam {pontos_faltam} pontos pra chegar no level {next_level}.')
    elif level_now >= 20 and level_now != 99:
        await ctx.send(f'{nickname} atualmente é level {level_now} com {rating} pontos. ')
    elif level_now == 99:
        await ctx.send(f'{nickname} atualmente é level {level_now} com {rating} pontos. O {nickname} jogou MAJOR! Tem que respeitar! ')

    navegador.quit()

#BANCO DE DADOS DE ID'S - GC
@client.command(name='showids', help="!showids mostra o nosso cadastro de id's da GamersClub")
async def show_ids(ctx):    
    cadastro = open('cadastro_id.txt', 'r')
    for n in cadastro.readlines():
        n = n.split(':')
        await ctx.send(f'{n[0]}: id = {n[1]}')
    cadastro.close()
    
#CADASTRANDO NOVAS ID'S
@client.command(name='cadastrar', help='!cadastrar e após o nick e id da GC para cadastrar uma nova id. Ex: !cadastrar dudu 322861')
async def cadastrar_ids(ctx, nickname, id_gc):
    cadastro = open('cadastro_id.txt','r+')
    if id_gc in cadastro.read():
        await ctx.send('Nosso banco de cadastros já possui este ID.')
    else:
        cadastro.writelines(f'\n{nickname}:{id_gc}')
        await ctx.send('Nickname e id cadastrados com sucesso!')
    cadastro.close()


TOKEN = config("TOKEN")
client.run(TOKEN)