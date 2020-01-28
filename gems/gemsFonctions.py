import discord
import random as r
import time as t
import datetime as dt
import json
from core import gestion as ge
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from operator import itemgetter
import zmq
import gg_lib as gg


global globalguild

def setglobalguild(guild):
    global globalguild
    globalguild = guild


#========== Couldown pour la fonction antispam ==========
couldown_72h = 86400*3
couldown_48h = 86400*2
couldown_36h = 86400 + 86400/2
couldown_24h = 86400
couldown_23h = 3600*23
couldown_22h = 3600*22
couldown_21h = 3600*21
couldown_20h = 3600*20
couldown_19h = 3600*19
couldown_18h = 3600*18
couldown_17h = 3600*17
couldown_16h = 3600*16
couldown_15h = 3600*15
couldown_14h = 3600*14
couldown_13h = 3600*13
couldown_12h = 3600*12
couldown_11h = 3600*11
couldown_10h = 3600*10
couldown_9h = 3600*9
couldown_8h = 3600*8
couldown_7h = 3600*7
couldown_6h = 3600*6
couldown_5h = 3600*5
couldown_4h = 3600*4
couldown_3h = 3600*3
couldown_2h = 3600*2
couldown_1h = 3600
couldown_30m = 3600/2
couldown_20m = 3600/3
couldown_15m = 3600/4
couldown_10m = 3600/6
couldown_5m = 3600/12
couldown_30s = 30
couldown_15s = 15
couldown_10s = 10
couldown_8s = 8
couldown_6s = 6
couldown_4s = 4
# nb de sec nécessaire entre 2 commandes


def get_idmoji(nameElem):
    """Version 2.0 | Permet de connaitre l'idmoji de l'item"""
    TupleIdmoji = globalguild.emojis
    for x in TupleIdmoji:
        if x.name == "gem_{}".format(nameElem):
            return x.id
        elif x.name == nameElem:
            return x.id


def msg_recv():
    #  Get the reply.
    socks = dict(ge.poll.poll(ge.REQUEST_TIMEOUT))
    if socks.get(ge.socket) == zmq.POLLIN:
        message = gg.std_receive_command(ge.socket.recv())
        msg = message['msg']
    else:
        msg = "Aucune réponse du serveur"
        # Socket is confused. Close and remove it.
        ge.socket.setsockopt(zmq.LINGER, 0)
        ge.socket.close()
        ge.poll.unregister(ge.socket)
        # Create new connection
        ge.socket = ge.context.socket(zmq.REQ)
        ge.socket.connect(ge.SERVER_ENDPOINT)
        ge.poll.register(ge.socket, zmq.POLLIN)
    try:
        for x in range(0, len(msg)-1):
            msg[x] = msg[x].replace("\\n", "\n")
    except:
        try:
            msg = msg.replace("\\n", "\n")
        except:
            a = False
    msg = msg_idmoji(msg)
    return msg


def msg_idmoji(msg):
    TupleIdmoji = globalguild.emojis
    for y in TupleIdmoji:
        test = "{idmoji["+ y.name +"]}"
        try:
            for x in range(0, len(msg)-1):
                msg[x] = msg[x].replace(test, str(get_idmoji(y.name)))
        except:
            msg = msg.replace(test, str(get_idmoji(y.name)))
    return msg


# def recette(ctx):
#     """Liste de toutes les recettes disponibles !"""
#     d_recette="Permet de voir la liste de toutes les recettes disponible !\n\n"
#     d_recette+="▬▬▬▬▬▬▬▬▬▬▬▬▬\n**Forge**\n"
#     for c in objetOutil:
#         for r in objetRecette :
#             if c.type == "forge":
#                 if c.nom == r.nom:
#                     d_recette += "<:gem_{0}:{1}>`{0}`: ".format(c.nom,get_idmoji(c.nom))
#                     if r.nb1 > 0:
#                         d_recette += "{0} <:gem_{1}:{2}>`{1}` ".format(r.nb1, r.item1, get_idmoji(r.item1))
#                     if r.nb2 > 0:
#                         d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb2, r.item2, get_idmoji(r.item2))
#                     if r.nb3 > 0:
#                         d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb3, r.item3, get_idmoji(r.item3))
#                     if r.nb4 > 0:
#                         d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb4, r.item4, get_idmoji(r.item4))
#                     d_recette += "\n"
#
#     msg = discord.Embed(title = "Recettes",color= 15778560, description = d_recette)
#     return msg
