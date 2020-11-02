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
    async def tutorial(self, ctx, lang = "EN"):
        """Displays the tutorial !"""
        lang = lang.upper()
        langlist = ["EN", "FR"]
        if lang not in langlist:
            lang = "EN"
        desc = lang_P.forge_msg(lang, "tuto", None, False, 1)
        msg = discord.Embed(title = lang_P.forge_msg(lang, "tuto", None, False, 0), color= 13752280, description = desc)
        msg.add_field(name=lang_P.forge_msg(lang, "tuto", None, False, 2), value="https://get-gems.bastion-gaming.fr/tutorial", inline=False)
        await ctx.channel.send(embed = msg)

    @commands.command(pass_context=True)
    async def begin(self, ctx):
        """To create your player account and get your starter kit!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["name"] = ctx.author.name
        ge.socket.send_string(gg.std_send_command("begin", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg["desc"])

    @commands.command(pass_context=True)
    async def connect(self, ctx, PlayerID):
        """**[PlayerID]** | WIP | Connecting a player account from another platform"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["PlayerID"] = PlayerID
        ge.socket.send_string(gg.std_send_command("connect", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        # if desc["type"] == "OK":
        #     # A faire
        await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def infos(self, ctx, nom = None):
        """**{name}** | Display player information"""
        ID = ctx.author.id
        param = dict()
        if nom is None:
            nom = ctx.author.name
            param["ID"] = ID
            param["name"] = nom
        else:
            IDname = ge.nom_ID(nom)
            param["ID"] = nom
            try:
                nom = ctx.guild.get_member(IDname).name
            except:
                pass
            param["name"] = nom
        ge.socket.send_string(gg.std_send_command("infos", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        if desc["type"] == "OK":
            lang = desc["lang"]
            title = lang_P.forge_msg(lang, "infos", [nom])
            msg = discord.Embed(title = title, color= 13752280, description = desc["playerid"], timestamp=dt.datetime.now())
            msg.add_field(name="**_Balance_**", value=desc["balance"], inline=False)

            msg.add_field(name=desc["lvl"], value=desc["xp"], inline=False)
            msg.add_field(name=desc["godparent titre"], value=desc["godparent"], inline=False)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
            # Message de réussite dans la console
            print("Gems >> Informations de {0} affichée par {1}".format(nom, ctx.author.name))
            return
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def username(self, ctx, NU):
        """**{new username}** | Change your username!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["NU"] = NU
        ge.socket.send_string(gg.std_send_command("username", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def bal(self, ctx, nom = None):
        """**{name}** | Are you rich or poor?"""
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
        if desc["type"] == "OK":
            lang = desc["lang"]
            title = lang_P.forge_msg(lang, "bal", [nom], False)
            msg = discord.Embed(title = title, color= 13752280, description = "", timestamp=dt.datetime.now())
            msg.add_field(name="**_Balance_**", value=desc["balance"], inline=False)

            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
            # Message de réussite dans la console
            print("Gems >> Balance de {} affichée".format(nom))
            return
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def baltop(self, ctx, n = None, m = None):
        """**{filter} {number}** | Player rankings"""
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

        if desc["type"] == "OK":
            lang = desc["lang"]
            if filtre == "gems" or filtre == "gem" or filtre == "spinelles" or filtre == "spinelle":
                Titre = lang_P.forge_msg(lang, "baltop", None, False, 0)
                if filtre == "spinelles" or filtre == "spinelle":
                    Titre = lang_P.forge_msg(lang, "baltop", [GF.get_idmoji("spinelle")], False, 1)

                msg = discord.Embed(title = Titre, color= 13752280, description = desc["baltop"])
                # Message de réussite dans la console
                print("Gems >> {} a afficher le classement des {} premiers joueurs | Filtre: {}".format(ctx.author.name, n, filtre))

            elif filtre == "guild" or filtre == "guilde":
                Titre = lang_P.forge_msg(lang, "baltop", None, False, 2)
                msg = discord.Embed(title = Titre, color= 13752280, description = desc["baltop"])
                # Message de réussite dans la console
                print("Gems >> {} a afficher le classement des {} premières guildes".format(ctx.author.name, n))

            else:
                msg = discord.Embed(title = "Classement", color= 13752280, description = "Erreur! Commande incorrect")
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def buy(self, ctx, item, nb = 1):
        """**[item] {number}** | Allows you to purchase items sold at the market"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["nb"] = nb
        param["item"] = item

        ge.socket.send_string(gg.std_send_command("buy", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]
        if desc["type"] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 1), color= 13752280, description = desc["desc"])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def sell(self, ctx, item, nb = 1):
        """**[item] {number}** | Allows you to sell your items!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["nb"] = nb
        param["item"] = item

        ge.socket.send_string(gg.std_send_command("sell", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]
        if desc["type"] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 2), color= 13752280, description = desc["desc"])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def inv(self, ctx, fct = None):
        """**{pocket name}** | Allows you to see what you have in your belly!"""
        ID = ctx.author.id
        nom = ctx.author.name
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("inv", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]

        if desc["type"] == "OK":
            msg_titre = lang_P.forge_msg(lang, "inv", [nom], False, 0)
            msg = discord.Embed(title = msg_titre, color= 6466585, description = desc["desc"])
            invD = desc["inv"]
            for one in invD.keys():
                if one == "outils":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=invD["outils"], inline=False)
                elif one == "special":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=invD["special"], inline=False)
                elif one == "minerai":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=invD["minerai"], inline=False)
                elif one == "poisson":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=invD["poisson"], inline=False)
                elif one == "plante":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=invD["plante"], inline=False)
                elif one == "consommable":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=invD["consommable"], inline=False)
                elif one == "event":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=invD["event"], inline=False)
                elif one == "lootbox":
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=invD["lootbox"], inline=False)
            await ctx.channel.send(embed = msg)

        elif desc["type"] == "pockets":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "inv", None, False, 1), color= 6466585, description = desc["desc"], timestamp=dt.datetime.now())
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)

        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def market(self, ctx, fct = None):
        """**{stand}** | Allows you to see all the items you can buy or sell!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("market", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]

        if desc["type"] == "OK":
            if fct != None:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "market", [fct], False, 1), color= 2461129, description = desc["desc"], timestamp=dt.datetime.now())
            else:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "market", None, False, 0), color= 2461129, description = desc["desc"], timestamp=dt.datetime.now())
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            if fct == "mobile":
                stands = []
                StandsMobile = {}
                for k in desc.keys():
                    if k not in ["type", "lang", "desc"]:
                        if "prix" not in k and "info" not in k:
                            stands.append(k)
                for one in stands:
                    Stand = desc[one].split("\n")
                    StandP = desc["{0} prix".format(one)].split("\n")
                    StandI = desc["{0} info".format(one)].split("\n")
                    StandD = ""
                    for i in range(1, len(Stand)):
                        StandD += "\n{0}: {1} | {2}".format(Stand[i], StandP[i], StandI[i])
                    StandsMobile[one] = StandD
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=StandsMobile["outils"], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=StandsMobile["special"], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=StandsMobile["minerai"], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=StandsMobile["poisson"], inline=False)
                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=StandsMobile["plante"], inline=False)
                try:
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=StandsMobile["items"], inline=False)
                except KeyError:
                    pass
                try:
                    msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=StandsMobile["event"], inline=False)
                except KeyError:
                    pass

                msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=StandsMobile["lootbox"], inline=False)
                await ctx.channel.send(embed = msg)

            else:
                if fct == None or ("outil" in fct):
                    try:
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc["outils"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc["outils prix"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc["outils info"], inline=True)
                    except KeyError:
                        pass

                if fct == None or ("outil" or "item" or "minerai" in fct) or fct == "poissons" or fct == "fish" or fct == "plantes" or fct == "plants" or fct == "event" or fct == "événements":
                    try:
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc["special"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc["special prix"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc["special info"], inline=True)
                    except KeyError:
                        pass

                if fct == None or ("minerai" in fct):
                    try:
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc["minerai"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc["minerai prix"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc["minerai info"], inline=True)
                    except KeyError:
                        pass

                if fct == None or fct == "fish" or fct == "poissons":
                    try:
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc["poisson"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc["poisson prix"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc["poisson info"], inline=True)
                    except KeyError:
                        pass

                if fct == None or fct == "plants" or fct == "plantes":
                    try:
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc["plante"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc["plante prix"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc["plante info"], inline=True)
                    except KeyError:
                        pass

                if fct == None or ("item" in fct):
                    try:
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc["consommable"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc["consommable prix"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc["consommable info"], inline=True)
                    except KeyError:
                        pass

                if fct == None or fct == "event" or fct == "événements":
                    try:
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc["event"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 2), value=desc["event prix"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 4), value=desc["event info"], inline=True)
                    except KeyError:
                        pass

                if fct == None or fct == "lootbox":
                    try:
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=desc["lootbox"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 3), value=desc["lootbox prix"], inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc["lootbox info"], inline=True)
                    except KeyError:
                        pass
                await ctx.channel.send(embed = msg)

        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def pay(self, ctx, nom, gain):
        """**[name] [prize]** | Give money to your friends!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["nom"] = ctx.author.name
        param["ID_recu"] = nom
        try:
            param["Nom_recu"] = ctx.guild.get_member(ge.nom_ID(param["ID_recu"])).name
        except:
            param["Nom_recu"] = nom
        param["gain"] = gain

        ge.socket.send_string(gg.std_send_command("pay", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]
        if desc["type"] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 3), color= 13752280, description = desc["desc"])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def give(self, ctx, nom, item, nb = None):
        """**[name] [item] [number]** | Give items to your friends!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["nom"] = ctx.author.name
        param["ID_recu"] = nom
        try:
            param["Nom_recu"] = ctx.guild.get_member(ge.nom_ID(param["ID_recu"])).name
        except:
            param["Nom_recu"] = nom
        param["item"] = item
        param["nb"] = nb

        ge.socket.send_string(gg.std_send_command("give", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]
        if desc["type"] == "OK":
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 3), color= 13752280, description = desc["desc"])
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def forge(self, ctx, item = None, nb = 1):
        """**{item} {number}** | Allows you to design specific items"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        param["item"] = item
        param["nb"] = nb

        ge.socket.send_string(gg.std_send_command("forge", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]
        if desc["type"] == "OK":
            if item == None:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "recette"), color= 15778560, description = desc["desc"])
                await ctx.channel.send(embed = msg)
            else:
                msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 4), color= 13752280, description = desc["desc"])
                msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def graphbourse(self, ctx, item, moisD = None, anneeD = None, moisF = None, anneeF = None, type = None):
        """**[item] {start month} {start year} {final month} {final year}** | Exchange History by Item"""
        ID = ctx.author.id
        now = dt.datetime.now()

        if item.lower() == "all":
            if anneeF is not None:
                temp = type
            type = moisD.lower()
            if anneeD is None:
                anneeD = str(now.year)
                moisD = str(now.month)
            else:
                moisD = anneeD
                anneeD = moisF
            if anneeF is None:
                moisF = str(now.month)
                anneeF = str(now.year)
            else:
                moisF = anneeF
                anneeF = temp
            param = dict()
            param["ID"] = ID
            param["type"] = type

            ge.socket.send_string(gg.std_send_command("listobjet", ID, ge.name_pl, param))
            msg = GF.msg_recv()

            if msg[0] == "NOK":
                await ctx.channel.send(msg[1])
            else:
                for one in msg[1]:
                    graph = GS.create_graphbourse(ctx, one, anneeD, moisD, anneeF, moisF)
                    lang = graph[1]
                    if graph[0] == "404":
                        await ctx.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
                    else:
                        await ctx.send(file=discord.File("cache/{}".format(graph[0])))
                        os.remove("cache/{}".format(graph[0]))
        else:
            if moisD == None:
                moisD = str(now.month)
            if anneeD == None:
                anneeD = str(now.year)
            if moisF == None:
                moisF = str(now.month)
            if anneeF == None:
                anneeF = str(now.year)
            graph = GS.create_graphbourse(ctx, item, anneeD, moisD, anneeF, moisF)
            lang = graph[1]
            if graph[0] == "404":
                await ctx.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
            else:
                await ctx.send(file=discord.File("cache/{}".format(graph[0])))
                os.remove("cache/{}".format(graph[0]))

    @commands.command(pass_context=True)
    async def lang(self, ctx, langue = None):
        """**{language}** | Allows you to change the language for a player."""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["langue"] = langue

        ge.socket.send_string(gg.std_send_command("lang", ID, ge.name_pl, param))
        desc = GF.msg_recv()

        await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True)
    async def godparent(self, ctx, nom):
        """**[name]** | Allows you to add a player as a godparent."""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["GPID"] = nom
        ge.socket.send_string(gg.std_send_command("godparent", ID, ge.name_pl, param))
        desc = GF.msg_recv()
        lang = desc["lang"]
        if ID == ge.nom_ID(nom) or ctx.author.name == nom:
            await ctx.channel.send(lang_P.forge_msg(lang, "godparent"))
        else:
            await ctx.channel.send(desc["desc"])

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
    open("help/cogs.txt", "a").write("GemsBase\n")