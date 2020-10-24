import discord
from core import gestion as ge
from gems import gemsFonctions as GF
import gg_lib as gg
import datetime as dt
from languages import lang as lang_P


async def checklevel(message):
    ID = message.author.id
    nom = message.author.name
    ge.socket.send_string(gg.std_send_command("level", ID, ge.name_pl))
    recv = GF.msg_recv()
    await message.channel.send(recv)
    lang = recv['lang']
    if recv['error'] in [100, 404]:
        print("Level Error {1} | {0} | {2}".format(recv['etat'], recv['error'], nom))
        return False
    try:
        if recv['etat'] == "Level UP":
            print("Level UP >> {0}".format(nom))
            title = "Level UP | Get Gems"
            lvl_desc = ":tada: {0} {1} {2}".format(nom, lang_P.forge_msg(lang, "level", [recv['gain']['level']], False, 0), lang_P.forge_msg(lang, "level", [recv['gain']['gems']], False, 1))
            msg = discord.Embed(title = title, color= 6466585, description = lvl_desc, timestamp=dt.datetime.now())
            msg.set_thumbnail(url=message.author.avatar_url)
            msg.set_footer(text=message.author.name)
            await message.channel.send(embed = msg)
        if recv['success'] is not False:
            title = "Success"
            descS = ""
            for i in range(0, len(recv['success'])-1):
                descS += "{0}\n".format(recv['success'][i])
            msg = discord.Embed(title = title, color= 6824352, description = descS, timestamp=dt.datetime.now())
            msg.set_thumbnail(url=message.author.avatar_url)
            msg.set_footer(text=message.author.name)
            await message.channel.send(embed = msg)
    except KeyError:
        pass
    return False
