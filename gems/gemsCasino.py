import discord
from discord.ext import commands
from discord.ext.commands import bot
from gems import gemsFonctions as GF
from core import gestion as ge
import gg_lib as gg
from languages import lang as lang_P


class GemsCasino(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def gamble(self, ctx, valeur):
        """**[bet]** | Are you a gambler's man?"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["valeur"] = valeur
        ge.socket.send_string(gg.std_send_command("gamble", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]
        if desc["type"] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 3), color= 13752280, description = desc["desc"])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def slots(self, ctx, imise = None):
        """**{bet}** | Slot machine, minimum bet is 10 :gem:`gems`"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["imise"] = imise
        ge.socket.send_string(gg.std_send_command("slots", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        lang = msg["lang"]
        if msg["type"] == "OK":
            desc = "{0}\n{1}".format(lang_P.forge_msg(lang, "casino", [msg["misemax"]], False, 6), lang_P.forge_msg(lang, "casino", [msg["mise"]], False, 7))
            e = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 9), color= 13752280, description = desc)
            desc = ""
            for i in range(0, 9):
                if i == 3:
                    desc += "\n"
                elif i == 6:
                    desc += " :arrow_backward:\n"
                desc += msg["result"][i]
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 8), value=desc, inline=False)
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 3), value=msg["desc"], inline=False)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = e)
        else:
            await ctx.channel.send(msg["desc"])

    @commands.command(pass_context=True)
    async def roulette(self, ctx, mise, valeur):
        """**[bet] [value]** | Flat roulette"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["valeur"] = valeur
        param["mise"] = mise
        ge.socket.send_string(gg.std_send_command("roulette", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        lang = msg["lang"]
        if msg["type"] == "OK":
            msgD = msg["desc"]
            desc = "{1}\n{0}".format(lang_P.forge_msg(lang, "casino", [GF.NumberList[int(valeur)//10], GF.NumberList[int(valeur) % 10]], False, 5), lang_P.forge_msg(lang, "casino", [int(mise)], False, 7))
            e = discord.Embed(title = lang_P.forge_msg(lang, "casino", None, False, 0), color= 13752280, description = desc)

            desc = "| :{0}::{1}: |".format(GF.NumberList[msgD["VB"]//10], GF.NumberList[msgD["VB"] % 10])
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 1), value=desc, inline=False)

            desc = "|"
            for one in msgD["VM"]:
                desc += " :{0}::{1}: |".format(GF.NumberList[one//10], GF.NumberList[one % 10])
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 2), value=desc, inline=False)

            desc = "{0}\n{1}".format(msgD["desc"], lang_P.forge_msg(lang, "casino", [msgD["gain"]], False, 4))
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 3), value=desc, inline=False)

            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = e)
        else:
            await ctx.channel.send(msg["desc"])

    @commands.command(pass_context=True)
    async def marketbet(self, ctx, item, perCent, mise):
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["item"] = item
        param["perCent"] = perCent
        param["mise"] = mise
        ge.socket.send_string(gg.std_send_command("marketbet", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        lang = msg["lang"]
        if msg["type"] == "OK":
            e = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 0), color=13755260, description=msg["desc"])
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = e)
        else:
            await ctx.channel.send(msg["desc"])

def setup(bot):
    bot.add_cog(GemsCasino(bot))
    open("help/cogs.txt", "a").write("GemsCasino\n")
