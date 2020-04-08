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
        desc = GF.msg_recv()
        lang = desc["lang"]
        if desc["type"] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 9), color= 13752280, description = desc["desc"])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def roulette(self, ctx, mise, valeur):
        """**[bet] [value]** | Flat roulette"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["valeur"] = valeur
        param["mise"] = mise
        ge.socket.send_string(gg.std_send_command("roulette", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]
        if desc["type"] == "OK":
            msgD = desc["desc"]
            msg = lang_P.forge_msg(lang, "roulette", [GF.NumberList[int(valeur)//10], GF.NumberList[int(valeur) % 10]], False, 6)
            e = discord.Embed(title = lang_P.forge_msg(lang, "roulette", None, False, 0), color= 13752280, description = msg)

            msg = "| :{0}::{1}: |".format(GF.NumberList[msgD["VB"]//10], GF.NumberList[msgD["VB"] % 10])
            e.add_field(name=lang_P.forge_msg(lang, "roulette", None, False, 1), value=msg, inline=False)

            msg = "|"
            for one in msgD["VM"]:
                msg += " :{0}::{1}: |".format(GF.NumberList[one//10], GF.NumberList[one % 10])
            e.add_field(name=lang_P.forge_msg(lang, "roulette", None, False, 2), value=msg, inline=False)

            msg = "{2}\n{0}\n{1}".format(msgD["desc"], lang_P.forge_msg(lang, "roulette", [msgD["gain"]], False, 4), lang_P.forge_msg(lang, "roulette", [int(mise)], False, 5))
            e.add_field(name=lang_P.forge_msg(lang, "roulette", None, False, 3), value=msg, inline=False)

            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = e)
        else:
            await ctx.channel.send(desc["desc"])


def setup(bot):
    bot.add_cog(GemsCasino(bot))
    open("help/cogs.txt", "a").write("GemsCasino\n")
