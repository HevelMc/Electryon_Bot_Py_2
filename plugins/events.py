import discord
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

import json

with open('data/events.json', encoding='utf-8') as f:
    EVENTS = json.load(f)

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Ajoute un évènement dans la liste des events.')
    @commands.has_permissions(administrator=True)
    async def addevent(self, ctx, id):
        channel = self.client.get_channel(647431339464851466)

        if EVENTS[id]:
            color = discord.Colour(int(EVENTS[id]['color'], 16))

            desc = EVENTS[id]['description']

            embed=discord.Embed(title=f"Un nouvel évènement à été planifié !", description=f"**Participez à l’évènement `{EVENTS[id]['title']}` !**\n\n__**Description de l'évènement** :__\n*{desc}*\n\n__S'inscrire en repondant au formulaire:__ **[ICI]({EVENTS[id]['url_form']})**", color=color)
            embed.set_thumbnail(url=EVENTS[id]['url_image'])
            embed.add_field(name="Date", value=f"le **{EVENTS[id]['date']}** à **{EVENTS[id]['heure']}**", inline=True)
            embed.add_field(name="Fin de l'inscription", value=f"le **{EVENTS[id]['fin_inscription']}**", inline=True)
            embed.add_field(name="Joueurs", value=f"**?** / **{EVENTS[id]['max_players']}**", inline=True)
            embed.set_footer(text=f"Évènement n°{id}.")
            await channel.send(embed=embed)
        else:
            await ctx.send(f"L'évènement n°{id} n'existe pas.")

    @commands.command(help='Déplace un évènement dans la liste des events archivés.')
    @commands.has_permissions(administrator=True)
    async def archiveevent(self, ctx, id):
        annonce_channel = self.client.get_channel(647431339464851466)
        archives_channel = self.client.get_channel(647431386428604418)

        message = await annonce_channel.fetch_message(int(id))

        if message:
            embed = message.embeds[0]
            await message.delete()
            embed.title = f"**Message Archivé :**"
            newmessage = await archives_channel.send(embed=embed)
            await ctx.send(":green_circle: Message déplacé !")
        else:
            await ctx.send(f":red_circle: Message introuvable, l'ID est probablement invalide ou le message n'appartient pas au channel <#{annonce_channel.id}> !")


def setup(bot):
    bot.add_cog(Events(bot))