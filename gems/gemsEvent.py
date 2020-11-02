import discord
from gems import gemsFonctions as GF
from core import gestion as ge
import gg_lib as gg
from discord.ext import commands
from discord.ext.commands import bot


class GemsEvent(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def event(self, ctx):
        """Date of Events !"""
        ID = ctx.author.id
        ge.socket.send_string(gg.std_send_command("level", ID, ge.name_pl))
        recv = GF.msg_recv()
        # await message.channel.send(recv)
        lang = recv['lang']
        msg = discord.Embed(title = "Evénements", color= 13752280, description = "Date des Evénements !!")
        desc = "26 Octobre :arrow_right: 10 Novembre"
        desc += "\n{0}`{1}`".format(GF.build_idmoji("pumpkin"), GF.trad_objet(lang, "pumpkin"))
        desc += "\n{0}`{1}`".format(GF.build_idmoji("pumpkinpie"), GF.trad_objet(lang, "pumpkinpie"))
        msg.add_field(name="Halloween", value=desc, inline=False)

        desc = "21 Décembre :arrow_right: 14 Janvier"
        desc += "\n{0}`{1}`".format(GF.build_idmoji("cupcake"), GF.trad_objet(lang, "cupcake"))
        msg.add_field(name="Noël", value=desc, inline=False)
        await ctx.channel.send(embed = msg)


def setup(bot):
    bot.add_cog(GemsEvent(bot))
    open("help/cogs.txt", "a").write("GemsEvent\n")
