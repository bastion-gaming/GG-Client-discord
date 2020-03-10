import discord
from core import gestion as ge
from gems import gemsFonctions as GF
import gg_lib as gg
import datetime as dt


async def checklevel(message):
    ID = message.author.id
    nom = message.author.name
    ge.socket.send_string(gg.std_send_command("level", ID, ge.name_pl))
    desc = GF.msg_recv()
    if desc[0] == "Level UP":
        print("Level UP >> {0}".format(nom))
        title = "Level UP | Get Gems"
        lvl_desc = ":tada: {0} {1}".format(nom, desc[1])
        msg = discord.Embed(title = title, color= 6466585, description = lvl_desc, timestamp=dt.datetime.now())
        msg.set_thumbnail(url=message.author.avatar_url)
        msg.set_footer(text=message.author.name)
        await message.channel.send(embed = msg)
    if len(desc) > 2:
        if desc[0] != "Error":
            title = "Success"
            descS = ""
            for i in range(1, len(desc[2])):
                descS += "{0}\n".format(desc[2][i])
            msg = discord.Embed(title = title, color= 6824352, description = descS, timestamp=dt.datetime.now())
            msg.set_thumbnail(url=message.author.avatar_url)
            msg.set_footer(text=message.author.name)
            await message.channel.send(embed = msg)
    return False
