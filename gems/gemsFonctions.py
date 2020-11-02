from core import gestion as ge
import zmq
import gg_lib as gg
from languages import lang as lang_P


global globalguild


def setglobalguild(guild):
    global globalguild
    globalguild = guild


NumberList = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "keycap_ten"]


class objetTrad():

    def __init__(self, nom, type, num):
        self.nom = nom
        self.type = type
        self.num = num


objets = [
    objetTrad("backpack", "TradItem", 0),
    objetTrad("hyperpack", "TradItem", 1),
    objetTrad("fishhook", "TradItem", 2),

    objetTrad("cobblestone", "TradItem", 3),
    objetTrad("iron", "TradItem", 4),
    objetTrad("gold", "TradItem", 5),
    objetTrad("diamond", "TradItem", 6),
    objetTrad("emerald", "TradItem", 7),
    objetTrad("ruby", "TradItem", 8),

    objetTrad("fish", "TradItem", 9),
    objetTrad("tropicalfish", "TradItem", 10),
    objetTrad("blowfish", "TradItem", 11),
    objetTrad("octopus", "TradItem", 12),

    objetTrad("seed", "TradItem", 13),
    objetTrad("cacao", "TradItem", 14),
    objetTrad("potato", "TradItem", 15),

    objetTrad("oak", "TradItem", 16),
    objetTrad("spruce", "TradItem", 17),
    objetTrad("palm", "TradItem", 18),
    objetTrad("hops", "TradItem", 19),
    objetTrad("grapes", "TradItem", 20),

    objetTrad("wine", "TradItem", 21),
    objetTrad("beer", "TradItem", 22),

    objetTrad("chocolate", "TradItem", 23),
    objetTrad("fries", "TradItem", 24),
    objetTrad("cookie", "TradItem", 25),
    objetTrad("candy", "TradItem", 26),
    objetTrad("lollipop", "TradItem", 27),

    objetTrad("pumpkin", "TradItem", 28),
    objetTrad("pumpkinpie", "TradItem", 29),
    objetTrad("cupcake", "TradItem", 30),

    objetTrad("fishingrod", "TradOutil", 0),

    objetTrad("pickaxe", "TradOutil", 1),
    objetTrad("iron_pickaxe", "TradOutil", 2),
    objetTrad("diamond_pickaxe", "TradOutil", 3),

    objetTrad("shovel", "TradOutil", 4),
    objetTrad("iron_shovel", "TradOutil", 5),
    objetTrad("diamond_shovel", "TradOutil", 6),

    objetTrad("planting_plan", "TradOutil", 7),
    objetTrad("barrel", "TradOutil", 8),
    objetTrad("furnace", "TradOutil", 9),

    objetTrad("bank", "TradUpgrade", 0)
]


def build_idmoji(nameElem):
    """Version 3.0 | Permet de construire l'idmoji de l'item"""
    TupleIdmoji = globalguild.emojis
    for x in TupleIdmoji:
        if x.name == "gem_{}".format(nameElem):
            idmoji = '<:gem_{0}:{1}>'.format(nameElem, x.id)
            return idmoji
        elif x.name == "upgrade_{}".format(nameElem):
            idmoji = '<:upgrade_{0}:{1}>'.format(nameElem, x.id)
            return idmoji
        elif x.name == nameElem:
            idmoji = '<:{0}:{1}>'.format(nameElem, x.id)
            return idmoji
    return ':{0}:'.format(nameElem)


def trad_objet(lang, nameElem):
    for o in objets:
        if o.nom == nameElem:
            return lang_P.forge_msg(lang, o.type, None, False, o.num)
    return nameElem


