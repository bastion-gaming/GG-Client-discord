import discord
from discord.ext import commands
from discord.ext.commands import bot
from gems import gemsFonctions as GF
from core import gestion as ge
import gg_lib as gg
from languages import lang as lang_P


class GemsCasino(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True, aliases=['pari'])
    async def gamble(self, ctx, valeur):
        """**[bet]** | Are you a gambler's man?"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["valeur"] = valeur
        ge.socket.send_string(gg.std_send_command("gamble", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 0:
            desc = ""
            if recv['gain'] == 0:
                desc = lang_P.forge_msg(lang, "gamble", [valeur], False, 0)
            else:
                desc = "{1} {0} {2}`Gems`".format(recv['gain'], lang_P.forge_msg(lang, "gamble array", None, True), GF.build_idmoji("gem"))
            msg = discord.Embed(
                title = lang_P.forge_msg(lang, "titres", None, False, 3),
                color= 13752280,
                description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", [recv['amende']], False, 9))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "gamble", None, False, 4))
        elif recv['error'] == 3:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))

    @commands.command(pass_context=True, aliases=['machine'])
    async def slots(self, ctx, imise = None):
        """**{bet}** | Slot machine, minimum bet is 10 :gem:`gems`"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["imise"] = imise
        ge.socket.send_string(gg.std_send_command("slots", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        # await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 0:
            desc = "{0}\n{1}".format(
                lang_P.forge_msg(lang, "casino", [recv['slots']["misemax"]], False, 6),
                lang_P.forge_msg(lang, "casino", [recv['slots']["mise"]], False, 7))
            e = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 9), color= 13752280, description = desc)
            desc = ""
            for i in range(0, 9):
                if i == 3:
                    desc += "\n"
                elif i == 6:
                    desc += " :arrow_backward:\n"
                desc += GF.build_idmoji(recv['slots']["result"][i])
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 8), value=desc, inline=False)
            desc = ""
            if recv['slots']['gain'] != 0 and recv['slots']['gain'] != 1:
                if recv['slots']['prix'] > 400:
                    desc += lang_P.forge_msg(lang, "slots", [recv['slots']['prix']], False, 8)
                elif recv['slots']['prix'] > 0:
                    desc += lang_P.forge_msg(lang, "slots", [recv['slots']['prix']], False, 9)
                else:
                    desc += lang_P.forge_msg(lang, "slots", [-1*recv['slots']['prix']], False, 10)
            elif recv['slots']['gain'] == 1:
                desc += lang_P.forge_msg(lang, "slots", None, False, 11)
            else:
                desc += lang_P.forge_msg(lang, "slots", None, False, 12)
            if recv['slots']['cookies'] is not False:
                desc += lang_P.forge_msg(lang, "slots", [recv['slots']['cookies']], False, 4)
            if recv['slots']['grapes'] is not False:
                desc += lang_P.forge_msg(lang, "slots", [recv['slots']['grapes']], False, 6)
            if recv['slots']['backpack'] is not False:
                desc += lang_P.forge_msg(lang, "slots", [GF.build_idmoji("backpack"), recv['slots']['backpack']], False, 7)
            if recv['slots']['ruby'] is not False:
                desc += lang_P.forge_msg(lang, "slots", [GF.build_idmoji("ruby")], False, 1)
            if recv['slots']['beer'] is not False:
                desc += lang_P.forge_msg(lang, "slots", [ctx.author.name], False, 3)
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 3), value=desc, inline=False)
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = e)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", [recv['amende']], False, 9))
        elif recv['error'] == 3:
            await ctx.channel.send(lang_P.forge_msg(lang, "gamble", None, False, 4))

    @commands.command(pass_context=True)
    async def roulette(self, ctx, mise, valeur):
        """**[bet] [value]** | Flat roulette"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["valeur"] = valeur
        param["mise"] = mise
        ge.socket.send_string(gg.std_send_command("roulette", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 0:
            if recv['roulette']['etat'] == "Victoire":
                msgD = lang_P.forge_msg(lang, "roulette", [int(recv['roulette']['pourcentage'])], False, 1)
            elif recv['roulette']['etat'] == "Echec":
                msgD = lang_P.forge_msg(lang, "roulette", None, False, 0)
            elif recv['roulette']['etat'] == "Defaite":
                msgD = lang_P.forge_msg(lang, "roulette", [int(recv['roulette']['pourcentage'])], False, 2)

            desc = "{2}\n{1}\n{0}".format(
                lang_P.forge_msg(lang, "casino", [GF.NumberList[int(valeur)//10], GF.NumberList[int(valeur) % 10]], False, 5),
                lang_P.forge_msg(lang, "casino", [int(mise)], False, 7),
                lang_P.forge_msg(lang, "casino", [recv['roulette']["misemax"]], False, 6))
            e = discord.Embed(title = lang_P.forge_msg(lang, "casino", None, False, 0), color= 13752280, description = desc)

            desc = "| :{0}::{1}: |".format(GF.NumberList[recv['roulette']['valeurs']["VB"]//10], GF.NumberList[recv['roulette']['valeurs']["VB"] % 10])
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 1), value=desc, inline=False)

            desc = "|"
            for one in recv['roulette']['valeurs']["VM"]:
                desc += " :{0}::{1}: |".format(GF.NumberList[one//10], GF.NumberList[one % 10])
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 2), value=desc, inline=False)

            desc = "{0}\n{1}".format(msgD, lang_P.forge_msg(lang, "casino", [recv['roulette']["gain"]], False, 4))
            e.add_field(name=lang_P.forge_msg(lang, "casino", None, False, 3), value=desc, inline=False)

            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = e)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", [recv['amende']], False, 9))
        elif recv['error'] == 3:
            await ctx.channel.send(lang_P.forge_msg(lang, "gamble", None, False, 4))
        elif recv['error'] == 4:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 7))


def setup(bot):
    bot.add_cog(GemsCasino(bot))
    open("help/cogs.txt", "a").write("GemsCasino\n")
