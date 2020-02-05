import discord
from discord.ext import commands
from discord.ext.commands import bot
from gems import gemsFonctions as GF
from core import gestion as ge
import gg_lib as gg


class GemsPlay(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def daily(self, ctx):
        """Récupère ta récompense journalière!"""
        # =======================================================================
        # Initialisation des variables générales de la fonction
        # =======================================================================
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        ge.socket.send_string(gg.std_send_command("daily", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def bank(self, ctx, ARG = None, ARG2 = None):
        """Compte épargne"""
        # =======================================================================
        # Initialistation des variables générales de la fonction
        # =======================================================================
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["ARG"] = ARG
        param["ARG2"] = ARG2

        ge.socket.send_string(gg.std_send_command("bank", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if desc[0] == "bal":
            if ARG2 != None:
                ID = ge.nom_ID(ARG2)
                nom = ctx.guild.get_member(ID)
                ARG2 = nom.name
                title = "Compte épargne de {}".format(ARG2)
            else:
                title = "Compte épargne de {}".format(ctx.author.name)
            msg = discord.Embed(title = title, color= 13752280, description = "")
            msg.add_field(name="Balance", value=desc[1], inline=False)
            msg.add_field(name="Commandes", value=desc[2], inline=False)
            await ctx.channel.send(embed = msg)

        else:
            await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def stealing(self, ctx, name=None):
        """**[nom]** | Vole des :gem:`gems` aux autres joueurs!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["name"] = name
        ge.socket.send_string(gg.std_send_command("stealing", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def crime(self, ctx):
        """Commets un crime et gagne des :gem:`gems` Attention au DiscordCop!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        ge.socket.send_string(gg.std_send_command("crime", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def gamble(self, ctx, valeur):
        """**[valeur]** | Avez vous l'ame d'un parieur ?"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["valeur"] = valeur
        ge.socket.send_string(gg.std_send_command("gamble", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def mine(self, ctx):
        """Minez compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        ge.socket.send_string(gg.std_send_command("mine", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def dig(self, ctx):
        """Creusons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        ge.socket.send_string(gg.std_send_command("dig", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def fish(self, ctx):
        """Péchons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        ge.socket.send_string(gg.std_send_command("fish", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def slots(self, ctx, imise = None):
        """**[mise]** | La machine à sous, la mise minimum est de 10 :gem:`gems`"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["imise"] = imise
        ge.socket.send_string(gg.std_send_command("slots", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def boxes(self, ctx, fct = None, name = None):
        """**open [nom]** | Ouverture de Loot Box"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["fct"] = fct
        param["name"] = name
        ge.socket.send_string(gg.std_send_command("boxes", ID, ge.name_pl, param))
        msg = GF.msg_recv()

        if msg[0] == "OK":
            titre = msg[2]
            desc = msg[1]
            MsgEmbed = discord.Embed(title = "Loot Box | {}".format(titre), color= 13752280, description = desc)
            await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def hothouse(self, ctx, fct = None, arg = None, arg2 = None):
        """**[harvest / plant]** {_n° plantation / item à planter_} | Plantons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["fct"] = fct
        param["arg"] = arg
        param["arg2"] = arg2
        ge.socket.send_string(gg.std_send_command("hothouse", ID, ge.name_pl, param))
        msg = GF.msg_recv()

        if msg[0] == "OK":
            nbplanting = msg[1]
            desc = "Voici tes plantations.\nUtilise `hothouse plant seed` pour planter une <:gem_seed:{0}>`seed`".format(GF.get_idmoji("seed"))
            MsgEmbed = discord.Embed(title = "La serre", color= 6466585, description = desc)
            k = len(msg)
            i = 2
            while i < k:
                j = (i-2)/2
                if j % 10 == 0 and j != nbplanting and j != 0:
                    if j // 10 == 1:
                        await ctx.channel.send(embed = MsgEmbed)
                    else:
                        await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
                    MsgEmbed = discord.Embed(title = "La serre | Partie {}".format(int((j//10)+1)), color= 6466585, description = "Voici tes plantation.")
                    MsgEmbed.add_field(name="Plantation n°{}".format(msg[i]), value=msg[i+1], inline=False)
                else:
                    MsgEmbed.add_field(name="Plantation n°{}".format(msg[i]), value=msg[i+1], inline=False)
                i += 2
            await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def ferment(self, ctx, item = None):
        """**{grapes/wheat}** | Cave de fermentation. Alcool illimité !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["item"] = item
        ge.socket.send_string(gg.std_send_command("ferment", ID, ge.name_pl, param))
        msg = GF.msg_recv()

        if msg[0] == "OK":
            nbplanting = msg[1]
            desc = "Voici tes barrils.\nUtilise `ferment grapes` pour obtenir des :wine_glass:`wine_glass`"
            MsgEmbed = discord.Embed(title = "La cave", color= 14902529, description = desc)
            k = len(msg)
            i = 2
            while i < k:
                j = (i-2)/2
                if j % 10 == 0 and j != nbplanting and j != 0:
                    if j // 10 == 1:
                        await ctx.channel.send(embed = MsgEmbed)
                    else:
                        await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
                    MsgEmbed = discord.Embed(title = "La cave | Partie {}".format(int((j//10)+1)), color= 14902529, description = "Voici vos barrils.")
                    MsgEmbed.add_field(name="Barril n°{}".format(msg[i]), value=msg[i+1], inline=False)
                else:
                    MsgEmbed.add_field(name="Barril n°{}".format(msg[i]), value=msg[i+1], inline=False)
                i += 2
            await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def cooking(self, ctx, item = None):
        """**{potato/pumpkin/chocolate}** | Cuisinons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["item"] = item
        ge.socket.send_string(gg.std_send_command("cooking", ID, ge.name_pl, param))
        msg = GF.msg_recv()

        if msg[0] == "OK":
            nbplanting = msg[1]
            desc = "Voici tes fours.\nUtilise `cooking potato` pour obtenir des <:gem_fries:{0}>`fries`".format(GF.get_idmoji("fries"))
            MsgEmbed = discord.Embed(title = "La Cuisine", color= 14902529, description = desc)
            k = len(msg)
            i = 2
            while i < k:
                j = (i-2)/2
                if j % 10 == 0 and j != nbplanting and j != 0:
                    if j // 10 == 1:
                        await ctx.channel.send(embed = MsgEmbed)
                    else:
                        await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
                    MsgEmbed = discord.Embed(title = "La Cuisine | Partie {}".format(int((j//10)+1)), color= 14902529, description = "Voici vos fours.")
                    MsgEmbed.add_field(name="Four n°{}".format(msg[i]), value=msg[i+1], inline=False)
                else:
                    MsgEmbed.add_field(name="Four n°{}".format(msg[i]), value=msg[i+1], inline=False)
                i += 2
            await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send(msg[1])


def setup(bot):
    bot.add_cog(GemsPlay(bot))
    open("help/cogs.txt", "a").write("GemsPlay\n")
