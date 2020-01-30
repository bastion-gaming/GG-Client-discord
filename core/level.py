import discord
from core import gestion as ge
from gems import gemsFonctions as GF
import gg_lib as gg


async def checklevel(message):
    ID = message.author.id
    ge.socket.send_string(gg.std_send_command("level", ID, ge.name_pl))
    desc = GF.msg_recv()
    if desc != "" and desc[1] != "Aucune réponse du serveur" and desc[1] != "Aucun compte utilisateur n'a été trouvé":
        title = "Level UP | Get Gems"
        desc[1] = desc[1].replace("{PlayerName}", message.author.name)
        msg = discord.Embed(title = title, color= 6466585, description = desc[1])
        msg.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed = msg)
    return False
