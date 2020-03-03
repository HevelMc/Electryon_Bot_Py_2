import discord
from discord.ext import commands
from discord.ext.commands import Bot

import os

PREFIX = os.getenv('BOT_PREFIX')


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Affiche le message d'aide.")
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self, ctx, *cog):
        try:
            if not cog:
                halp = discord.Embed(title='Liste des catégories et commandes non catégorisées',
                                     description=f'Utilisez `{PREFIX}help <catégorie>` pour en savoir plus sur une catégorie !', color=0x0080ff)
                cogs_desc = ''
                for x in self.client.cogs:
                    cogs_desc += ('+ {}'.format(x)+'\n')
                halp.add_field(
                    name='Catégories', value=cogs_desc[0:len(cogs_desc)-1], inline=False)
                cmds_desc = ''
                for y in self.client.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name, y.help)+'\n')
                halp.add_field(name='Commandes non catégorisées',
                               value=cmds_desc[0:len(cmds_desc)-1], inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('', embed=halp)
                for x in self.client.cogs:
                    await self.helpcat(ctx.message, x)
            else:
                await self.helpcat(ctx.message, cog[0])
        except Exception as e:
            await ctx.message.channel.send('erreur = ' + str(e))

    async def helpcat(self, message, *cog):
        if len(cog) > 1:
            halp = discord.Embed(
                title='Erreur!', description='Il y a beaucoup trop de catégories !', color=discord.Color.red())
            await message.author.send('', embed=halp)
        else:
            found = False
            for x in self.client.cogs:
                for y in cog:
                    if x == y:
                        halp = discord.Embed(
                            title=cog[0]+' - Liste des commandes', description=self.client.cogs[cog[0]].__doc__, color=0xffff80)
                        for c in self.client.get_cog(y).get_commands():
                            if not c.hidden:
                                halp.add_field(
                                    name=c.name, value=c.help, inline=False)
                        found = True
            if not found:
                halp = discord.Embed(
                    title='Erreur!', description='Je ne connais pas la catégorie: "'+cog[0]+'".', color=discord.Color.red())
            else:
                await message.add_reaction(emoji='✉')
            await message.author.send('', embed=halp)


def setup(bot):
    bot.add_cog(Help(bot))
