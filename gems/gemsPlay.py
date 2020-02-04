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
            desc = "Voici tes plantations.\nUtilisé `hothouse plant seed` pour planter une <:gem_seed:{0}>`seed`".format(GF.get_idmoji("seed"))
            MsgEmbed = discord.Embed(title = "La serre", color= 6466585, description = desc)
            k = len(msg)
            i = 2
            while i < k:
                j = (i-2)/2
                if j % 10 == 0 and j != nbplanting and j!= 0:
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
            desc = "Voici tes plantations.\nUtilisé `hothouse plant seed` pour planter une <:gem_seed:{0}>`seed`".format(GF.get_idmoji("seed"))
            MsgEmbed = discord.Embed(title = "La cave", color= 6466585, description = desc)
            k = len(msg)
            i = 2
            while i < k:
                j = (i-2)/2
                if j % 10 == 0 and j != nbplanting and j!= 0:
                    if j // 10 == 1:
                        await ctx.channel.send(embed = MsgEmbed)
                    else:
                        await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
                    MsgEmbed = discord.Embed(title = "La cave | Partie {}".format(int((j//10)+1)), color= 6466585, description = "Voici vos barrils.")
                    MsgEmbed.add_field(name="Barril n°{}".format(msg[i]), value=msg[i+1], inline=False)
                else:
                    MsgEmbed.add_field(name="Barril n°{}".format(msg[i]), value=msg[i+1], inline=False)
                i += 2
            await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send(msg[1])

    #
    #
    #
    # @commands.command(pass_context=True)
    # async def ferment(self, ctx, item = None):
    #     """**{grapes/wheat}** | Cave de fermentation. Alcool illimité !!"""
    #     ID = ctx.author.id
    #     jour = dt.date.today()
    #     gain = ""
    #     i = 1
    #     max = 20
    #     msg = discord.Embed(title = "La Cave | Partie {}".format((i//10)+1),color= 14902529, description = "Voici vos barrils.")
    #
    #     if sql.spam(ID,GF.couldown_4s, "ferment", "gems"):
    #         if item == "grapes":
    #             nbitem = 10
    #             gain = "wine_glass"
    #             couldown = GF.couldown_3h
    #             couldownMsg = "3h"
    #         elif item == "wheat":
    #             nbitem = 8
    #             gain = "beer"
    #             couldown = GF.couldown_8h
    #             couldownMsg = "8h"
    #         sql.updateComTime(ID, "ferment", "gems")
    #         nbferment = sql.valueAtNumber(ID, "barrel", "inventory") + 1
    #         if nbferment >= max:
    #             nbferment = max
    #         while i <= nbferment:
    #             data = []
    #             valueFerment = sql.valueAt(ID, i, "ferment")
    #             if valueFerment != 0:
    #                 valueTime = float(valueFerment[0])
    #                 valueItem = valueFerment[1]
    #             else:
    #                 valueTime = 0
    #                 valueItem = ""
    #             fermentItem = sql.valueAtNumber(ID, item, "inventory")
    #             if valueItem == "" and item == None:
    #                 desc = "Ce barril est vide."
    #             elif item == "grapes" or item == "wheat":
    #                 if valueTime == 0:
    #                     if fermentItem >= nbitem:
    #                         data = []
    #                         data.append(str(t.time()))
    #                         data.append(item)
    #                         sql.add(ID, i, data, "ferment")
    #                         sql.add(ID, item, -nbitem, "inventory")
    #                         if item == "grapes":
    #                             desc = "Ton barril a été rempli de :{0}:`{0}`. L'alcool aura fini de fermenter dans :clock2:`{1}`".format(item, couldownMsg)
    #                         else:
    #                             desc = "Ton barril a été rempli de <:gem_{0}:{1}>`{0}`. L'alcool aura fini de fermenter dans :clock2:`{2}`".format(item, GF.get_idmoji(item), couldownMsg)
    #                     else:
    #                         if item == "grapes":
    #                             desc = "Tu n'as pas assez de :{0}:`{0}` dans ton inventaire! \nIl te faut {2} :{0}:`{0}` pour faire des :{1}:`{1}`".format(item, gain, nbitem)
    #                         else:
    #                             desc = "Tu n'as pas assez de <:gem_{0}:{1}>`{0}` dans ton inventaire! \nIl te faut {3} <:gem_{0}:{1}>`{0}` pour faire des :{2}:`{2}`".format(item, GF.get_idmoji(item), gain, nbitem)
    #                         if i > 15:
    #                             await ctx.channel.send(embed = msg)
    #                             await ctx.channel.send(desc)
    #                             return 0
    #                 else:
    #                     if valueItem == "grapes":
    #                         desc = "Fermentation de :{0}:`{0}` en cours.".format(valueItem)
    #                     else:
    #                         desc = "Fermentation de <:gem_{0}:{1}>`{0}` en cours.".format(valueItem, GF.get_idmoji(valueItem))
    #             elif item == None:
    #                 if valueItem == "grapes":
    #                     gain = "wine_glass"
    #                     nbgain = r.randint(1,4)
    #                     couldown = GF.couldown_3h
    #                 elif valueItem == "wheat":
    #                     gain = "beer"
    #                     nbgain = r.randint(2,6)
    #                     couldown = GF.couldown_8h
    #                 CookedTime = float(valueTime)
    #                 InstantTime = t.time()
    #                 time = CookedTime - (InstantTime-couldown)
    #                 if time <= 0:
    #                     data = []
    #                     data.append(0)
    #                     data.append("")
    #                     sql.add(ID, gain, nbgain, "inventory")
    #                     sql.updateField(ID, i, data, "ferment")
    #                     desc = "Ton alcool à fini de fermenter, en ouvrant le barril tu gagnes {2} :{0}:`{0}`".format(gain, GF.get_idmoji(gain), nbgain)
    #                     lvl.addxp(ID, 1, "gems")
    #                     if i > 1:
    #                         nbbarrel = int(sql.valueAtNumber(ID, "barrel", "inventory"))
    #                         if nbbarrel > 0:
    #                             if sql.valueAtNumber(ID, "barrel", "durability") == 0:
    #                                 for c in GF.objetOutil:
    #                                     if c.nom == "barrel":
    #                                         sql.add(ID, "barrel", c.durabilite, "durability")
    #                             sql.add(ID, "barrel", -1, "durability")
    #                             if sql.valueAtNumber(ID, "barrel", "durability") <= 0:
    #                                 for c in GF.objetOutil:
    #                                     if c.nom == "barrel":
    #                                         sql.add(ID, "barrel", c.durabilite, "durability")
    #                                 sql.add(ID, "barrel", -1, "inventory")
    #                 else:
    #                     timeH = int(time / 60 / 60)
    #                     time = time - timeH * 3600
    #                     timeM = int(time / 60)
    #                     timeS = int(time - timeM * 60)
    #                     if valueItem == "grapes":
    #                         desc = "Fermentation de :{0}:`{0}` en cours.".format(valueItem)
    #                     else:
    #                         desc = "Fermentation de <:gem_{0}:{1}>`{0}` en cours.".format(valueItem, GF.get_idmoji(valueItem))
    #                     desc += "\nTon alcool aura fini de fermenter dans :clock2:`{}h {}m {}s`".format(timeH,timeM,timeS)
    #             if i % 10 == 0 and i != nbferment:
    #                 if i // 10 == 1:
    #                     await ctx.channel.send(embed = msg)
    #                 else:
    #                     await ctx.channel.send(embed = msg, delete_after = 90)
    #                 msg = discord.Embed(title = "La Cave | Partie {}".format((i//10)+1),color= 14902529, description = "Voici vos barrils.")
    #                 msg.add_field(name="Barril n°{}".format(i), value=desc, inline=False)
    #             else:
    #                 msg.add_field(name="Barril n°{}".format(i), value=desc, inline=False)
    #             i += 1
    #         if nbferment // 10 == 0:
    #             await ctx.channel.send(embed = msg)
    #         else:
    #             await ctx.channel.send(embed = msg, delete_after = 90)
    #     else:
    #         msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
    #         await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(GemsPlay(bot))
    open("help/cogs.txt","a").write("GemsPlay\n")
