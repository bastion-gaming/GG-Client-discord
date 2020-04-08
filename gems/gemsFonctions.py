from core import gestion as ge
import zmq
import gg_lib as gg


global globalguild


def setglobalguild(guild):
    global globalguild
    globalguild = guild


# ========== Couldown pour la fonction antispam ==========
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


NumberList = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "keycap_ten"]


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
        # msg = {"type": "Error", "lang": "FR", "desc": "Aucune réponse du serveur"}
        msg = {"type": "Error", "lang": "EN", "desc": "No reply from the server"}
        # Socket is confused. Close and remove it.
        ge.socket.setsockopt(zmq.LINGER, 0)
        ge.socket.close()
        ge.poll.unregister(ge.socket)
        # Create new connection
        ge.socket = ge.context.socket(zmq.REQ)
        ge.socket.connect(ge.SERVER_ENDPOINT)
        ge.poll.register(ge.socket, zmq.POLLIN)

    msg = MEF(msg, "\\n", "\n")
    TupleIdmoji = globalguild.emojis
    for y in TupleIdmoji:
        test = "{idmoji[" + y.name + "]}"
        msg = MEF(msg, test, str(get_idmoji(y.name)))
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
    elif type(msg) is int:
        pass
    else:
        msg = msg.replace(source, destination)
    return msg