def trad_objet_inv(nameElem):
    nameElem0 = MEFTrad(nameElem)
    for i in range(0, 31):
        nameElemFR = MEFTrad(lang_P.forge_msg("FR", "TradItem", None, False, i))
        nameElemEN = MEFTrad(lang_P.forge_msg("EN", "TradItem", None, False, i))
        if nameElem0 == nameElemFR or nameElem0 == nameElemEN:
            for x in objets:
                if x.type == "TradItem" and x.num == i:
                    return x.nom
    for i in range(0, 10):
        nameElemFR = MEFTrad(lang_P.forge_msg("FR", "TradOutil", None, False, i))
        nameElemEN = MEFTrad(lang_P.forge_msg("EN", "TradOutil", None, False, i))
        if nameElem0 == nameElemFR or nameElem0 == nameElemEN:
            for x in objets:
                if x.type == "TradOutil" and x.num == i:
                    return x.nom
    for i in range(0, 1):
        nameElemFR = MEFTrad(lang_P.forge_msg("FR", "TradUpgrade", None, False, i))
        nameElemEN = MEFTrad(lang_P.forge_msg("EN", "TradUpgrade", None, False, i))
        if nameElem0 == nameElemFR or nameElem0 == nameElemEN:
            for x in objets:
                if x.type == "TradUpgrade" and x.num == i:
                    return x.nom
    return nameElem


def msg_recv():
    #  Get the reply.
    socks = dict(ge.poll.poll(ge.REQUEST_TIMEOUT))
    if socks.get(ge.socket) == zmq.POLLIN:
        message = gg.std_receive_command(ge.socket.recv())
        msg = message['msg']
    else:
        # msg = {"type": "Error", "lang": "FR", "desc": "Aucune réponse du serveur"}
        # msg = {"type": "Error", "lang": "EN", "desc": "No reply from the server"}
        msg = {'error': 100, 'etat': 'No reply from the server', 'lang': 'EN'}
        # Socket is confused. Close and remove it.
        ge.socket.setsockopt(zmq.LINGER, 0)
        ge.socket.close()
        ge.poll.unregister(ge.socket)
        # Create new connection
        ge.socket = ge.context.socket(zmq.REQ)
        ge.socket.connect(ge.SERVER_ENDPOINT)
        ge.poll.register(ge.socket, zmq.POLLIN)

    msg = MEF(msg, "\\n", "\n")
    return msg


def MEF(msg, source, destination):
    if type(msg) is dict:
        for k in msg.keys():
            if type(msg[k]) is str:
                msg[k] = msg[k].replace(source, destination)
            else:
                MEF(msg[k], source, destination)
    elif type(msg) is list:
        for x in range(0, len(msg)):
            if type(msg[x]) is str:
                msg[x] = msg[x].replace(source, destination)
            else:
                MEF(msg[x], source, destination)
    elif type(msg) is str:
        msg = msg.replace(source, destination)
    return msg


def MEFTrad(msg):
    msg = MEF(msg, "à", "a")
    msg = MEF(msg, "â", "a")
    msg = MEF(msg, "ä", "a")

    msg = MEF(msg, "é", "e")
    msg = MEF(msg, "è", "e")
    msg = MEF(msg, "ê", "e")
    msg = MEF(msg, "ë", "e")

    msg = MEF(msg, "î", "i")
    msg = MEF(msg, "ï", "i")

    msg = MEF(msg, "ô", "o")
    msg = MEF(msg, "ö", "o")

    msg = MEF(msg, "ù", "u")

    msg = MEF(msg, "ç", "c")
    return msg


def time_aff(time):
    # Traduit une valeur time (en secondes) en valeur HH:mm:ss
    # (avec un emoji correspondant devant)
    dtime = dict()
    dtime["timeH"] = int(time / 60 / 60)
    dtime["time"] = time - dtime["timeH"] * 3600
    dtime["timeM"] = int(dtime["time"] / 60)
    dtime["timeS"] = int(dtime["time"] - dtime["timeM"] * 60)
    if dtime["timeM"] <= 30:
        if dtime["timeH"] % 12 == 0:
            dtime["cl"] = "12"
        else:
            dtime["cl"] = dtime["timeH"] % 12
        dtime["cl"] = "clock{0}30".format(dtime["cl"])
    else:
        if dtime["timeH"] % 12 == 0:
            dtime["cl"] = "12"
        else:
            dtime["cl"] = (dtime["timeH"] % 12)+1
        dtime["cl"] = "clock{0}".format(dtime["cl"])
    return dtime
