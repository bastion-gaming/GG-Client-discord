import discord
from discord.ext import commands
from discord.ext.commands import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core import gestion as ge, utils, level as lvl
from gems import gemsFonctions as GF
import gg_lib as gg
from datetime import date

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("core/version.txt").read().replace("\n", "")
TOKEN = open("token/token.txt", "r").read().replace("\n", "")
PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
client = commands.Bot(command_prefix="{0}".format(PREFIX))
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
    GGconnect, utils.nb_saisons, utils.date_saison = ge.ZMQ()
    print('------\n')
    activity = discord.Activity(type=discord.ActivityType.playing, name="{0}help | Season {1}".format(PREFIX, utils.nb_saisons))
    await client.change_presence(status=discord.Status.online, activity=activity)

    scheduler = AsyncIOScheduler()
    tab_date_saison = utils.date_saison.split("-")
    scheduler.add_job(request_date_end_season, 'date', run_date=date(int(tab_date_saison[2]), int(tab_date_saison[1]), int(tab_date_saison[0])), id="REQUEST_SEASON")
    scheduler.start()
    scheduler.print_jobs()


async def request_date_end_season():
    ge.socket.send_string(gg.std_send_command('req_date', '__client', 'discord'))
    socks = dict(ge.poll.poll(ge.REQUEST_TIMEOUT))
    if socks.get(ge.socket) == ge.zmq.POLLIN:
        msg = ge.socket.recv()
        msg_DEC = msg.decode()
        utils.nb_saisons = utils.nb_saisons + 1
        utils.date_saison = msg_DEC
        D = msg_DEC.split("-")
        scheduler = AsyncIOScheduler()
        scheduler.reschedule_job('REQUEST_SEASON', trigger='date', run_date=date(int(D[2]), int(D[1]), int(D[0])))
        scheduler.start()
        scheduler.print_jobs()
        activity = discord.Activity(type=discord.ActivityType.playing, name="{0}help | Season {1}".format(PREFIX, utils.nb_saisons))
        await client.change_presence(status=discord.Status.online, activity=activity)

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
    param = dict()
    param["IDGuild"] = guild.id
    param["name"] = guild.name
    ge.socket.send_string(gg.std_send_command("NewServer", guild.id, ge.name_pl, param))
    GF.msg_recv()
    await systemchannel.send('Bonjour **{0}**!'.format(guild.name))


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

client.load_extension('gems.gemsSuccess')

# client.load_extension('gems.gemsGuild')

# client.load_extension('gems.gemsEvent')

client.load_extension('gems.gemsAdmin')

####################### Lancemement du bot ######################

try:
    client.run(TOKEN)
except (KeyboardInterrupt, SystemExit):
    pass
