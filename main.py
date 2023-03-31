import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound, CommandInvokeError
from decouple import config
import requests

import datetime


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#I'M READY!
@client.event
async def on_ready():
    print(f'Estou conectado como {client.user}!')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):#
        await ctx.send('Coloque o id da Gamersclub após o comando. Digite !help para ver os comandos.')
    elif isinstance(error, CommandNotFound):#
        await ctx.send('O comando não existe. Digite !help para ver os comandos.')
    elif isinstance(error, CommandInvokeError):#
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

    headers = {
        'authority': 'gamersclub.com.br',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,pt;q=0.8,fr;q=0.7',
        'referer': f'https://gamersclub.com.br/player/{id_gc}',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

    response = requests.get(f'https://gamersclub.com.br/api/box/init/{id_gc}', headers=headers)
    stat = response.json()
    
    estatisticas = stat['stats']

    stat = []
    value = []
    for itens_of_list in estatisticas:
        for key_of_dict, value_of_dict in itens_of_list.items():
            if key_of_dict in 'diff':
                pass       
            elif key_of_dict in 'stat':
                stat.append(value_of_dict)
            elif key_of_dict in 'value':
                value.append(value_of_dict)

    for s, v in zip(stat, value):
        await ctx.send(f'{s} = {v}')

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