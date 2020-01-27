import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import aiohttp

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("core/version.txt").read().replace("\n","")
TOKEN = open("token/token.txt", "r").read().replace("\n","")
PREFIX = open("core/prefix.txt","r").read().replace("\n","")
client = commands.Bot(command_prefix = "{0}".format(PREFIX))
NONE = open("help/cogs.txt","w")
NONE = open("help/help.txt","w")

client.remove_command("help")

# Au démarrage du Bot.
@client.event
async def on_ready():
	print('Connecté avec le nom : {0.user}'.format(client))
	print('PREFIX = '+str(PREFIX))
	print('\nGet Gems - Client Discord '+VERSION)
	GF.setglobalguild(client.get_guild(utils.ServIDmoji))
	print('------\n')

####################### Commande help.py #######################

client.load_extension('help.help')

################### Core ############################

client.load_extension('core.utils')

####################### Stat ####################################

@client.event
async def on_message(message):
	await lvl.checklevel(message, "gems")
	await client.process_commands(message)

####################### Commande gems.py #######################

client.load_extension('gems.gemsBase')

client.load_extension('gems.gemsPlay')

client.load_extension('gems.gemsGuild')

client.load_extension('gems.gemsEvent')

####################### Lancemement du bot ######################

client.run(TOKEN)
