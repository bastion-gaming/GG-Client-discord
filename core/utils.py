import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.utils import get

ServIDmoji = 634317171496976395

client = discord.Client()
VERSION = open("core/version.txt").read().replace("\n","")

class Utils(commands.Cog):

    def __init__(self,ctx):
        return(None)

    @commands.command(pass_context=True)
    async def version(self, ctx):
            """
            Permet d'avoir la version du bot.
            """
            msg = "Je suis en version : **" +str(VERSION)+"**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def site(self, ctx):
            """
            Permet d'avoir le site de bastion.
            """
            msg = "Le site est : **http://www.bastion-gaming.fr/**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
            """
            PONG.
            """
            msg = "**PONG**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def twitch(self, ctx):
            """
            Permet d'avoir le lien du twitch.
            """
            msg = "Notre chaine twitch :arrow_right: **https://www.twitch.tv/bastionlivetv/**."
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def github(self, ctx):
            """
            Permet d'avoir le lien du github.
            """
            msg = "Le github du Bot :arrow_right: **https://github.com/bastion-gaming/**."
            await ctx.channel.send(msg)

def setup(bot):
    bot.add_cog(Utils(bot))
    open("help/cogs.txt","a").write("Utils\n")