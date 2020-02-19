import discord
from operator import itemgetter
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
    async def tutorial(self, ctx, lang = "EN"):
        """Affiche le tutoriel !"""
        lang = lang.upper()
        langlist = ["EN", "FR"]
        if lang not in langlist:
            lang = "EN"
        desc = lang_P.forge_msg(lang, "tuto", None, False, 1)
        msg = discord.Embed(title = lang_P.forge_msg(lang, "tuto", None, False, 0), color= 13752280, description = desc)
        msg.add_field(name=lang_P.forge_msg(lang, "tuto", None, False, 2), value="https://bastion-gaming.fr/get-gems/tutorial", inline=False)
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
            if desc[3] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc[3], inline=False)
            if desc[4] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc[4], inline=False)
            if desc[5] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc[5], inline=False)
            if desc[6] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc[6], inline=False)
            if desc[7] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc[7], inline=False)
            if desc[8] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc[8], inline=False)
            if desc[9] != "None":
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc[9], inline=False)
            if desc[10] != "None":
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
                type = str(now.year)
            if annee == None:
                annee = str(now.month)
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
                for one in msg[1]:
                    graph = GS.create_graph(ctx, one, annee, mois)
                    lang = graph[1]
                    if graph[0] == "404":
                        await ctx.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
                    else:
                        await ctx.send(file=discord.File("cache/{}".format(graph[0])))
                        os.remove("cache/{}".format(graph[0]))
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
    async def lang(self, ctx, langue = None):
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

    @commands.command(pass_context=True)
    async def stats(self, ctx, Nom = None):
        """
        Affichage des statistiques du joueur.
        """
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        if ge.permission(ctx, ge.Inquisiteur):
            param["nom"] = Nom
            if Nom == None:
                Nom = ctx.author.name
            else:
                Nom = ctx.guild.get_member(ge.nom_ID(Nom)).name
        else:
            param["nom"] = "None"
            Nom = ctx.author.name

        ge.socket.send_string(gg.std_send_command("stats", ID, ge.name_pl, param))
        tab = GF.msg_recv()
        lang = tab[1]
        if tab[0] == "NOK":
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
            return False
        ltab = len(tab)
        StatList = []
        for i in range(2, ltab):
            tab[i] = tab[i].replace("(", "")
            tab[i] = tab[i].replace(")", "")
            tab[i] = tab[i].replace("'", "")
            tab[i] = tab[i].split(", ")
            StatList.append((tab[i][0], tab[i][1], tab[i][2]))
        StatList = sorted(StatList, key=itemgetter(2))
        StatList = sorted(StatList, key=itemgetter(1))
        desc = ""           # Statistique non pris en charge
        descGeneral = ""     # bal, baltop, inv, market, divers
        descBuy = ""        # buy
        descSell = ""       # sell
        descDon = ""        # pay, give
        descForge = ""      # forge
        descBank = ""       # bank, stealing, crime, gamble
        descMine = ""       # mine
        descDig = ""        # dig
        descFish = ""       # fish
        descSlots = ""      # slots
        descBoxes = ""      # boxes
        descHothouse = ""   # hothouse
        descCooking = ""    # cooking
        descFerment = ""    # ferment
        for x in StatList:
            y = x[2].split(" | ")
            if x[1] == "bal" or x[1] == "inv" or x[1] == "market":
                if x[2] == x[1]:
                    descGeneral += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))

            elif x[1] == "baltop":
                if x[2] == x[1]:
                    descGeneral += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descGeneral += y[i] + " "
                        if i == len(y)-1:
                            descGeneral += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "buy":
                if x[2] == x[1]:
                    descBuy += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descBuy += y[i] + " "
                        if i == len(y)-1:
                            descBuy += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "sell":
                if x[2] == x[1]:
                    descSell += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descSell += y[i] + " "
                        if i == len(y)-1:
                            descSell += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "pay" or x[1] == "give":
                if x[2] == x[1]:
                    descDon += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(0, len(y)):
                        descDon += y[i] + " "
                        if i == len(y)-1:
                            descDon += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "forge":
                if x[2] == x[1]:
                    descForge += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descForge += y[i] + " "
                        if i == len(y)-1:
                            descForge += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "bank" or x[1] == "stealing" or x[1] == "crime" or x[1] == "gamble":
                if x[2] == x[1]:
                    descBank += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(0, len(y)):
                        descBank += y[i] + " "
                        if i == len(y)-1:
                            descBank += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "mine":
                if x[2] == x[1]:
                    descMine += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descMine += y[i] + " "
                        if i == len(y)-1:
                            descMine += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "fish":
                if x[2] == x[1]:
                    descFish += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descFish += y[i] + " "
                        if i == len(y)-1:
                            descFish += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "dig":
                if x[2] == x[1]:
                    descDig += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descDig += y[i] + " "
                        if i == len(y)-1:
                            descDig += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "slots":
                if x[2] == x[1]:
                    descSlots += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descSlots += y[i] + " "
                        if i == len(y)-1:
                            descSlots += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "boxes":
                if x[2] == x[1]:
                    descBoxes += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descBoxes += y[i] + " "
                        if i == len(y)-1:
                            descBoxes += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "hothouse":
                if x[2] == x[1]:
                    descHothouse += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descHothouse += y[i] + " "
                        if i == len(y)-1:
                            descHothouse += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "cooking":
                if x[2] == x[1]:
                    descCooking += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descCooking += y[i] + " "
                        if i == len(y)-1:
                            descCooking += ": `x{0}`\n\n".format(x[0])

            elif x[1] == "ferment":
                if x[2] == x[1]:
                    descFerment += "{2} **{1}** `x{0}`\n\n".format(x[0], x[2], lang_P.forge_msg(lang, "stats", None, False, 15))
                else:
                    for i in range(1, len(y)):
                        descFerment += y[i] + " "
                        if i == len(y)-1:
                            descFerment += ": `x{0}`\n\n".format(x[0])

            else:
                desc += "\n{1} `x{0}`".format(x[0], x[2])

        msg = discord.Embed(title = "Statistiques de {0}".format(Nom), color= 13752280, description = "")
        if descGeneral != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 0), value=descGeneral)
        if descBuy != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 1), value=descBuy)
        if descSell != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 2), value=descSell)
        if descDon != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 3), value=descDon)
        if descForge != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 4), value=descForge)
        if descBank != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 5), value=descBank)
        if descMine != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 6), value=descMine)
        if descFish != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 7), value=descFish)
        if descDig != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 8), value=descDig)
        if descSlots != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 9), value=descSlots)
        if descBoxes != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 10), value=descBoxes)
        if descHothouse != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 11), value=descHothouse)
        if descCooking != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 12), value=descCooking)
        if descFerment != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 13), value=descFerment)
        if desc != "":
            msg.add_field(name=lang_P.forge_msg(lang, "stats", None, False, 14), value=desc)

        await ctx.channel.send(embed = msg)

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


def setup(bot):
    bot.add_cog(GemsBase(bot))
    open("help/cogs.txt","a").write("GemsBase\n")
