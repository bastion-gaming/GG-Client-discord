import discord
from core import gestion as ge
from gems import gemsFonctions as GF, gemsStats as GS
from discord.ext import commands
from discord.ext.commands import bot
import gg_lib as gg
import os
import datetime as dt
from languages import lang as lang_P


class GemsMarket(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True, aliases=['achat', 'acheter'])
    async def buy(self, ctx, item, nb = 1):
        """**[item] {number}** | Allows you to purchase items sold at the market"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["nb"] = nb
        param["item"] = GF.trad_objet_inv(item)

        ge.socket.send_string(gg.std_send_command("buy", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 99:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 10))
        elif recv['error'] == 98:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", [GF.trad_objet(lang, recv["item"])], False, 10))
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif item == None:
            await ctx.channel.send(lang_P.forge_msg(lang, "buy", None, False, 2))
        elif recv['error'] == 0:
            for p in recv['perte']:
                if "gem" in p:
                    device = "{0}`{1}`".format(GF.build_idmoji("gem"), "Gems")
                else:
                    device = "{0}`{1}`".format(GF.build_idmoji("spinelle"), "Spinelles")
                cout = recv['perte'][p]
            desc = lang_P.forge_msg(lang, "buy", [nb, GF.trad_objet(lang, recv["item"]), GF.build_idmoji(param["item"]), cout, device], False, 0)
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 1), color= 13752280, description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))
        elif recv['error'] == 2:
            # Inventory full
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 2))
        elif recv['error'] == 3:
            # Anti-cheat
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 9))
        elif recv['error'] == 4:
            if "gem" in recv['device']:
                device = "{0}`{1}`".format(GF.build_idmoji("gem"), "Gems")
            else:
                device = "{0}`{1}`".format(GF.build_idmoji("spinelle"), "Spinelles")
            await ctx.channel.send(lang_P.forge_msg(lang, "buy", [device], False, 1))
        elif recv['error'] == 5:
            await ctx.channel.send(lang_P.forge_msg(lang, "buy", None, False, 2))

    @commands.command(pass_context=True, aliases=['vente', 'vendre'])
    async def sell(self, ctx, item, nb = 1):
        """**[item] {number}** | Allows you to sell your items!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["nb"] = nb
        param["item"] = GF.trad_objet_inv(item)

        ge.socket.send_string(gg.std_send_command("sell", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 99:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 10))
        elif recv['error'] == 98:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", [GF.trad_objet(lang, recv["item"])], False, 10))
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif item == None:
            await ctx.channel.send(lang_P.forge_msg(lang, "sell", None, False, 1))
        elif recv['error'] == 0:
            for p in recv['gain']:
                if "gem" in p:
                    device = "{0}`{1}`".format(GF.build_idmoji("gem"), "Gems")
                else:
                    device = "{0}`{1}`".format(GF.build_idmoji("spinelle"), "Spinelles")
                cout = recv['gain'][p]
            desc = lang_P.forge_msg(lang, "sell", [nb, GF.trad_objet(lang, recv["item"]), GF.build_idmoji(param["item"]), cout, device], False, 0)
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 1), color= 13752280, description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "sell", [GF.trad_objet(lang, recv["item"]), GF.build_idmoji(item), recv['nbItem']], False, 2))
        elif recv['error'] == 5:
            await ctx.channel.send(lang_P.forge_msg(lang, "sell", None, False, 1))

    @commands.command(pass_context=True, aliases=['marcher', 'marche', 'marché'])
    async def market(self, ctx, fct = None):
        """**{stand}** | Allows you to see all the items you can buy or sell!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        if fct is not None:
            fct = fct.lower()
        param["fct"] = fct

        ge.socket.send_string(gg.std_send_command("market", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 99:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 10))
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['etat'] == "OK":
            msg_titre = lang_P.forge_msg(lang, "market", None, False, 4)
            msg_desc = "{0}\n{1}".format(lang_P.forge_msg(lang, "market", None, False, 2), lang_P.forge_msg(lang, "market", [recv['time'][0], recv['time'][1], recv['time'][2]], False, 3))
            msg = discord.Embed(title = msg_titre, color= 2461129, description = msg_desc)
            for one in recv['market']:
                if recv['market'][one] != {}:
                    if one == "outils" and (fct == None or ("outil" in fct)):
                        desc = desc_VA = desc_info = ""
                        for two in recv['market']['outils']:
                            desc += "\n{idmoji}`{name}`".format(name=GF.trad_objet(lang, two), idmoji=GF.build_idmoji(two))
                            desc_VA += "\n`{vente}`{argent}_{PV} _|`{achat}`{argent}_{PA} _".format(argent=GF.build_idmoji("gem"), vente=recv['market']['outils'][two]["vente"], achat=recv['market']['outils'][two]["achat"], PV=recv['market']['outils'][two]["PV"], PA=recv['market']['outils'][two]["PA"])
                            desc_info += "\n`{spec}:` {valeur}".format(spec=lang_P.forge_msg(lang, "spec", None, False, 0), valeur=recv['market']['outils'][two]["durability"])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 0), value=desc, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc_VA, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 6), value=desc_info, inline=True)
                    elif one == "upgrade" and (fct == None or ("upgrade" in fct)):
                        desc = desc_A = desc_info = ""
                        for two in recv['market']['upgrade']:
                            desc += "\n{idmoji}`{name}`".format(name=GF.trad_objet(lang, two), idmoji=GF.build_idmoji(two))
                            desc_A += "\n`{achat}`{argent}".format(argent=GF.build_idmoji("gem"), achat=recv['market']['upgrade'][two]["achat"])
                            desc_info += "\n`{info}`".format(info=lang_P.forge_msg(lang, "upgrade_infos", None, False, recv['market']['upgrade'][two]['info']))
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 7), value=desc, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "graphbourse", None, False, 0), value=desc_A, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 6), value=desc_info, inline=True)
            for one in recv['market']['items']:
                if recv['market']['items'][one] != {}:
                    if one == "special":
                        desc = desc_VA = desc_info = ""
                        for two in recv['market']['special']:
                            desc += "\n{idmoji}`{name}`".format(name=GF.trad_objet(lang, two), idmoji=GF.build_idmoji(two))
                            desc_VA += "\n`{vente}`{argent}_{PV} _|`{achat}`{argent}_{PA} _".format(argent=GF.build_idmoji("gem"), vente=recv['market']['special'][two]["vente"], achat=recv['market']['special'][two]["achat"], PV=recv['market']['special'][two]["PV"], PA=recv['market']['special'][two]["PA"])
                            desc_info += "\n`{spec}:` {valeur}".format(spec=lang_P.forge_msg(lang, "spec", None, False, 0), valeur=recv['market']['special'][two]["durability"])
                        for two in recv['market']['items'][one]:
                            desc += "\n{idmoji}`{name}`".format(name=GF.trad_objet(lang, two), idmoji=GF.build_idmoji(two))
                            desc_VA += "\n`{vente}`{argent}_{PV} _|`{achat}`{argent}_{PA} _".format(argent=GF.build_idmoji("gem"), vente=recv['market']['items'][one][two]["vente"], achat=recv['market']['items'][one][two]["achat"], PV=recv['market']['items'][one][two]["PV"], PA=recv['market']['items'][one][two]["PA"])
                            desc_info += "\n`{spec}:` {valeur}".format(spec=lang_P.forge_msg(lang, "spec", None, False, 1), valeur=recv['market']['items'][one][two]["poids"])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 1), value=desc, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc_VA, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 6), value=desc_info, inline=True)
                    elif one == "minerai" and (fct == None or ("mine" in fct)):
                        desc = desc_VA = desc_info = ""
                        for two in recv['market']['items'][one]:
                            desc += "\n{idmoji}`{name}`".format(name=GF.trad_objet(lang, two), idmoji=GF.build_idmoji(two))
                            desc_VA += "\n`{vente}`{argent}_{PV} _|`{achat}`{argent}_{PA} _".format(argent=GF.build_idmoji("gem"), vente=recv['market']['items'][one][two]["vente"], achat=recv['market']['items'][one][two]["achat"], PV=recv['market']['items'][one][two]["PV"], PA=recv['market']['items'][one][two]["PA"])
                            desc_info += "\n`{spec}:` {valeur}".format(spec=lang_P.forge_msg(lang, "spec", None, False, 1), valeur=recv['market']['items'][one][two]["poids"])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 3), value=desc, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc_VA, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 6), value=desc_info, inline=True)
                    elif one == "poisson" and (fct == None or ("fish" in fct or "poisson" in fct)):
                        desc = desc_VA = desc_info = ""
                        for two in recv['market']['items'][one]:
                            desc += "\n{idmoji}`{name}`".format(name=GF.trad_objet(lang, two), idmoji=GF.build_idmoji(two))
                            desc_VA += "\n`{vente}`{argent}_{PV} _|`{achat}`{argent}_{PA} _".format(argent=GF.build_idmoji("gem"), vente=recv['market']['items'][one][two]["vente"], achat=recv['market']['items'][one][two]["achat"], PV=recv['market']['items'][one][two]["PV"], PA=recv['market']['items'][one][two]["PA"])
                            desc_info += "\n`{spec}:` {valeur}".format(spec=lang_P.forge_msg(lang, "spec", None, False, 1), valeur=recv['market']['items'][one][two]["poids"])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 4), value=desc, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc_VA, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 6), value=desc_info, inline=True)
                    elif one == "plante" and (fct == None or ("plant" in fct)):
                        desc = desc_VA = desc_info = ""
                        for two in recv['market']['items'][one]:
                            desc += "\n{idmoji}`{name}`".format(name=GF.trad_objet(lang, two), idmoji=GF.build_idmoji(two))
                            desc_VA += "\n`{vente}`{argent}_{PV} _|`{achat}`{argent}_{PA} _".format(argent=GF.build_idmoji("gem"), vente=recv['market']['items'][one][two]["vente"], achat=recv['market']['items'][one][two]["achat"], PV=recv['market']['items'][one][two]["PV"], PA=recv['market']['items'][one][two]["PA"])
                            desc_info += "\n`{spec}:` {valeur}".format(spec=lang_P.forge_msg(lang, "spec", None, False, 1), valeur=recv['market']['items'][one][two]["poids"])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 5), value=desc, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc_VA, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 6), value=desc_info, inline=True)
                    elif one == "consommable" and (fct == None or ("item" in fct or "cons" in fct)):
                        desc = desc_VA = desc_info = ""
                        for two in recv['market']['items'][one]:
                            desc += "\n{idmoji}`{name}`".format(name=GF.trad_objet(lang, two), idmoji=GF.build_idmoji(two))
                            desc_VA += "\n`{vente}`{argent}_{PV} _|`{achat}`{argent}_{PA} _".format(argent=GF.build_idmoji("gem"), vente=recv['market']['items'][one][two]["vente"], achat=recv['market']['items'][one][two]["achat"], PV=recv['market']['items'][one][two]["PV"], PA=recv['market']['items'][one][two]["PA"])
                            desc_info += "\n`{spec}:` {valeur}".format(spec=lang_P.forge_msg(lang, "spec", None, False, 1), valeur=recv['market']['items'][one][two]["poids"])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 2), value=desc, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc_VA, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 6), value=desc_info, inline=True)
                    elif one == "event" and (fct == None or ("even" in fct or "évèn" in fct)):
                        desc = desc_VA = desc_info = ""
                        for two in recv['market']['items'][one]:
                            desc += "\n{idmoji}`{name}`".format(name=GF.trad_objet(lang, two), idmoji=GF.build_idmoji(two))
                            desc_VA += "\n`{vente}`{argent}_{PV} _|`{achat}`{argent}_{PA} _".format(argent=GF.build_idmoji("gem"), vente=recv['market']['items'][one][two]["vente"], achat=recv['market']['items'][one][two]["achat"], PV=recv['market']['items'][one][two]["PV"], PA=recv['market']['items'][one][two]["PA"])
                            desc_info += "\n`{spec}:` {valeur}".format(spec=lang_P.forge_msg(lang, "spec", None, False, 1), valeur=recv['market']['items'][one][two]["poids"])
                        msg.add_field(name=lang_P.forge_msg(lang, "categorie", None, False, 6), value=desc, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 5), value=desc_VA, inline=True)
                        msg.add_field(name=lang_P.forge_msg(lang, "market", None, False, 6), value=desc_info, inline=True)
            await ctx.channel.send(embed = msg)
        else:
            await ctx.channel.send('Error')

    @commands.command(pass_context=True, aliases=['payer'])
    async def pay(self, ctx, nom, gain):
        """**[name] [prize]** | Give money to your friends!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["nom"] = ctx.author.name
        param["ID_recu"] = nom
        try:
            param["Nom_recu"] = ctx.guild.get_member(ge.nom_ID(param["ID_recu"])).name
        except:
            param["Nom_recu"] = nom
        param["gain"] = gain

        ge.socket.send_string(gg.std_send_command("pay", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 99:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 10))
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 405:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 6))
        elif recv['error'] == 0:
            desc = lang_P.forge_msg(lang, "pay", [param["nom"], recv['gain'], param["Nom_recu"], GF.build_idmoji("gem")], False, 0)
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 3), color= 13752280, description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 3))
        elif recv['error'] == 3:
            await ctx.channel.send(lang_P.forge_msg(lang, "pay", None, False, 2))
        elif recv['error'] == 4:
            await ctx.channel.send(lang_P.forge_msg(lang, "pay", [param["nom"], recv['don'], param["Nom_recu"], GF.build_idmoji("gem")], False, 1))

    @commands.command(pass_context=True, aliases=['donner'])
    async def give(self, ctx, nom, item, nb = None):
        """**[name] [item] [number]** | Give items to your friends!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["nom"] = ctx.author.name
        param["ID_recu"] = nom
        try:
            param["Nom_recu"] = ctx.guild.get_member(ge.nom_ID(param["ID_recu"])).name
        except:
            param["Nom_recu"] = nom
        param["item"] = GF.trad_objet_inv(item)
        param["nb"] = nb

        ge.socket.send_string(gg.std_send_command("give", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 99:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 10))
        elif recv['error'] == 98:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", [GF.trad_objet(lang, recv["item"])], False, 11))
        elif recv['error'] == 97:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", [GF.trad_objet(lang, recv["item"]), recv['Nom_recu']], False, 12))
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 405:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 6))
        elif recv['error'] == 0:
            desc = lang_P.forge_msg(lang, "give", [recv["nom"], recv['nb'], recv["nom_recu"], GF.build_idmoji(recv['item']), GF.trad_objet(lang, recv["item"])], False, 0)
            msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 3), color= 13752280, description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 3))
        elif recv['error'] == 3:
            await ctx.channel.send(lang_P.forge_msg(lang, "give", None, False, 2))
        elif recv['error'] == 4:
            await ctx.channel.send(lang_P.forge_msg(lang, "give", [recv["nom"], recv['nb'], recv["nom_recu"], GF.build_idmoji(recv['item']), GF.trad_objet(lang, recv["item"])], False, 1))
        elif recv['error'] == 5:
            await ctx.channel.send(lang_P.forge_msg(lang, "give", [recv["nom_recu"]], False, 4))
        elif recv['error'] == 6:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", [recv['amende']], False, 9))
        elif recv['error'] == 7:
            await ctx.channel.send(lang_P.forge_msg(lang, "give", None, False, 3))


def setup(bot):
    bot.add_cog(GemsMarket(bot))
    open("help/cogs.txt", "a").write("GemsMarket\n")
