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
    async def slots(self, ctx, imise = None):
        """**{bet}** | Slot machine, minimum bet is 10 :gem:`gems`"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["imise"] = imise
        ge.socket.send_string(gg.std_send_command("slots", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc[1]
        if desc[0] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 9), color= 13752280, description = desc[2])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[2])

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
        lang = desc[1]
        if desc[0] == "OK":
            msg = desc[2]
            await ctx.channel.send(msg)
        else:
            await ctx.channel.send(desc[2])


def setup(bot):
    bot.add_cog(GemsCasino(bot))
    open("help/cogs.txt", "a").write("GemsCasino\n")
