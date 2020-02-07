import discord
from core import gestion as ge
from gems import gemsFonctions as GF, gemsStats as GS
from discord.ext import commands
from discord.ext.commands import bot
import gg_lib as gg
import os
import datetime as dt
from languages import lang as lang_P

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
        param["fct"] = "None"
        if nom is None:
            nom = ctx.author.name
            param["ID"] = ID
        elif nom == "info":
            nom = ctx.author.name
            param["ID"] = ID
            param["fct"] = "info"
        else:
            IDname = ge.nom_ID(nom)
            param["ID"] = IDname
            nom = ctx.guild.get_member(IDname)
            nom = nom.name
        ge.socket.send_string(gg.std_send_command("bal", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        if desc[0] == "OK":
            lang = desc[1]
            title = lang_P.forge_msg(lang, "bal", [nom], False)
            msg = discord.Embed(title = title, color= 13752280, description = desc[2])
            msg.add_field(name="**_Balance_**", value=desc[3], inline=False)

            msg.add_field(name=desc[4], value=desc[5], inline=False)
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
            filtre = "gems"
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
            lang = desc[1]
            if filtre == "gems" or filtre == "gem" or filtre == "spinelles" or filtre == "spinelle":
                Titre = lang_P.forge_msg(lang, "baltop", None, False, 0)
                if filtre == "spinelles" or filtre == "spinelle":
                    Titre = lang_P.forge_msg(lang, "baltop", [GF.get_idmoji("spinelle")], False, 1)

                msg = discord.Embed(title = Titre, color= 13752280, description = desc[2])
                # Message de réussite dans la console
                print("Gems >> {} a afficher le classement des {} premiers joueurs | Filtre: {}".format(ctx.author.name, n, filtre))

            elif filtre == "guild" or filtre == "guilde":
                Titre = lang_P.forge_msg(lang, "baltop", None, False, 2)
                msg = discord.Embed(title = Titre, color= 13752280, description = desc[2])
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
        param["IDGuild"] = ctx.guild.id
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
        param["IDGuild"] = ctx.guild.id
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
        param["IDGuild"] = ctx.guild.id
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("inv", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if desc[0] == "OK":
            lang = desc[1]
            msg_titre = lang_P.forge_msg(lang, "inv", [nom], False, 0)
            msg = discord.Embed(title = msg_titre, color= 6466585, description = desc[2])
            if desc[2] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc[3], inline=False)
            if desc[3] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc[4], inline=False)
            if desc[4] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc[5], inline=False)
            if desc[5] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc[6], inline=False)
            if desc[6] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc[7], inline=False)
            if desc[7] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc[8], inline=False)
            if desc[8] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc[9], inline=False)
            if desc[9] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=desc[10], inline=False)
            await ctx.channel.send(embed = msg)

        elif desc[0] == "pockets":
            lang = desc[1]
            msg = discord.Embed(title = lang_P.forge_msg(lang, "inv", None, False, 1), color= 6466585, description = desc[2])
            await ctx.channel.send(embed = msg)

        else:
            await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def market(self, ctx, fct = None):
        """**[stand]** | Permet de voir tout les objets que l'on peux acheter ou vendre !"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("market", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if desc[0] == "OK":
            lang = desc[1]
            if fct != None:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "market", [fct], False, 1), color= 2461129, description = desc[2])
            else:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "market", None, False, 0), color= 2461129, description = desc[2])
            if fct == "mobile":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc[3], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc[4], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc[5], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc[6], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc[7], inline=False)
                if desc[7] != "None":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc[8], inline=False)
                if desc[8] != "None":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc[9], inline=False)
                if desc[9] != "None":
                    msg.add_field(name="Spinelles <:spinelle:{}>".format(GF.get_idmoji("spinelle")), value=desc[10], inline=False)

                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=desc[11], inline=False)
                await ctx.channel.send(embed = msg)

            else:
                if fct == None or fct == "outil" or fct == "outils":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc[4], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[5], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[6], inline=True)

                if fct == None or fct == "outils" or fct == "outil" or fct == "item" or fct == "items" or fct == "minerai" or fct == "minerais" or fct == "poissons" or fct == "fish" or fct == "plantes" or fct == "plants" or fct == "event" or fct == "événements":
                    if desc[6] != "None":
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc[7], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[8], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[9], inline=True)

                if fct == None or fct == "minerai" or fct == "minerais":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc[10], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[11], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[12], inline=True)

                if fct == None or fct == "fish" or fct == "poissons":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc[13], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[14], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[15], inline=True)

                if fct == None or fct == "plants" or fct == "plantes":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc[16], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[17], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[18], inline=True)

                if fct == None or fct == "item" or fct == "items":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc[19], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[20], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[21], inline=True)

                if fct == None or fct == "event" or fct == "événements":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc[22], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc[23], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc[24], inline=True)

                if fct == None or fct == "lootbox":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=desc[25], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 3), value=desc[26], inline=True)
                    msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc[27], inline=True)
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
        param["IDGuild"] = ctx.guild.id
        param["nom"] = ctx.author.name
        param["ID_recu"] = ge.nom_ID(nom)
        param["Nom_recu"] = ctx.guild.get_member(param["ID_recu"]).name
        param["gain"] = gain

        ge.socket.send_string(gg.std_send_command("pay", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def give(self, ctx, nom, item, nb = None):
        """**[nom] [item] [nombre]** | Donner des items à vos amis !"""
        ID = ctx.author.id
        param = dict()
        param["platform"] = "discord"
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["nom"] = ctx.author.name
        param["ID_recu"] = ge.nom_ID(nom)
        param["Nom_recu"] = ctx.guild.get_member(param["ID_recu"]).name
        param["item"] = item
        param["nb"] = nb

        ge.socket.send_string(gg.std_send_command("give", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def forge(self, ctx, item = None, nb = 1):
        """**[item] [nombre]** | Permet de concevoir des items spécifiques"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["IDGuild"] = ctx.guild.id
        param["item"] = item
        param["nb"] = nb

        ge.socket.send_string(gg.std_send_command("forge", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        if item == None:
            lang = desc[1]
            msg = discord.Embed(title = lang_P.forge_msg(lang, "recette"), color= 15778560, description = desc[2])
            await ctx.channel.send(embed = msg)
            return True
        else:
            await ctx.channel.send(desc[1])

    @commands.command(pass_context=True)
    async def graphbourse(self, ctx, item, mois = None, annee = None, type = None):
        """**[item] [mois] [année]** | Historique de la bourse par item"""
        ID = ctx.author.id
        now = dt.datetime.now()

        if item.lower() == "all":
            if type == None:
                type = str(now.month)
            if annee == None:
                annee = str(now.year)
            temp = type
            type = mois.lower()
            mois = annee
            annee = temp
            param = dict()
            param["ID"] = ID
            param["type"] = type

            ge.socket.send_string(gg.std_send_command("listobjet", ID, ge.name_pl, param))
            msg = GF.msg_recv()

            if msg[0] == "NOK":
                await ctx.channel.send(msg[1])
            else:
                for one in msg[2]:
                    graph = GS.create_graph(ctx, one, annee, mois)
                    lang = graph[1]
                    if graph[0] == "404":
                        await ctx.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
                    else:
                        await ctx.send(file=discord.File("cache/{}".format(graph)))
                        os.remove("cache/{}".format(graph))
        else:
            if mois == None:
                mois = str(now.month)
            if annee == None:
                annee = str(now.year)
            graph = GS.create_graph(ctx, item, annee, mois)
            lang = graph[1]
            if graph[0] == "404":
                await ctx.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
            else:
                await ctx.send(file=discord.File("cache/{}".format(graph[0])))
                os.remove("cache/{}".format(graph[0]))

    @commands.command(pass_context=True)
    async def lang(self, ctx, langue):
        """
        Permet de changer la langue pour un joueur.
        """
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["langue"] = langue

        ge.socket.send_string(gg.std_send_command("lang", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        await ctx.channel.send(desc[1])

    # ==============================
    # ===== Commande désactivé =====
    # ==============================
    # @commands.command(pass_context=True)
    # async def convert(self, ctx, nb = None):
    #     """**[Nombre de spinelle]** | Convertisseur :gem:`gems` :left_right_arrow: `spinelles` (250 000 pour 1)"""
    #     ID = ctx.author.id
    #     param = dict()
    #     param["ID"] = ID
    #     param["IDGuild"] = ctx.guild.id
    #     param["nb"] = nb
    #
    #     ge.socket.send_string(gg.std_send_command("convert", ID, ge.name_pl, param))
    #     desc = GF.msg_recv()
    #
    #     await ctx.channel.send(desc[1])

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


def setup(bot):
    bot.add_cog(GemsBase(bot))
    open("help/cogs.txt","a").write("GemsBase\n")
