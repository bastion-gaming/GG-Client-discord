import discord
from core import gestion as ge
from gems import gemsFonctions as GF
import gg_lib as gg

async def checklevel(message):
    ID = message.author.id
    ge.socket.send_string(gg.std_send_command("level", ID, ge.name_pl))
    desc = GF.msg_recv()
    if desc != "" and desc != "Aucune réponse du serveur" and desc != "Aucun compte utilisateur n'a été trouvé":
        title = "Level UP | Get Gems"
        desc = desc.replace("{PlayerName}", message.author.name)
        msg = discord.Embed(title = title,color= 6466585, description = desc)
        msg.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed = msg)
    return False
