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

    # @commands.command(pass_context=True)
    # async def tutorial(self, ctx, lang = "EN"):
    #     """Displays the tutorial !"""
    #     lang = lang.upper()
    #     langlist = ["EN", "FR"]
    #     if lang not in langlist:
    #         lang = "EN"
    #     desc = lang_P.forge_msg(lang, "tuto", None, False, 1)
    #     msg = discord.Embed(title = lang_P.forge_msg(lang, "tuto", None, False, 0), color= 13752280, description = desc)
    #     msg.add_field(name=lang_P.forge_msg(lang, "tuto", None, False, 2), value="https://get-gems.bastion-gaming.fr/tutorial", inline=False)
    #     await ctx.channel.send(embed = msg)

    @commands.command(pass_context=True, aliases=['commencer', 'start'])
    async def begin(self, ctx, lang = None):
        """To create your player account and get your starter kit!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["name"] = ctx.author.name
        ge.socket.send_string(gg.std_send_command("begin", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        if lang in ['FR', 'EN']:
            lang = lang
        else:
            lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            msg = lang_P.forge_msg(lang, "WarningMsg", None, False, 0)
        elif recv['etat'] == "OK":
            msg = lang_P.forge_msg(lang, "newPlayer", None, False, 0)
            # Message RGPD
            msg += lang_P.forge_msg(lang, "newPlayer", None, False, 2)
        else:
            msg = lang_P.forge_msg(lang, "newPlayer", None, False, 1)
        await ctx.channel.send(msg)

    # @commands.command(pass_context=True)
    # async def connect(self, ctx, PlayerID):
    #     """**[PlayerID]** | WIP | Connecting a player account from another platform"""
    #     ID = ctx.author.id
    #     param = dict()
    #     param["ID"] = ID
    #     param["PlayerID"] = PlayerID
    #     ge.socket.send_string(gg.std_send_command("connect", ID, ge.name_pl, param))
    #     recv = GF.msg_recv()
    #     lang = recv['lang']
    #     if recv['error'] == 100:
    #         await ctx.channel.send(recv['etat'])
    #     elif recv['error'] == 404:
    #         msg = lang_P.forge_msg(lang, "WarningMsg", None, False, 0)
    #     else:
    #         msg = "in build"
    #     await ctx.channel.send(msg)

    @commands.command(pass_context=True, aliases=['info', 'inf'])
    async def infos(self, ctx, nom = None):
        """**{name}** | Display player information"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["name"] = nom
        ge.socket.send_string(gg.std_send_command("infos", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        else:
            nom = recv['info']["Pseudo"]
            title = lang_P.forge_msg(lang, "infos", [nom], False, 0)
            msg = discord.Embed(title = title, color= 13752280, description = '{0}'.format(lang_P.forge_msg(lang, "infos", [recv['info']["PlayerID"], nom], False, 1)), timestamp=dt.datetime.now())
            Bdesc = "{g} {idmoji}`Gems`".format(g=recv['info']["Gems"], idmoji=GF.build_idmoji("gem"))
            if recv['info']['Spinelles'] != 0:
                Bdesc += "{g} {idmoji}`Spinelles`".format(g=recv['info']["Spinelles"], idmoji=GF.build_idmoji("spinelle"))
            msg.add_field(name="**_Balance_**", value=Bdesc, inline=False)

            msg.add_field(name='{0}'.format(lang_P.forge_msg(lang, "infos", [recv['info']["Level"]], False, 2)), value='XP: `{0}`'.format(recv['info']["XP"]), inline=False)

            GPdesc = '{}: '.format(lang_P.forge_msg(lang, "godparent", None, False, 0))
            if recv['info']['Godparent'] is not False:
                GPdesc += '`{0}`'.format(recv['info']['Godparent'])
            if recv['info']['Godchilds'] is not False:
                F_li = recv['info']['Godchilds']
                if len(F_li) > 1:
                    sV = "s"
                else:
                    sV = ""
                GPdesc += '\n{2}{1} `x{0}`: '.format(len(F_li), sV, lang_P.forge_msg(lang, "godparent", None, False, 1))
                for one in F_li:
                    GPdesc += "\n• _{0}_".format(one)

            msg.add_field(name=lang_P.forge_msg(lang, "godparent", None, False, 2), value=GPdesc, inline=False)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
            # Message de réussite dans la console
            print("Gems >> Informations de {0} affichée par {1}".format(nom, ctx.author.name))

    @commands.command(pass_context=True, aliases=['name', 'pseudo'])
    async def username(self, ctx, NU):
        """**{new username}** | Change your username!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["NU"] = NU
        ge.socket.send_string(gg.std_send_command("username", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['etat'] == "OK":
            await ctx.channel.send(lang_P.forge_msg(lang, "username", None, False, 0))
        else:
            await ctx.channel.send(lang_P.forge_msg(lang, "username", None, False, 1))

    @commands.command(pass_context=True, aliases=['top'])
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
        param["filtre"] = filtre
        ge.socket.send_string(gg.std_send_command("baltop", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 0:
            j = 1
            UserList = recv['baltop']
            desc = ""
            for one in UserList: # affichage des données trié
                if j <= n:
                    desc += "{2} |{3} `{0}`: {1} {4}`Gems`".format(one[0], one[1], j, one[3], GF.build_idmoji("gem"))
                    if one[2] != 0:
                        desc += " | {0} {1}`Spinelles`\n".format(one[2], GF.build_idmoji("spinelle"))
                    else:
                        desc += "\n"
                j += 1
            Titre = lang_P.forge_msg(lang, "baltop", [GF.build_idmoji("gem")], False, 1)
            if "spinelle" in filtre:
                Titre = lang_P.forge_msg(lang, "baltop", GF.build_idmoji("spinelle"), False, 2)
            msg = discord.Embed(title = Titre, color= 13752280, description = desc)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "baltop", None, False, 0))

    @commands.command(pass_context=True, aliases=['inv', 'i', 'inventaire'])
    async def inventory(self, ctx, fct = None):
        """**{pocket name}** | Allows you to see what you have in your belly!"""
        ID = ctx.author.id
        nom = ctx.author.name
        param = dict()
        param["ID"] = ID
        # param["IDGuild"] = ctx.guild.id
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("inventory", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['etat'] == "OK":
            msg_titre = lang_P.forge_msg(lang, "inv", [nom], False, 0)
            msg_desc = "\n{2}: `{0}/{1}`".format(recv['taille'][0], recv['taille'][1], lang_P.forge_msg(lang, "inv", None, False, 1))
            if recv['taille'][0] >= recv['taille'][1]:
                msg_desc += " :bangbang:"
            msg = discord.Embed(title = msg_titre, color= 6466585, description = msg_desc)
            for one in recv['inventory']:
                if recv['inventory'][one] != {}:
                    if one == "outils":
                        desc = ""
                        for two in recv['inventory']['outils']:
                            desc += "\n{idmoji}`{name}`: `x{stock}` | {dname}: `{durability}/{dMax}`".format(name=two, idmoji=GF.build_idmoji(two), stock=recv['inventory'][one][two]['stock'], durability=recv['inventory']['outils'][two]['durability'], dMax=recv['inventory']['outils'][two]['durabilityMax'], dname=lang_P.forge_msg(lang, "inv", None, False, 2))
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc, inline=False)
                    elif one == "upgrade":
                        desc = ""
                        for two in recv['inventory']['upgrade']:
                            desc += "\n{idmoji}`{name}`: `x{stock}`".format(name=two, idmoji=GF.build_idmoji(two), stock=recv['inventory'][one][two]['stock'])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=desc, inline=False)
            for one in recv['inventory']['items']:
                if recv['inventory']['items'][one] != {}:
                    if one == "special":
                        desc = ""
                        for two in recv['inventory']['items']['special']:
                            desc += "\n{idmoji}`{name}`: `x{stock}`".format(name=two, idmoji=GF.build_idmoji(two), stock=recv['inventory']['items'][one][two]['stock'])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc, inline=False)
                    elif one == "minerai":
                        desc = ""
                        for two in recv['inventory']['items']['minerai']:
                            desc += "\n{idmoji}`{name}`: `x{stock}`".format(name=two, idmoji=GF.build_idmoji(two), stock=recv['inventory']['items'][one][two]['stock'])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc, inline=False)
                    elif one == "poisson":
                        desc = ""
                        for two in recv['inventory']['items']['poisson']:
                            desc += "\n{idmoji}`{name}`: `x{stock}`".format(name=two, idmoji=GF.build_idmoji(two), stock=recv['inventory']['items'][one][two]['stock'])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc, inline=False)
                    elif one == "plante":
                        desc = ""
                        for two in recv['inventory']['items']['plante']:
                            desc += "\n{idmoji}`{name}`: `x{stock}`".format(name=two, idmoji=GF.build_idmoji(two), stock=recv['inventory']['items'][one][two]['stock'])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc, inline=False)
                    elif one == "consommable":
                        desc = ""
                        for two in recv['inventory']['items']['consommable']:
                            desc += "\n{idmoji}`{name}`: `x{stock}`".format(name=two, idmoji=GF.build_idmoji(two), stock=recv['inventory']['items'][one][two]['stock'])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc, inline=False)
                    elif one == "event":
                        desc = ""
                        for two in recv['inventory']['items']['event']:
                            desc += "\n{idmoji}`{name}`: `x{stock}`".format(name=two, idmoji=GF.build_idmoji(two), stock=recv['inventory']['items'][one][two]['stock'])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc, inline=False)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send('Error')

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
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif item == None:
            desc = ""
            for one in recv['recettes']:
                desc += "\n• {idmoji}`{name}` :arrow_right: ".format(name=one, idmoji=GF.build_idmoji(one))
                i = 0
                for two in recv['recettes'][one]:
                    if i != 0:
                        desc += ", "
                    desc += "x{nb} {idmoji}`{name}`".format(name=two, idmoji=GF.build_idmoji(two), nb=recv['recettes'][one][two])
                    i += 1
            msg = discord.Embed(title = lang_P.forge_msg(lang, "recette"), color= 15778560, description = desc)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 0:
            desc = lang_P.forge_msg(lang, "forge", [nb, item, GF.build_idmoji(item)], False, 0)
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 4), color= 13752280, description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 2))
        elif recv['error'] == 3:
            await ctx.channel.send(lang_P.forge_msg(lang, "forge", None, False, 2))
        elif recv['error'] == 4:
            await ctx.channel.send(lang_P.forge_msg(lang, "forge", [recv['nbmissing'], recv['missing'], GF.build_idmoji(recv['missing'])], False, 1))

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

    @commands.command(pass_context=True, aliases=['l', 'langue'])
    async def lang(self, ctx, langue = None):
        """**{language}** | Allows you to change the language for a player."""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["langue"] = langue

        ge.socket.send_string(gg.std_send_command("lang", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif langue is None:
            await ctx.channel.send(lang_P.forge_msg(lang, "lang", None, False, 2))
        elif recv['etat'] == "OK":
            await ctx.channel.send(lang_P.forge_msg(lang, "lang", None, False, 0))
        else:
            await ctx.channel.send(lang_P.forge_msg(lang, "lang", None, False, 1))

    @commands.command(pass_context=True, aliases=['parrain', 'marraine'])
    async def godparent(self, ctx, nom):
        """**[name]** | Allows you to add a player as a godparent."""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["GPID"] = nom
        ge.socket.send_string(gg.std_send_command("godparent", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 0:
            desc = lang_P.forge_msg(lang, "godparent", [recv['gain']['gems'], GF.build_idmoji("gem"), recv['gain']['XP']], False, 3)
            desc += "\n"
            desc += lang_P.forge_msg(lang, "godparent", [recv['gainGP']['gems'], GF.build_idmoji("gem"), recv['gainGP']['XP']], False, 4)
            await ctx.channel.send(desc)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 6))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "godparent", None, False, 5))
        elif recv['error'] == 3:
            await ctx.channel.send(lang_P.forge_msg(lang, "godparent", None, False, 6))

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
