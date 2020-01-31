import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
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
        ge.socket.send_string(gg.std_send_command("crime", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def gamble(self, ctx, valeur):
        """**[valeur]** | Avez vous l'ame d'un parieur ?"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
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
        ge.socket.send_string(gg.std_send_command("mine", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def dig(self, ctx):
        """Creusons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("dig", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def fish(self, ctx):
        """Péchons compagnons !!"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        ge.socket.send_string(gg.std_send_command("fish", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    @commands.command(pass_context=True)
    async def slots(self, ctx, imise = None):
        """**[mise]** | La machine à sous, la mise minimum est de 10 :gem:`gems`"""
        ID = ctx.author.id
        param = dict()
        param["ID"] = ID
        param["imise"] = imise
        ge.socket.send_string(gg.std_send_command("slots", ID, ge.name_pl, param))
        msg = GF.msg_recv()
        await ctx.channel.send(msg[1])

    #
    #
    #
    # @commands.command(pass_context=True)
    # async def hothouse(self, ctx, fct = None, arg = None, arg2 = None):
    #     """**[harvest / plant]** {_n° plantation / item à planter_} | Plantons compagnons !!"""
    #     ID = ctx.author.id
    #     maxplanting = 50
    #     if sql.spam(ID,GF.couldown_4s, "hothouse", "gems"):
    #         nbplanting = int(sql.valueAtNumber(ID, "planting_plan", "inventory")) + 1
    #         if nbplanting >= maxplanting:
    #             nbplanting = maxplanting
    #         msg = discord.Embed(title = "La serre",color= 6466585, description = "Voici tes plantations.\nUtilisé `hothouse plant seed` pour planter une <:gem_seed:{0}>`seed`".format(GF.get_idmoji("seed")))
    #         desc = ""
    #         i = 1
    #         sql.updateComTime(ID, "hothouse", "gems")
    #         if fct == None or fct == "harvest":
    #             if  arg != None:
    #                 if int(arg) <= nbplanting:
    #                     nbplanting = int(arg)
    #                 else:
    #                     msg = "Tu n'as pas assez de plantations ou cette plantation n'est pas disponible!"
    #                     await ctx.channel.send(msg)
    #                     return 404
    #             while i <= nbplanting:
    #                 data = []
    #                 valuePlanting = sql.valueAt(ID, i, "hothouse")
    #                 if valuePlanting != 0:
    #                     valueTime = float(valuePlanting[0])
    #                     valueItem = valuePlanting[1]
    #                 else:
    #                     valueTime = 0
    #                     valueItem = ""
    #                 if valueItem == "cacao":
    #                     couldown = GF.couldown_4h
    #                 else:
    #                     couldown = GF.couldown_6h
    #                 if valueTime == 0:
    #                     desc = "Cette plantation est vide!"
    #                 else:
    #                     PlantingTime = float(valueTime)
    #                     InstantTime = t.time()
    #                     time = PlantingTime - (InstantTime-couldown)
    #                     if time <= 0:
    #                         De = r.randint(1,15)
    #                         jour = dt.date.today()
    #                         if valueItem == "seed" or valueItem == "":
    #                             if (jour.month == 10 and jour.day >= 23) or (jour.month == 11 and jour.day <= 10): #Special Halloween
    #                                 if De <= 2:
    #                                     nbHarvest = r.randint(1, 2)
    #                                     item = "oak"
    #                                 elif De > 2 and De <= 7:
    #                                     nbHarvest = r.randint(2, 4)
    #                                     item = "pumpkin"
    #                                 elif De > 7 and De <= 10:
    #                                     nbHarvest = r.randint(1, 2)
    #                                     item = "spruce"
    #                                 elif De > 10 and De <= 12:
    #                                     nbHarvest = r.randint(1, 2)
    #                                     item = "palm"
    #                                 elif De > 12 and De <= 14:
    #                                     nbHarvest = r.randint(4,10)
    #                                     item = "wheat"
    #                                 elif De > 14:
    #                                     nbHarvest = r.randint(6,12)
    #                                     item = "grapes"
    #                             else:
    #                                 if De <= 5:
    #                                     nbHarvest = r.randint(1, 2)
    #                                     item = "oak"
    #                                 elif De > 5 and De <= 9:
    #                                     nbHarvest = r.randint(1, 2)
    #                                     item = "spruce"
    #                                 elif De > 9 and De <= 12:
    #                                     nbHarvest = r.randint(1, 2)
    #                                     item = "palm"
    #                                 elif De > 12 and De <= 14:
    #                                     nbHarvest = r.randint(4,10)
    #                                     item = "wheat"
    #                                 elif De > 14:
    #                                     nbHarvest = r.randint(6,12)
    #                                     item = "grapes"
    #                         elif valueItem == "cacao":
    #                             nbHarvest = r.randint(1,4)
    #                             item = "chocolate"
    #                         data = []
    #                         data.append(0)
    #                         data.append("")
    #                         sql.add(ID, item, nbHarvest, "inventory")
    #                         sql.updateField(ID, i, data, "hothouse")
    #                         if item == "grapes":
    #                             desc = "Ta plantation à fini de pousser, en la coupant tu gagnes {2} :{1}:`{1}`".format(GF.get_idmoji(item), item, nbHarvest)
    #                         else:
    #                             desc = "Ta plantation à fini de pousser, en la coupant tu gagnes {2} <:gem_{1}:{0}>`{1}`".format(GF.get_idmoji(item), item, nbHarvest)
    #                         lvl.addxp(ID, 1, "gems")
    #                         if i > 1:
    #                             if sql.valueAtNumber(ID, "planting_plan", "inventory") > 0:
    #                                 if sql.valueAt(ID, "planting_plan", "durability") == 0:
    #                                     for c in GF.objetOutil:
    #                                         if c.nom == "planting_plan":
    #                                             sql.add(ID, "planting_plan", c.durabilite, "durability")
    #                                 sql.add(ID, "planting_plan", -1, "durability")
    #                                 if sql.valueAt(ID, "planting_plan", "durability")[0] <= 0:
    #                                     for c in GF.objetOutil:
    #                                         if c.nom == "planting_plan":
    #                                             sql.add(ID, "planting_plan", c.durabilite, "durability")
    #                                     sql.add(ID, "planting_plan", -1, "inventory")
    #
    #                     else:
    #                         timeH = int(time / 60 / 60)
    #                         time = time - timeH * 3600
    #                         timeM = int(time / 60)
    #                         timeS = int(time - timeM * 60)
    #                         desc = "<:gem_{3}:{4}>`{3}` | Ta plantation aura fini de pousser dans :clock2:`{0}h {1}m {2}s`".format(timeH,timeM,timeS,valueItem,GF.get_idmoji(valueItem))
    #                 if i % 10 == 0 and i != nbplanting:
    #                     if i // 10 == 1:
    #                         await ctx.channel.send(embed = msg)
    #                     else:
    #                         await ctx.channel.send(embed = msg, delete_after = 90)
    #                     msg = discord.Embed(title = "La serre | Partie {}".format((i//10)+1),color= 6466585, description = "Voici tes plantation.")
    #                     msg.add_field(name="Plantation n°{}".format(i), value=desc, inline=False)
    #                 else:
    #                     msg.add_field(name="Plantation n°{}".format(i), value=desc, inline=False)
    #                 i += 1
    #         elif fct == "plant":
    #             if sql.valueAtNumber(wel.idBaBot, "DailyMult", "daily") == 1:
    #                 await ctx.channel.send("Plantations endommagées! Un violent orage :cloud_lightning: à détruit tes plantations\nTes plantations seront réparrées au plus vite")
    #                 return False
    #             if arg != "seed" and arg != "cacao":
    #                 arg = "seed"
    #             if arg2 != None:
    #                 try:
    #                     arg2 = int(arg2)
    #                 except:
    #                     return 404
    #                 if arg2 > nbplanting:
    #                     msg = "Tu n'as pas assez de plantations ou cette plantation n'est pas disponible!"
    #                     await ctx.channel.send(msg)
    #                     return 404
    #                 elif int(arg2) < 0:
    #                     sql.addGems(ID, -100)
    #                     lvl.addxp(ID, -10, "gems")
    #                     msg = ":no_entry: Anti-cheat! Je vous met un amende de 100 :gem:`gems` pour avoir essayé de tricher !"
    #                     slq.add(ID, "DiscordCop Amende", 1, "statgems")
    #                     await ctx.channel.send(msg)
    #                     return "anticheat"
    #                 data = []
    #                 valuePlanting = sql.valueAt(ID, i, "hothouse")
    #                 if valuePlanting != 0:
    #                     valueTime = float(valuePlanting[0])
    #                     valueItem = valuePlanting[1]
    #                 else:
    #                     valueTime = 0
    #                     valueItem = ""
    #                 if valueItem == "cacao":
    #                     couldown = "4h"
    #                 else:
    #                     couldown = "6h"
    #                 if valueTime == 0:
    #                     PlantingItemValue = sql.valueAtNumber(ID, arg, "inventory")
    #                     if PlantingItemValue >= 1:
    #                         data = []
    #                         data.append(str(t.time()))
    #                         data.append(arg)
    #                         sql.add(ID, arg2, data, "hothouse")
    #                         sql.add(ID, arg, -1, "inventory")
    #                         desc = "<:gem_{0}:{1}>`{0}` plantée. Elle aura fini de pousser dans :clock2:`{2}`".format(arg, GF.get_idmoji(arg), couldown)
    #                     else:
    #                         desc = "Tu n'as pas de <:gem_{0}:{1}>`{0}` à planter dans ton inventaire".format(arg, GF.get_idmoji(arg))
    #                 else:
    #                     desc = "Tu as déjà planté une <:gem_{0}:{1}>`{0}` dans cette plantation".format(valueItem, GF.get_idmoji(valueItem))
    #                 msg.add_field(name="Plantation n°{}".format(arg2), value=desc, inline=False)
    #             else:
    #                 j = 0
    #                 while i <= nbplanting:
    #                     data = []
    #                     valuePlanting = sql.valueAt(ID, i, "hothouse")
    #                     if valuePlanting != 0:
    #                         valueTime = float(valuePlanting[0])
    #                         valueItem = valuePlanting[1]
    #                     else:
    #                         valueTime = 0
    #                         valueItem = ""
    #                     PlantingItemValue = sql.valueAtNumber(ID, arg, "inventory")
    #                     if valueItem == "cacao" or (valueItem == "" and arg == "cacao"):
    #                         couldown = "4h"
    #                     else:
    #                         couldown = "6h"
    #                     if valueTime == 0:
    #                         if PlantingItemValue >= 1:
    #                             data = []
    #                             data.append(str(t.time()))
    #                             data.append(arg)
    #                             sql.add(ID, i, data, "hothouse")
    #                             sql.add(ID, arg, -1, "inventory")
    #                             desc = "<:gem_{0}:{1}>`{0}` plantée. Elle aura fini de pousser dans :clock2:`{2}`".format(arg, GF.get_idmoji(arg), couldown)
    #                         else:
    #                             desc = "Tu n'as pas de <:gem_{0}:{1}>`{0}` à planter dans ton inventaire".format(arg, GF.get_idmoji(arg))
    #                             if j == 0:
    #                                 j = -1
    #                                 if arg == "seed":
    #                                     arg = "cacao"
    #                                 else:
    #                                     arg = "seed"
    #                             if i > 15 and j == 1:
    #                                 await ctx.channel.send(embed = msg)
    #                                 await ctx.channel.send(desc)
    #                                 return 0
    #                     else:
    #                         desc = "Tu as déjà planté une <:gem_{0}:{1}>`{0}` dans cette plantation".format(valueItem, GF.get_idmoji(valueItem))
    #                     if i % 10 == 0 and i != nbplanting:
    #                         if i // 10 == 1:
    #                             await ctx.channel.send(embed = msg)
    #                         else:
    #                             await ctx.channel.send(embed = msg, delete_after = 90)
    #                         msg = discord.Embed(title = "La serre | Partie {}".format((i//10)+1),color= 6466585, description = "Voici vos plantations.".format(GF.get_idmoji("seed")))
    #                         msg.add_field(name="Plantation n°{}".format(i), value=desc, inline=False)
    #                     else:
    #                         msg.add_field(name="Plantation n°{}".format(i), value=desc, inline=False)
    #                     if j == -1:
    #                         j = 1
    #                     else:
    #                         i += 1
    #         else:
    #             msg = "Fonction inconnu"
    #             await ctx.channel.send(msg)
    #             return False
    #         if nbplanting // 10 == 0:
    #             await ctx.channel.send(embed = msg)
    #         else:
    #             await ctx.channel.send(embed = msg, delete_after = 90)
    #     else:
    #         msg = "Il faut attendre "+str(GF.couldown_4s)+" secondes entre chaque commande !"
    #         await ctx.channel.send(msg)
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
    #
    #
    #
    # @commands.command(pass_context=True)
    # async def boxes(self, ctx, fct = None, name = None):
    #     """**open [nom]** | Ouverture de Loot Box"""
    #     ID = ctx.author.id
    #
    #     if fct == "open":
    #         if name != None:
    #             for lootbox in GF.objetBox:
    #                 if name == "lootbox_{}".format(lootbox.nom):
    #                     name = lootbox.nom
    #             if sql.valueAtNumber(ID, "lootbox_{}".format(name), "inventory") > 0:
    #                 if name == "gift":
    #                     for lootbox in GF.objetBox:
    #                         if name == lootbox.nom:
    #                             titre = lootbox.titre
    #                             gain = r.randint(lootbox.min, lootbox.max)
    #                             sql.add(ID, "lootbox_{}".format(lootbox.nom), -1, "inventory")
    #
    #                             sql.addGems(ID, gain)
    #                             desc = "{} :gem:`gems`\n".format(gain)
    #                             if r.randint(0,6) == 0:
    #                                 nb = r.randint(-2, 3)
    #                                 if nb < 1:
    #                                     nb = 1
    #                                 sql.addSpinelles(ID, nb)
    #                                 desc += "{nombre} <:spinelle:{idmoji}>`spinelle`\n".format(idmoji=GF.get_idmoji("spinelle"), nombre=nb)
    #                             for x in GF.objetItem:
    #                                 if r.randint(0,10) <= 1:
    #                                     if x.nom == "hyperpack":
    #                                         nbgain = 1
    #                                     else:
    #                                         nbgain = r.randint(3, 8)
    #                                     sql.add(ID, x.nom, nbgain, "inventory")
    #                                     if x.type != "emoji":
    #                                         desc += "\n<:gem_{0}:{2}>`{0}` x{1}".format(x.nom, nbgain, GF.get_idmoji(x.nom))
    #                                     else:
    #                                         desc += "\n:{0}:`{0}` x{1}".format(x.nom, nbgain)
    #                             msg = discord.Embed(title = "Loot Box | {}".format(titre),color= 13752280, description = desc)
    #                             print("Gems >> {} a ouvert une Loot Box de Noel".format(ctx.author.name))
    #                             await ctx.channel.send(embed = msg)
    #                             return True
    #                 elif name == "gift_heart":
    #                     for lootbox in GF.objetBox:
    #                         if name == lootbox.nom:
    #                             titre = lootbox.titre
    #                             for x in GF.objetItem:
    #                                 if r.randint(0,15) >= 14:
    #                                     if x.nom == "hyperpack":
    #                                         nbgain = r.randint(1,2)
    #                                     else:
    #                                         nbgain = r.randint(4, 10)
    #                                     sql.add(ID, x.nom, nbgain, "inventory")
    #                                     if x.type != "emoji":
    #                                         desc += "\n<:gem_{0}:{2}>`{0}` x{1}".format(x.nom, nbgain, GF.get_idmoji(x.nom))
    #                                     else:
    #                                         desc += "\n:{0}:`{0}` x{1}".format(x.nom, nbgain)
    #                             msg = discord.Embed(title = "Loot Box | {}".format(titre),color= 13752280, description = desc)
    #                             print("Gems >> {} a ouvert une Loot Box de la Saint Valentin".format(ctx.author.name))
    #                             await ctx.channel.send(embed = msg)
    #                             return True
    #                 else:
    #                     for lootbox in GF.objetBox:
    #                         if name == lootbox.nom:
    #                             gain = r.randint(lootbox.min, lootbox.max)
    #                             titre = lootbox.titre
    #
    #                             sql.addGems(ID, gain)
    #                             sql.add(ID, "lootbox_{}".format(lootbox.nom), -1, "inventory")
    #                             desc = "{} :gem:`gems`".format(gain)
    #                             msg = discord.Embed(title = "Loot Box | {}".format(titre),color= 13752280, description = desc)
    #                             print("Gems >> {} a ouvert une Loot Box".format(ctx.author.name))
    #                             await ctx.channel.send(embed = msg)
    #                             return True
    #
    #                 await ctx.channel.send("Cette box n'existe pas!")
    #                 return False
    #             else:
    #                 msg = "Tu ne possèdes pas cette Loot Box"
    #         else:
    #             msg = "Commande `boxes open` incomplète"
    #     elif fct == None:
    #         msg = "Commande `boxes` incomplète"
    #     else:
    #         msg = "Commande `boxes` invalide"
    #     await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(GemsPlay(bot))
    open("help/cogs.txt","a").write("GemsPlay\n")
