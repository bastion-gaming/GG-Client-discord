import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import zmq
import gg_lib as gg
import time

name_pl = "discord" # Nom de la plateforme

REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://localhost:5555"

admin = 0
Inquisiteur = 1
Joueurs = 2
rolesID = [[417451897729843223],[417451897729843223,417451604141277185],[417451897729843223,417451604141277185,423606460908306433]]
guildID = [634317171496976395,640507787494948865,478003352551030796,129364058901053440]

def permission(ctx,grade):
    roles = ctx.author.roles
    for role in roles :
        if role.id in rolesID[grade] or (ctx.guild.id in guildID and role.permissions.administrator):
            return True
    return False


context = zmq.Context(1)

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect(SERVER_ENDPOINT)
# TIMEOUT
poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)

def ZMQ():
    context = zmq.Context(1)

    #  Socket to talk to server
    print("Connecting to Get Gems server…")
    socket = context.socket(zmq.REQ)
    socket.connect(SERVER_ENDPOINT)
    # TIMEOUT
    poll = zmq.Poller()
    poll.register(socket, zmq.POLLIN)

    socket.send_string(gg.std_send_command("connect", "__client", name_pl))
    time.sleep(1)
    socks = dict(poll.poll(REQUEST_TIMEOUT))
    if socks.get(socket) == zmq.POLLIN:
        msg = socket.recv()
        if msg.decode() == "1":
            print("Connected to Get Gems server")
    else:
        print("Aucune réponse du serveur")
        # Socket is confused. Close and remove it.
        socket.setsockopt(zmq.LINGER, 0)
        socket.close()
        poll.unregister(socket)
    return True