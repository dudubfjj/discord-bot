import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound, CommandInvokeError
from decouple import config
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
#criando navegador
servico = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")




client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

API_KEY = config('API_KEY')

#I'M READY!
@client.event
async def on_ready():
    print(f'Estou conectado como {client.user}!')


#GAMERSCLUB LAST GAME
@client.command(name='gc', help="Digite o id da GamersClub após o comando. Ex: !gc 322861")
async def get_url(ctx, id_gc):
    driver = uc.Chrome(options=options, service=servico)
    resp = driver.get('https://gamersclub.com.br/api/box/init/322861')
    print(resp.content)

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
 


TOKEN = config("TOKEN")
client.run(TOKEN)