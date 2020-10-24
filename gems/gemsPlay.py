import discord
from discord.ext import commands
from discord.ext.commands import bot
from gems import gemsFonctions as GF
from core import gestion as ge
import gg_lib as gg
from languages import lang as lang_P
import datetime as dt


class GemsPlay(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True, aliases=['quotidien'])
    async def daily(self, ctx):
        """Get your daily reward!"""
        # =======================================================================
        # Initialisation des variables générales de la fonction
        # =======================================================================
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("daily", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 0:
            desc = lang_P.forge_msg(lang, "daily", [GF.build_idmoji("gem")], False, 0)
            desc += lang_P.forge_msg(lang, "daily", [recv['DailyMult'], recv['bonus'], GF.build_idmoji("gem")], False, 1)
            if recv['m'] != 0:
                desc += lang_P.forge_msg(lang, "daily", [recv['DailyMult'], recv['m'], GF.build_idmoji("gem")], False, 2)
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 0), color= 13752280, description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            desc = lang_P.forge_msg(lang, "daily", [GF.build_idmoji("gem")], False, 3)
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 0), color= 13752280, description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 2:
            desc = lang_P.forge_msg(lang, "daily", [GF.build_idmoji("gem")], False, 0)
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 0), color= 13752280, description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)

    @commands.command(pass_context=True, aliases=['banque'])
    async def bank(self, ctx, ARG = None, ARG2 = None):
        """**[bal/add/saving] [name/number]** | Savings account"""
        # =======================================================================
        # Initialistation des variables générales de la fonction
        # =======================================================================
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["ARG"] = ARG
        param["ARG2"] = ARG2

        ge.socket.send_string(gg.std_send_command("bank", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 405:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 6))
        elif recv['error'] == 0:
            if recv['type'] == "bal":
                title = lang_P.forge_msg(lang, "bank", [recv['name']], False, 15)
                # title = "Compte épargne de {}".format(ctx.author.name)
                msg = discord.Embed(title = title, color= 13752280, description = "", timestamp=dt.datetime.now())
                msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

                desc = "{0} / {1} :gem:`gems`\n".format(recv['BankSolde'], recv['BankSMax'])
                PCcharacter = "{}".format(recv['%'])
                pc = ""
                for i in range(0, 4):
                    pc += PCcharacter[i]
                desc += "\n{0}\n".format(lang_P.forge_msg(lang, "bank", [pc], False, 14))
                msg.add_field(name="Balance", value=desc, inline=False)

                desc = lang_P.forge_msg(lang, "bank", None, False, 0)
                desc += lang_P.forge_msg(lang, "bank", [GF.build_idmoji("gem")], False, 1)
                desc += lang_P.forge_msg(lang, "bank", None, False, 2)
                desc += lang_P.forge_msg(lang, "bank", ["bank", GF.build_idmoji("bank")], False, 3)
                msg.add_field(name="Commandes", value=desc, inline=False)
                await ctx.channel.send(embed = msg)
            elif recv['type'] == "add":
                desc = ""
                if recv['BankSNew'] >= recv['BankSMax']:
                    desc = lang_P.forge_msg(lang, "bank", [recv['BankSMax'], GF.build_idmoji("gem")], False, 4)
                desc += lang_P.forge_msg(lang, "bank", [recv['BankSAdd'], GF.build_idmoji("gem")], False, 6)
                desc += lang_P.forge_msg(lang, "bank", [recv['BankSNew'], GF.build_idmoji("gem")], False, 7)
                msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 4), color= 13752280, description = desc, timestamp=dt.datetime.now())
                msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed = msg)
            elif recv['type'] == "saving":
                desc = lang_P.forge_msg(lang, "bank", [int(recv['BankSAdd']), GF.build_idmoji("gem")], False, 10)
                if recv['BankSNew'] >= recv['BankSMax']:
                    desc += lang_P.forge_msg(lang, "bank", [recv['BankSMax'], GF.build_idmoji("gem")], False, 11)
                desc += lang_P.forge_msg(lang, "bank", [recv['BankSNew'], GF.build_idmoji("gem")], False, 7)
                msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 5), color= 13752280, description = desc, timestamp=dt.datetime.now())
                msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "couldown", [str(recv['couldown'])]))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 1))
        elif recv['error'] == 3:
            await ctx.channel.send(lang_P.forge_msg(lang, "bank", [GF.build_idmoji("gem")], False, 9))
        elif recv['error'] == 4:
            await ctx.channel.send(lang_P.forge_msg(lang, "bank", [GF.build_idmoji("gem")], False, 8))
        elif recv['error'] == 5:
            await ctx.channel.send(lang_P.forge_msg(lang, "bank", [recv['BankSolde'], GF.build_idmoji("gem")], False, 13))
        elif recv['error'] == 6:
            await ctx.channel.send(lang_P.forge_msg(lang, "bank", [recv['time'][0], recv['time'][1], recv['time'][2]], False, 12))

    @commands.command(pass_context=True, aliases=['vol', 'voler'])
    async def stealing(self, ctx, name=None):
        """**{name}** | Steal :gem:`gems` from other players!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["name"] = name
        ge.socket.send_string(gg.std_send_command("stealing", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        elif recv['error'] == 405:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 6))
        elif recv['error'] == -1:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 4))
        elif recv['error'] == 0:
            if recv['result']['DiscordCop']:
                desc = lang_P.forge_msg(lang, "DiscordCop Arrestation", [recv['result']['perte'], GF.build_idmoji("gem")], False, 0)
            else:
                desc = lang_P.forge_msg(lang, "stealing", [recv['result']['gain'], recv['nameVol'], GF.build_idmoji("gem")], False, 1)
            msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 1), color= 13752280, description = desc)
            msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.channel.send(embed = msg)
        elif recv['error'] == 1:
            await ctx.channel.send(lang_P.forge_msg(lang, "stealing", [recv['time'][0], recv['time'][1], recv['time'][2], GF.build_idmoji("gem")], False, 0))
        elif recv['error'] == 2:
            await ctx.channel.send(lang_P.forge_msg(lang, "stealing", [GF.build_idmoji("gem")], False, 4))
        elif recv['error'] == 3:
            await ctx.channel.send(lang_P.forge_msg(lang, "stealing", [GF.build_idmoji("gem")], False, 3))
        elif recv['error'] == 4:
            await ctx.channel.send(lang_P.forge_msg(lang, "stealing", [GF.build_idmoji("gem")], False, 2))

    @commands.command(pass_context=True)
    async def crime(self, ctx):
        """Commit a crime and earn :gem:`gems` Beware of DiscordCop!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("crime", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        # desc = GF.msg_recv()
        # lang = desc["lang"]
        # if desc["type"] == "OK":
        #     msg = discord.Embed(title = lang_P.forge_msg(lang, "titres", None, False, 2), color= 13752280, description = desc["desc"])
        #     msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #     await ctx.channel.send(embed = msg)
        # else:
        #     await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True, aliases=['m', 'miner'])
    async def mine(self, ctx):
        """Let's mine, mates!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("mine", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        # desc = GF.msg_recv()
        # lang = desc["lang"]
        # if desc["type"] == "OK":
        #     msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 6), color= 13752280, description = desc["desc"])
        #     msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #     await ctx.channel.send(embed = msg)
        # else:
        #     await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True, aliases=['d', 'creuser'])
    async def dig(self, ctx):
        """Let's dig, mates!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("dig", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        # desc = GF.msg_recv()
        # lang = desc["lang"]
        # if desc["type"] == "OK":
        #     msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 8), color= 13752280, description = desc["desc"])
        #     msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #     await ctx.channel.send(embed = msg)
        # else:
        #     await ctx.channel.send(desc["desc"])

    @commands.command(pass_context=True, aliases=['f', 'peche', 'pêche'])
    async def fish(self, ctx):
        """Let us sin mates!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("fish", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        # desc = GF.msg_recv()
        # lang = desc["lang"]
        # if desc["type"] == "OK":
        #     msg = discord.Embed(title = lang_P.forge_msg(lang, "stats", None, False, 7), color= 13752280, description = desc["desc"])
        #     msg.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #     await ctx.channel.send(embed = msg)
        # else:
        #     await ctx.channel.send(desc["desc"])

    # @commands.command(pass_context=True, aliases=['ouvrir'])
    # async def open(self, ctx, name = None):
    #     """**[name]** | Loot Box Opening"""
    #     ID = ctx.author.id
    #     param = dict()
    #     param["ID"] = ID
    #     param["name"] = name
    #     ge.socket.send_string(gg.std_send_command("open", ID, ge.name_pl, param))
    #     recv = GF.msg_recv()
    #     await ctx.channel.send(recv)
    #     lang = recv['lang']
    #     if recv['error'] == 100:
    #         await ctx.channel.send(recv['etat'])
    #     elif recv['error'] == 404:
    #         await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        # msg = GF.msg_recv()
        #
        # if msg["type"] == "OK":
        #     titre = msg["titre"]
        #     desc = msg["desc"]
        #     MsgEmbed = discord.Embed(title = "Loot Box | {}".format(titre), color= 13752280, description = desc)
        #     MsgEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        #     await ctx.channel.send(embed = MsgEmbed)
        # else:
        #     await ctx.channel.send(msg["desc"])

    @commands.command(pass_context=True, aliases=['serre'])
    async def hothouse(self, ctx, item = None):
        """**{seed/pumpkin}** | Let's plant mates!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["item"] = item
        ge.socket.send_string(gg.std_send_command("hothouse", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        # msg = GF.msg_recv()
        #
        # if msg["type"] == "OK":
        #     lang = msg["lang"]
        #     nbplanting = msg["nboutil"]
        #     desc = lang_P.forge_msg(lang, "hothouse", [GF.get_idmoji("seed")], False, 0)
        #     titre = lang_P.forge_msg(lang, "hothouse", None, False, 1)
        #     MsgEmbed = discord.Embed(title = titre, color= 6466585, description = desc)
        #     k = len(msg) - 3
        #     i = 1
        #     while i <= k:
        #         j = i-1
        #         if j % 10 == 0 and j != nbplanting and j != 0:
        #             if j // 10 == 1:
        #                 await ctx.channel.send(embed = MsgEmbed)
        #             else:
        #                 await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
        #             MsgEmbed = discord.Embed(title = lang_P.forge_msg(lang, "hothouse", [int((j//10)+1)], False, 2), color= 6466585, description = "Voici tes plantation.")
        #             MsgEmbed.add_field(name=lang_P.forge_msg(lang, "hothouse", [i], False, 3), value=msg[i], inline=False)
        #         else:
        #             MsgEmbed.add_field(name=lang_P.forge_msg(lang, "hothouse", [i], False, 3), value=msg[i], inline=False)
        #         if lang_P.forge_msg(lang, "production") in msg[i]:
        #             i = k+1
        #         else:
        #             i += 1
        #     await ctx.channel.send(embed = MsgEmbed)
        # else:
        #     await ctx.channel.send(msg["desc"])

    @commands.command(pass_context=True, aliases=['cave'])
    async def ferment(self, ctx, item = None):
        """**{grapes/wheat}** | Fermentation winery. Unlimited alcohol!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["item"] = item
        ge.socket.send_string(gg.std_send_command("ferment", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        # msg = GF.msg_recv()
        #
        # if msg["type"] == "OK":
        #     lang = msg["lang"]
        #     nbplanting = msg["nboutil"]
        #     desc = lang_P.forge_msg(lang, "ferment", None, False, 0)
        #     titre = lang_P.forge_msg(lang, "ferment", None, False, 1)
        #     MsgEmbed = discord.Embed(title = titre, color= 9633863, description = desc)
        #     k = len(msg) - 3
        #     i = 1
        #     while i <= k:
        #         j = i-1
        #         if j % 10 == 0 and j != nbplanting and j != 0:
        #             if j // 10 == 1:
        #                 await ctx.channel.send(embed = MsgEmbed)
        #             else:
        #                 await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
        #             MsgEmbed = discord.Embed(title = lang_P.forge_msg(lang, "ferment", [int((j//10)+1)], False, 2), color= 9633863, description = "Voici vos barrils.")
        #             MsgEmbed.add_field(name=lang_P.forge_msg(lang, "ferment", [i], False, 3), value=msg[i], inline=False)
        #         else:
        #             MsgEmbed.add_field(name=lang_P.forge_msg(lang, "ferment", [i], False, 3), value=msg[i], inline=False)
        #         if lang_P.forge_msg(lang, "production") in msg[i]:
        #             i = k+1
        #         else:
        #             i += 1
        #     await ctx.channel.send(embed = MsgEmbed)
        # else:
        #     await ctx.channel.send(msg["desc"])

    @commands.command(pass_context=True, aliases=['cuisine'])
    async def cooking(self, ctx, item = None):
        """**{potato/pumpkin/chocolate}** | Let's cook together!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["item"] = item
        ge.socket.send_string(gg.std_send_command("cooking", ID, ge.name_pl, param))
        recv = GF.msg_recv()
        await ctx.channel.send(recv)
        lang = recv['lang']
        if recv['error'] == 100:
            await ctx.channel.send(recv['etat'])
        elif recv['error'] == 404:
            await ctx.channel.send(lang_P.forge_msg(lang, "WarningMsg", None, False, 0))
        # msg = GF.msg_recv()
        #
        # if msg["type"] == "OK":
        #     lang = msg["lang"]
        #     nbplanting = msg["nboutil"]
        #     desc = lang_P.forge_msg(lang, "cooking", [GF.get_idmoji("fries")], False, 0)
        #     titre = lang_P.forge_msg(lang, "cooking", None, False, 1)
        #     MsgEmbed = discord.Embed(title = titre, color= 14902529, description = desc)
        #     k = len(msg) - 3
        #     i = 1
        #     while i <= k:
        #         j = i-1
        #         if j % 10 == 0 and j != nbplanting and j != 0:
        #             if j // 10 == 1:
        #                 await ctx.channel.send(embed = MsgEmbed)
        #             else:
        #                 await ctx.channel.send(embed = MsgEmbed, delete_after = 90)
        #             MsgEmbed = discord.Embed(title = lang_P.forge_msg(lang, "cooking", [int((j//10)+1)], False, 2), color= 14902529, description = "Voici vos fours.")
        #             MsgEmbed.add_field(name=lang_P.forge_msg(lang, "cooking", [i], False, 3), value=msg[i], inline=False)
        #         else:
        #             MsgEmbed.add_field(name=lang_P.forge_msg(lang, "cooking", [i], False, 3), value=msg[i], inline=False)
        #         if lang_P.forge_msg(lang, "production") in msg[i]:
        #             i = k+1
        #         else:
        #             i += 1
        #     await ctx.channel.send(embed = MsgEmbed)
        # else:
        #     await ctx.channel.send(msg["desc"])


def setup(bot):
    bot.add_cog(GemsPlay(bot))
    open("help/cogs.txt", "a").write("GemsPlay\n")
