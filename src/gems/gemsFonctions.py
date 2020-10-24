from core import gestion as ge
import zmq
import gg_lib as gg


global globalguild


def setglobalguild(guild):
    global globalguild
    globalguild = guild


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
    elif type(msg) is float:
        pass
    else:
        msg = msg.replace(source, destination)
    return msg
