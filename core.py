import discord
from discord.ext import commands
from discord.ext.commands import Bot
from core import gestion as ge, utils, level as lvl
from gems import gemsFonctions as GF
import gg_lib as gg

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("core/version.txt").read().replace("\n", "")
TOKEN = open("token/token.txt", "r").read().replace("\n", "")
PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
client = commands.Bot(command_prefix = "{0}".format(PREFIX))
NONE = open("help/cogs.txt", "w")
NONE = open("help/help.txt", "w")

client.remove_command("help")

# Au démarrage du Bot.
@client.event
async def on_ready():
    global GGconnect
    print('Connecté avec le nom : {0.user}'.format(client))
    print('PREFIX = '+str(PREFIX))
    print('\nGet Gems - Client Discord '+VERSION)
    GF.setglobalguild(client.get_guild(utils.ServIDmoji))
    print('------\n')
    GGconnect = ge.ZMQ()
    print('------\n')

####################### Commande help.py #######################

client.load_extension('help.help')

################### Core ############################

client.load_extension('core.utils')


####################### Welcome ####################################

@client.event
async def on_guild_join(guild):
    if guild.system_channel != None:
        systemchannel = guild.system_channel
    else:
        systemchannel = 0
    # sql.new(guild.id, "Guild")
    param = dict()
    param["IDGuild"] = guild.id
    ge.socket.send_string(gg.std_send_command("NewServer", guild.id, ge.name_pl, param))
    GF.msg_recv()
    await systemchannel.send('Bonjour {}!'.format(guild.name))


####################### Stat ####################################

@client.event
async def on_message(message):
    if not (message.author.bot) and message.content.startswith(PREFIX):
        if GGconnect:
            await lvl.checklevel(message)
        await client.process_commands(message)

####################### Commande gems.py #######################

client.load_extension('gems.gemsBase')

client.load_extension('gems.gemsPlay')

# client.load_extension('gems.gemsGuild')

client.load_extension('gems.gemsEvent')

client.load_extension('gems.gemsAdmin')

####################### Lancemement du bot ######################

client.run(TOKEN)
