import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

admin = 0
Inquisiteur = 1
Joueurs = 2
rolesID = [[417451897729843223],[417451897729843223,417451604141277185],[417451897729843223,417451604141277185,423606460908306433]]
guildID = [634317171496976395,640507787494948865,478003352551030796,129364058901053440]

def permission(ctx,grade):
	roles = ctx.author.roles
	for role in roles :
		if role.id in rolesID[grade] or (ctx.guild.id in guildID and role.permissions.administrator):
			return True
	return False
