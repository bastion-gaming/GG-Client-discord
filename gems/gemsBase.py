import os
import discord
import random as r
import time as t
import datetime as dt
from core import gestion as ge
from gems import gemsFonctions as GF
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter
import json
import gg_lib as gg

PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")


class GemsBase(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def tuto(self, ctx):
        """Affiche le tutoriel !"""
        desc = "Le but du jeu est de gagner le plus de :gem:`gems` possible.\n\n"
        msg = discord.Embed(title = "Tutoriel Get Gems!", color= 13752280, description = desc)
        desc = "`{0}begin` | Permet de créer son compte joueur et d'obtenir son starter Kit!\n••••••••••••\n".format(PREFIX)
        desc += "`{0}bal` | Permet de voir son nombre de :gem:`gems`\n••••••••••••\n".format(PREFIX)
        desc += "`{0}buy` | Permet d'acheter les items vendu au marché\n••••••••••••\n".format(PREFIX)
        desc += "`{0}crime` | Permet d'effectuer des vols pour récupérer des :gem:`gem`\n••••••••••••\n".format(PREFIX)
        desc += "`{0}mine` | Permet de récolter des matériaux.\nTu aura besoin d'une <:gem_pickaxe:{1}>`pickaxe` pour miner\n••••••••••••\n".format(PREFIX, GF.get_idmoji("pickaxe"))
        desc += "`{0}fish` | Permet de pécher des poissons.\nTu aura besoin d'une <:gem_fishingrod:{1}>`fishingrod` pour miner\n••••••••••••\n".format(PREFIX, GF.get_idmoji("fishingrod"))
        desc += "`{0}sell` | Permet de vendre les matériaux, les poissons, etc contre des :gem:`gems`\n••••••••••••\n".format(PREFIX)
        desc += "`{0}forge` | Permet de créer des outils à partir des matériaux récoltés\n".format(PREFIX)
        msg.add_field(name="Pour cela tu as les commandes:", value=desc, inline=False)
        await ctx.channel.send(embed = msg)

    @commands.command(pass_context=True)
    async def begin(self, ctx):
        """Pour créer son compte joueur et obtenir son starter Kit!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("begin", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def bal(self, ctx, nom = None):
        """Êtes vous riche ou pauvre ?"""
        ID = ctx.author.id
        param = dict()
        if nom is None:
            nom = ctx.author.name
            param["ID"] = ID
        else:
            IDname = ge.nom_ID(nom)
            param["ID"] = IDname
            nom = ctx.guild.get_member(IDname)
            nom = nom.name
        ge.socket.send_string(gg.std_send_command("bal", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        if desc[0] == "OK":
            title = "Compte principal de {}".format(nom)
            msg = discord.Embed(title = title, color= 13752280, description = "")
            msg.add_field(name="**_Balance_**", value=desc[1], inline=False)

            msg.add_field(name=desc[2], value=desc[3], inline=False)
            await ctx.channel.send(embed = msg)
            # Message de réussite dans la console
            print("Gems >> Balance de {} affichée".format(nom))
            return
        else:
            await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def baltop(self, ctx, n = None, m = None):
        """**_{filtre}_ [nombre]** | Classement des joueurs (10 premiers par défaut)"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        try:
            if n == None:
                n = 10
            else:
                n = int(n)
            filtre = "spinelles"
        except:
            if m == None:
                filtre = n
                n = 10
            else:
                filtre = n
                n = int(m)
        filtre = filtre.lower()
        param["nb"] = n
        param["filtre"] = filtre
        ge.socket.send_string(gg.std_send_command("baltop", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if desc[0] == "OK":
            if filtre == "gems" or filtre == "gem" or filtre == "spinelles" or filtre == "spinelle":
                Titre = "Classement des Joueurs | :gem:`gems`"
                if filtre == "spinelles" or filtre == "spinelle":
                    Titre = "Classement des Joueurs | <:spinelle:{idmoji}>`spinelles`".format(idmoji=GF.get_idmoji("spinelle"))

                msg = discord.Embed(title = Titre, color= 13752280, description = desc[1])
                # Message de réussite dans la console
                print("Gems >> {} a afficher le classement des {} premiers joueurs | Filtre: {}".format(ctx.author.name, n, filtre))

            elif filtre == "guild" or filtre == "guilde":
                msg = discord.Embed(title = "Classement des Guildes", color= 13752280, description = desc[1])
                # Message de réussite dans la console
                print("Gems >> {} a afficher le classement des {} premières guildes".format(ctx.author.name, n))

            else:
                msg = discord.Embed(title = "Classement", color= 13752280, description = "Erreur! Commande incorrect")
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def buy(self, ctx, item, nb = 1):
        """**[item] [nombre]** | Permet d'acheter les items vendus au marché"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["nb"] = nb
        param["item"] = item

        ge.socket.send_string(gg.std_send_command("buy", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def sell(self, ctx, item, nb = 1):
        """**[item] [nombre]** | Permet de vendre vos items !"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["nb"] = nb
        param["item"] = item

        ge.socket.send_string(gg.std_send_command("sell", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def inv(self, ctx, fct = None):
        """**[nom de la poche]** | Permet de voir ce que vous avez dans le ventre !"""
        ID = ctx.author.id
        nom = ctx.author.name
        param = dict()
        param["ID"] = ID
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("inv", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if desc[0] == "OK":
            msg_titre = "Inventaire de {} | Poche principale".format(nom)
            msg = discord.Embed(title = msg_titre, color= 6466585, description = desc[1])
            if desc[2] != "None":
                msg.add_field(name="Outils", value=desc[2], inline=False)
            if desc[3] != "None":
                msg.add_field(name="Spéciaux", value=desc[3], inline=False)
            if desc[4] != "None":
                msg.add_field(name="Items", value=desc[4], inline=False)
            if desc[5] != "None":
                msg.add_field(name="Minerais", value=desc[5], inline=False)
            if desc[6] != "None":
                msg.add_field(name="Poissons", value=desc[6], inline=False)
            if desc[7] != "None":
                msg.add_field(name="Plantes", value=desc[7], inline=False)
            if desc[8] != "None":
                msg.add_field(name="Événement", value=desc[8], inline=False)
            if desc[9] != "None":
                msg.add_field(name="Loot Box", value=desc[9], inline=False)
            await ctx.channel.send(embed = msg)

        elif desc[0] == "pockets":
            msg = discord.Embed(title = "Liste des poches de l'inventaire".format(nom), color= 6466585, description = desc[1])
            await ctx.channel.send(embed = msg)

        else:
            await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def market(self, ctx, fct = None):
        """**[stand]** | Permet de voir tout les objets que l'on peux acheter ou vendre !"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("market", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if desc[0] == "OK":
            if fct != None:
                msg = discord.Embed(title = "Le marché | {name}".format(name=fct), color= 2461129, description = desc[1])
            else:
                msg = discord.Embed(title = "Le marché", color= 2461129, description = desc[1])
            if fct == "mobile":
                msg.add_field(name="Outils", value=desc[2], inline=False)
                msg.add_field(name="Spéciaux", value=desc[3], inline=False)
                msg.add_field(name="Minerais", value=desc[4], inline=False)
                msg.add_field(name="Poissons", value=desc[5], inline=False)
                msg.add_field(name="Plantes", value=desc[6], inline=False)
                if desc[7] != "None":
                    msg.add_field(name="Items", value=desc[7], inline=False)
                if desc[8] != "None":
                    msg.add_field(name="Événement", value=desc[8], inline=False)
                if desc[9] != "None":
                    msg.add_field(name="Spinelles <:spinelle:{}>".format(GF.get_idmoji("spinelle")), value=desc[9], inline=False)

                msg.add_field(name="Loot Box", value=desc[10], inline=False)
                await ctx.channel.send(embed = msg)

            else:
                if fct == None or fct == "outil" or fct == "outils":
                    msg.add_field(name="Outils", value=desc[3], inline=True)
                    msg.add_field(name="Vente | Achat", value=desc[4], inline=True)
                    msg.add_field(name="Infos", value=desc[5], inline=True)

                if fct == None or fct == "outils" or fct == "outil" or fct == "item" or fct == "items" or fct == "minerai" or fct == "minerais" or fct == "poissons" or fct == "fish" or fct == "plantes" or fct == "plants" or fct == "event" or fct == "événements":
                    if desc[6] != "None":
                        msg.add_field(name="Spéciaux", value=desc[6], inline=True)
                        msg.add_field(name="Vente | Achat", value=desc[7], inline=True)
                        msg.add_field(name="Infos", value=desc[8], inline=True)

                if fct == None or fct == "minerai" or fct == "minerais":
                    msg.add_field(name="Minerais", value=desc[9], inline=True)
                    msg.add_field(name="Vente | Achat", value=desc[10], inline=True)
                    msg.add_field(name="Infos", value=desc[11], inline=True)

                if fct == None or fct == "fish" or fct == "poissons":
                    msg.add_field(name="Poissons", value=desc[12], inline=True)
                    msg.add_field(name="Vente | Achat", value=desc[13], inline=True)
                    msg.add_field(name="Infos", value=desc[14], inline=True)

                if fct == None or fct == "plants" or fct == "plantes":
                    msg.add_field(name="Plantes", value=desc[15], inline=True)
                    msg.add_field(name="Vente | Achat", value=desc[16], inline=True)
                    msg.add_field(name="Infos", value=desc[17], inline=True)

                if fct == None or fct == "item" or fct == "items":
                    msg.add_field(name="Items", value=desc[18], inline=True)
                    msg.add_field(name="Vente | Achat", value=desc[19], inline=True)
                    msg.add_field(name="Infos", value=desc[20], inline=True)

                if fct == None or fct == "event" or fct == "événements":
                    msg.add_field(name="Événements", value=desc[21], inline=True)
                    msg.add_field(name="Vente | Achat", value=desc[22], inline=True)
                    msg.add_field(name="Infos", value=desc[23], inline=True)

                if fct == None or fct == "lootbox":
                    msg.add_field(name="Loot Box", value=desc[24], inline=True)
                    msg.add_field(name="Achat", value=desc[25], inline=True)
                    msg.add_field(name="Gain", value=desc[26], inline=True)
                await ctx.channel.send(embed = msg)

        else:
            await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def pay(self, ctx, nom, gain):
        """**[nom] [gain]** | Donner de l'argent à vos amis !"""
        ID = ctx.author.id
        param = dict()
        param["platform"] = "discord"
        param["ID"] = ID
        param["nom"] = ctx.author.name
        param["ID_recu"] = ge.nom_ID(nom)
        param["Nom_recu"] = ctx.guild.get_member(param["ID_recu"]).name
        param["gain"] = gain

        ge.socket.send_string(gg.std_send_command("pay", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        await ctx.channel.send(desc[1])

    # @commands.command(pass_context=True)
    # async def give(self, ctx, nom, item, nb = None):
    #     """**[nom] [item] [nombre]** | Donner des items à vos amis !"""
    #     ID = ctx.author.id
    #     name = ctx.author.name
    #     checkLB = False
    #     if item == "bank_upgrade":
    #         await ctx.channel.send("Tu ne peux pas donner cette item!")
    #         return False
    #     if sql.spam(ID,GF.couldown_4s, "give", "gems"):
    #         try:
    #             if nb == None:
    #                 nb = 1
    #             else:
    #                 nb = int(nb)
    #             if nb < 0 and nb != -1:
    #                 sql.addGems(ID, -100)
    #                 msg = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
    #                 slq.add(ID, "DiscordCop Amende", 1, "statgems")
    #                 await ctx.channel.send(msg)
    #                 return "anticheat"
    #             elif nb > 0:
    #                 ID_recu = sql.nom_ID(nom)
    #                 Nom_recu = ctx.guild.get_member(ID_recu).name
    #                 for lootbox in GF.objetBox:
    #                     if item == lootbox.nom:
    #                         checkLB = True
    #                         itemLB = lootbox.nom
    #                         item = "lootbox_{}".format(lootbox.nom)
    #                 nbItem = int(sql.valueAtNumber(ID, item, "inventory"))
    #                 if nbItem >= nb and nb > 0:
    #                     if GF.testInvTaille(ID_recu):
    #                         sql.add(ID, item, -nb, "inventory")
    #                         sql.add(ID_recu, item, nb, "inventory")
    #                         if checkLB:
    #                             msg = "{0} donne {1} <:gem_lootbox:{3}>`{2}` à {4} !".format(name,nb,itemLB,GF.get_idmoji(itemLB),Nom_recu)
    #                         else:
    #                             for c in GF.objetItem:
    #                                 if c.nom == item:
    #                                     if c.type == "emoji":
    #                                         msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
    #                                     else:
    #                                         msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,GF.get_idmoji(item),Nom_recu)
    #                             for c in GF.objetOutil:
    #                                 if c.nom == item:
    #                                     if c.type == "emoji":
    #                                         msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
    #                                     else:
    #                                         msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,GF.get_idmoji(item),Nom_recu)
    #                         # Message de réussite dans la console
    #                         print("Gems >> {0} a donné {1} {2} à {3}".format(name, nb, item, Nom_recu))
    #                     else:
    #                         msg = "L'inventaire de {} est plein".format(Nom_recu)
    #                 else:
    #                     msg = "{0} n'a pas assez pour donner à {1} !".format(name, Nom_recu)
    #
    #             elif nb == -1:
    #                 ID_recu = sql.nom_ID(nom)
    #                 Nom_recu = ctx.guild.get_member(ID_recu).name
    #                 nbItem = int(sql.valueAtNumber(ID, item, "inventory"))
    #                 if nb > 0:
    #                     if GF.testInvTaille(ID_recu):
    #                         sql.add(ID, item, -nb, "inventory")
    #                         sql.add(ID_recu, item, nb, "inventory")
    #                         for c in GF.objetItem:
    #                             if c.nom == item:
    #                                 if c.type == "emoji":
    #                                     msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
    #                                 else:
    #                                     msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,GF.get_idmoji(item),Nom_recu)
    #                         for c in GF.objetOutil:
    #                             if c.nom == item:
    #                                 if c.type == "emoji":
    #                                     msg = "{0} donne {1} :{2}:`{2}` à {3} !".format(name, nb, item, Nom_recu)
    #                                 else:
    #                                     msg = "{0} donne {1} <:gem_{2}:{3}>`{2}` à {4} !".format(name,nb,item,GF.get_idmoji(item),Nom_recu)
    #                         # Message de réussite dans la console
    #                         print("Gems >> {0} a donné {1} {2} à {3}".format(name, nb, item, Nom_recu))
    #                     else:
    #                         msg = "L'inventaire de {} est plein".format(Nom_recu)
    #                 else:
    #                     msg = "{0} n'a pas assez pour donner à {1} !".format(name, Nom_recu)
    #
    #             else :
    #                 msg = "Tu ne peux pas donner une somme négative ! N'importe quoi enfin !"
    #             sql.updateComTime(ID, "give", "gems")
    #         except ValueError:
    #             msg = "La commande est mal formulée"
    #             pass
    #     else:
    #         msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
    #     await ctx.channel.send(msg)
    #
    #
    #
    # @commands.command(pass_context=True)
    # async def forge(self, ctx, item = None, nb = 1):
    #     """**[item] [nombre]** | Permet de concevoir des items spécifiques"""
    #     ID = ctx.author.id
    #     if sql.spam(ID,GF.couldown_4s, "forge", "gems"):
    #         if GF.testInvTaille(ID):
    #             #-------------------------------------
    #             # Affichage des recettes disponible
    #             if item == None:
    #                 msg = GF.recette(ctx)
    #                 await ctx.channel.send(embed = msg)
    #                 # Message de réussite dans la console
    #                 print("Gems >> {} a afficher les recettes".format(ctx.author.name))
    #                 return
    #             #-------------------------------------
    #             else:
    #                 for c in GF.objetRecette:
    #                     if item == c.nom:
    #                         nb = int(nb)
    #                         nb1 = nb*c.nb1
    #                         nb2 = nb*c.nb2
    #                         nb3 = nb*c.nb3
    #                         nb4 = nb*c.nb4
    #                         if c.item1 != "" and c.item2 != "" and c.item3 != "" and c.item4 != "":
    #                             if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(ID, c.item2, "inventory") >= nb2 and sql.valueAtNumber(ID, c.item3, "inventory") >= nb3 and sql.valueAtNumber(ID, c.item4, "inventory") >= nb4:
    #                                 sql.add(ID, c.nom, nb, "inventory")
    #                                 sql.add(ID, c.item1, -1*nb1, "inventory")
    #                                 sql.add(ID, c.item2, -1*nb2, "inventory")
    #                                 sql.add(ID, c.item3, -1*nb3, "inventory")
    #                                 sql.add(ID, c.item4, -1*nb4, "inventory")
    #                                 msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
    #                                 print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
    #                                 Durability = sql.valueAtNumber(ID, c.nom, "durability")
    #                                 if Durability == 0:
    #                                     for x in GF.objetOutil:
    #                                         if x.nom == c.nom:
    #                                             sql.add(ID, x.nom, x.durabilite, "durability")
    #                             else:
    #                                 msg = ""
    #                                 if sql.valueAtNumber(ID, c.item1, "inventory") < nb1:
    #                                     nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
    #                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item1, GF.get_idmoji(c.item1))
    #                                 if sql.valueAtNumber(ID, c.item2, "inventory") < nb2:
    #                                     nbmissing = (sql.valueAtNumber(ID, c.item2, "inventory") - nb2)*-1
    #                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item2, GF.get_idmoji(c.item2))
    #                                 if sql.valueAtNumber(ID, c.item3, "inventory") < nb3:
    #                                     nbmissing = (sql.valueAtNumber(ID, c.item3, "inventory") - nb3)*-1
    #                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item3, GF.get_idmoji(c.item3))
    #                                 if sql.valueAtNumber(ID, c.item4, "inventory") < nb4:
    #                                     nbmissing = (sql.valueAtNumber(ID, c.item4, "inventory") - nb4)*-1
    #                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item4, GF.get_idmoji(c.item4))
    #
    #                         elif c.item1 != "" and c.item2 != "" and c.item3 != "":
    #                             if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(ID, c.item2, "inventory") >= nb2 and sql.valueAtNumber(ID, c.item3, "inventory") >= nb3:
    #                                 sql.add(ID, c.nom, nb, "inventory")
    #                                 sql.add(ID, c.item1, -1*nb1, "inventory")
    #                                 sql.add(ID, c.item2, -1*nb2, "inventory")
    #                                 sql.add(ID, c.item3, -1*nb3, "inventory")
    #                                 msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
    #                                 print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
    #                                 Durability = sql.valueAtNumber(ID, c.nom, "durability")
    #                                 if Durability == 0:
    #                                     for x in GF.objetOutil:
    #                                         if x.nom == c.nom:
    #                                             sql.add(ID, x.nom, x.durabilite, "durability")
    #                             else:
    #                                 msg = ""
    #                                 if sql.valueAtNumber(ID, c.item1, "inventory") < nb1:
    #                                     nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
    #                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item1, GF.get_idmoji(c.item1))
    #                                 if sql.valueAtNumber(ID, c.item2, "inventory") < nb2:
    #                                     nbmissing = (sql.valueAtNumber(ID, c.item2, "inventory") - nb2)*-1
    #                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item2, GF.get_idmoji(c.item2))
    #                                 if sql.valueAtNumber(ID, c.item3, "inventory") < nb3:
    #                                     nbmissing = (sql.valueAtNumber(ID, c.item3, "inventory") - nb3)*-1
    #                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item3, GF.get_idmoji(c.item3))
    #
    #                         elif c.item1 != "" and c.item2 != "":
    #                             if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1 and sql.valueAtNumber(ID, c.item2, "inventory") >= nb2:
    #                                 sql.add(ID, c.nom, nb, "inventory")
    #                                 sql.add(ID, c.item1, -1*nb1, "inventory")
    #                                 sql.add(ID, c.item2, -1*nb2, "inventory")
    #                                 msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
    #                                 print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
    #                                 Durability = sql.valueAtNumber(ID, c.nom, "durability")
    #                                 if Durability == 0:
    #                                     for x in GF.objetOutil:
    #                                         if x.nom == c.nom:
    #                                             sql.add(ID, x.nom, x.durabilite, "durability")
    #                             else:
    #                                 msg = ""
    #                                 if sql.valueAtNumber(ID, c.item1, "inventory") < nb1:
    #                                     nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
    #                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item1, GF.get_idmoji(c.item1))
    #                                 if sql.valueAtNumber(ID, c.item2, "inventory") < nb2:
    #                                     nbmissing = (sql.valueAtNumber(ID, c.item2, "inventory") - nb2)*-1
    #                                     msg += "Il te manque {0} <:gem_{1}:{2}>`{1}`\n".format(nbmissing, c.item2, GF.get_idmoji(c.item2))
    #
    #                         elif c.item1 != "":
    #                             if sql.valueAtNumber(ID, c.item1, "inventory") >= nb1:
    #                                 sql.add(ID, c.nom, nb, "inventory")
    #                                 sql.add(ID, c.item1, -1*nb1, "inventory")
    #                                 msg = "Bravo, tu as réussi à forger {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, GF.get_idmoji(c.nom))
    #                                 print("Gems >> {0} a forgé {1} {2}".format(ctx.author.name, nb, c.nom))
    #                                 Durability = sql.valueAtNumber(ID, c.nom, "durability")
    #                                 if Durability == 0:
    #                                     for x in GF.objetOutil:
    #                                         if x.nom == c.nom:
    #                                             sql.add(ID, x.nom, x.durabilite, "durability")
    #                             else:
    #                                 nbmissing = (sql.valueAtNumber(ID, c.item1, "inventory") - nb1)*-1
    #                                 msg = "Il te manque {0} <:gem_{1}:{2}>`{1}`".format(nbmissing, c.item1, GF.get_idmoji(c.item1))
    #                         await ctx.channel.send(msg)
    #                         return True
    #                     else:
    #                         msg = "Aucun recette disponible pour forger cette item !"
    #             sql.updateComTime(ID, "forge", "gems")
    #         else:
    #             msg = "Ton inventaire est plein"
    #     else:
    #         msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
    #     await ctx.channel.send(msg)
    #
    #
    #
    # @commands.command(pass_context=True)
    # async def trophy(self, ctx, nom = None):
    #     """**[nom]** | Liste de vos trophées !"""
    #     ID = ctx.author.id
    #     if sql.spam(ID,GF.couldown_4s, "trophy", "gems"):
    #         if nom != None:
    #             ID = sql.nom_ID(nom)
    #             nom = ctx.guild.get_member(ID)
    #             nom = nom.name
    #         else:
    #             nom = ctx.author.name
    #         d_trophy = ":trophy:Trophées de {}\n\n".format(nom)
    #         #-------------------------------------
    #         # Récupération de la liste des trophées de ID
    #         # et attribution de nouveau trophée si les conditions sont rempli
    #         trophy = sql.valueAt(ID, "all", "trophy")
    #         for c in GF.objetTrophy:
    #             GF.testTrophy(ID, c.nom)
    #
    #         #-------------------------------------
    #         # Affichage des trophées possédés par ID
    #         for c in GF.objetTrophy:
    #             for x in trophy:
    #                 if c.nom == str(x[1]):
    #                     if int(x[0]) > 0:
    #                         d_trophy += "•**{}**\n".format(c.nom)
    #
    #         sql.updateComTime(ID, "trophy", "gems")
    #         msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
    #         # Message de réussite dans la console
    #         print("Gems >> {} a affiché les trophées de {}".format(ctx.author.name,nom))
    #         await ctx.channel.send(embed = msg)
    #     else:
    #         msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
    #         await ctx.channel.send(msg)
    #
    #
    #
    # @commands.command(pass_context=True)
    # async def trophylist(self, ctx):
    #     """Liste de tout les trophées disponibles !"""
    #     ID = ctx.author.id
    #     d_trophy = "Liste des :trophy:Trophées\n\n"
    #     if sql.spam(ID,GF.couldown_6s, "trophylist", "gems"):
    #         #-------------------------------------
    #         # Affichage des trophées standard
    #         for c in GF.objetTrophy:
    #             if c.type != "unique" and c.type != "special":
    #                 d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
    #         d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
    #         #-------------------------------------
    #         # Affichage des trophées spéciaux
    #         for c in GF.objetTrophy:
    #             if c.type != "unique" and c.type == "special":
    #                 d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
    #         d_trophy += "▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
    #         #-------------------------------------
    #         # Affichage des trophées uniques
    #         for c in GF.objetTrophy:
    #             if c.type == "unique" and c.type != "special":
    #                 d_trophy += "**{}**: {}\n".format(c.nom, c.desc)
    #
    #         sql.updateComTime(ID, "trophylist", "gems")
    #         msg = discord.Embed(title = "Trophées",color= 6824352, description = d_trophy)
    #         # Message de réussite dans la console
    #         print("Gems >> {} a affiché la liste des trophées".format(ctx.author.name))
    #         await ctx.channel.send(embed = msg)
    #     else:
    #         msg = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
    #         await ctx.channel.send(msg)
    #
    #
    #
    # @commands.command(pass_context=True)
    # async def graphbourse(self, ctx, item, mois = None, annee = None, type = None):
    #     """**[item] [mois] [année]** | Historique de la bourse par item"""
    #     ID = ctx.author.id
    #     now = dt.datetime.now()
    #
    #     if item.lower() == "all":
    #         if type == None:
    #             type = str(now.month)
    #         if annee == None:
    #             annee = str(now.year)
    #         temp = type
    #         type = mois.lower()
    #         mois = temp
    #         if type == "item" or type == "items":
    #             for c in GF.objetItem:
    #                 check = False
    #                 for x in GI.exception:
    #                     if x == c.nom:
    #                         check = True
    #                 for x in GF.ObjetEventEnd:
    #                     if x == c.nom:
    #                         check = True
    #                 if not check:
    #                     graph = GS.create_graph(c.nom, annee, mois)
    #                     if graph == "404":
    #                         await ctx.send("Aucune données n'a été trouvée!")
    #                     else:
    #                         await ctx.send(file=discord.File("cache/{}".format(graph)))
    #                         os.remove("cache/{}".format(graph))
    #         elif type == "outil" or type == "outils":
    #             for c in GF.objetOutil:
    #                 check = False
    #                 for x in GI.exception:
    #                     if x == c.nom:
    #                         check = True
    #                 if c.type != "bank" and check == False:
    #                     graph = GS.create_graph(c.nom, annee, mois)
    #                     if graph == "404":
    #                         await ctx.send("Aucune données n'a été trouvée!")
    #                     else:
    #                         await ctx.send(file=discord.File("cache/{}".format(graph)))
    #                         os.remove("cache/{}".format(graph))
    #         else:
    #             await ctx.send("Commande mal formulée")
    #     else:
    #         if mois == None:
    #             mois = str(now.month)
    #         if annee == None:
    #             annee = str(now.year)
    #         graph = GS.create_graph(item, annee, mois)
    #         if graph == "404":
    #             await ctx.send("Aucune données n'a été trouvée!")
    #         else:
    #             await ctx.send(file=discord.File("cache/{}".format(graph)))
    #             os.remove("cache/{}".format(graph))


def setup(bot):
    bot.add_cog(GemsBase(bot))
    open("help/cogs.txt","a").write("GemsBase\n")
