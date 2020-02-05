import discord
from gems import gemsFonctions as GF
from discord.ext import commands
from discord.ext.commands import bot


class GemsEvent(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def event(self, ctx):
        """Date des Événements !!"""
        msg = discord.Embed(title = "Evénements", color= 13752280, description = "Date des Evénements !!")
        desc = "26 Octobre :arrow_right: 10 Novembre"
        for one in GF.objetItem:
            if one.type == "halloween":
                desc += "\n<:gem_{0}:{1}>`{0}`".format(one.nom, GF.get_idmoji(one.nom))
        msg.add_field(name="Halloween", value=desc, inline=False)

        desc = "14 Décembre :arrow_right: 5 Janvier"
        for one in GF.objetItem:
            if one.type == "christmas":
                desc += "\n<:gem_{0}:{1}>`{0}`".format(one.nom, GF.get_idmoji(one.nom))
        desc += "\n:gift:`gift`"
        msg.add_field(name="Noël", value=desc, inline=False)

        # desc = "10 Février :arrow_right: 17 Février"
        # for one in GF.objetItem:
        #     if one.type == "saint valentin":
        #         desc += "\n<:gem_{0}:{1}>`{0}`".format(one.nom, GF.get_idmoji(one.nom))
        # desc += "\n:gift_heart:`gift_heart`"
        # msg.add_field(name="Saint Valentin", value=desc, inline=False)
        #
        # desc = "7 Juillet :arrow_right: 21 Juillet"
        # msg.add_field(name="Fête Nationale", value=desc, inline=False)
        await ctx.channel.send(embed = msg)


def setup(bot):
    bot.add_cog(GemsEvent(bot))
    open("help/cogs.txt", "a").write("GemsEvent\n")
