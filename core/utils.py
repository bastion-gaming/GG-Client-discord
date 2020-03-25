import discord
from discord.ext import commands
from discord.ext.commands import bot

ServIDmoji = 634317171496976395
nb_saisons = 0
date_saison = ""
client = discord.Client()
VERSION = open("core/version.txt").read().replace("\n", "")


class Utils(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def version(self, ctx):
            """
            Allows to have the version of the bot.
            """
            msg = "**" + str(VERSION) + "**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def site(self, ctx):
            """
            Allows to have the bastion site.
            """
            msg = "**http://www.bastion-gaming.fr/**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
            """
            PONG.
            """
            msg = "**PONG**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def github(self, ctx):
            """
            Allows to have the link of the github.
            """
            msg = "**https://github.com/bastion-gaming/**."
            await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Utils(bot))
    open("help/cogs.txt", "a").write("Utils\n")
