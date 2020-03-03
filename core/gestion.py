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
rolesID = [[417451897729843223], [417451897729843223, 417451604141277185], [417451897729843223, 417451604141277185, 423606460908306433]]
guildID = [634317171496976395, 417445502641111051, 640507787494948865, 478003352551030796, 129364058901053440] # Get Gems | Bastion | Bastion Twitch | Test | TopazDev


def permission(ctx, grade):
    roles = ctx.author.roles
    for role in roles :
        if role.id in rolesID[grade] or (ctx.guild.id in guildID and role.permissions.administrator):
            return True
    return False


def nom_ID(nom):
    """Convertis un nom en ID discord """
    if len(nom) == 21:
        ID = int(nom[2:20])
    elif len(nom) == 22:
        ID = int(nom[3:21])
    elif len(nom) == 18:
        ID = int(nom)
    else:
        ID = -1
    return(ID)


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
        print("No reply from the server")
        # Socket is confused. Close and remove it.
        socket.setsockopt(zmq.LINGER, 0)
        socket.close()
        poll.unregister(socket)
        return False
    return True
