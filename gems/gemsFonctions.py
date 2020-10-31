from core import gestion as ge
import zmq
import gg_lib as gg


global globalguild


def setglobalguild(guild):
    global globalguild
    globalguild = guild


NumberList = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "keycap_ten"]


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
