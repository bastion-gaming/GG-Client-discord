import discord
from core import gestion as ge
from gems import gemsFonctions as GF
import gg_lib as gg


async def checklevel(message):
    ID = message.author.id
    nom = message.author.name
    ge.socket.send_string(gg.std_send_command("level", ID, ge.name_pl))
    desc = GF.msg_recv()
    if desc[0] == "Level UP":
        title = "Level UP | Get Gems"
        lvl_desc = ":tada: {0} {1}".format(nom, desc[1])
        msg = discord.Embed(title = title, color= 6466585, description = lvl_desc)
        msg.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed = msg)
    return False
