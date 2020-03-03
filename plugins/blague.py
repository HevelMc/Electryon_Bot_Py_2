import discord
from discord.ext import commands
from discord.ext.commands import Bot
from plugins.divers import Random

import os
import requests
import random

PREFIX = os.getenv('BOT_PREFIX')

with open('data/urlemojis.txt') as f:
    URLEMOJIS = f.read().splitlines()

class Blague(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def run_blague(self, message, author, type):
        headers = {'Authorization': 'eBSuaR.-o5NB_fdzdslzj.tC2O.7CWe4gi-ND4rwCA0-PhjlpuUMVbiSGZB5j7ce'}
        if type == "joke":
            r = requests.get(url = "https://blague.xyz/api/joke/random", headers=headers)
        elif type == "vdm":
            r = requests.get(url = "https://blague.xyz/api/vdm/random", headers=headers)
        if r.status_code == 200:
            await message.channel.send("💚 Le bot s'est correctement connecté à l'API ! 💚")
            rjson = r.json()
        else:
            await message.channel.send(":name_badge: Désolé mais l'API ne répond pas. Veuillez patienter le temps de la réparation. :name_badge:")
            return

        if type == "joke":
            question = rjson["joke"]["question"]
            response = rjson["joke"]["answer"]
            id = int(rjson["joke"]["id"])
            embed=discord.Embed(title=f"{author.name} a réclamé une blague", color=random.randint(0, 0xffffff))
            embed.set_thumbnail(url=URLEMOJIS[random.randrange(len(URLEMOJIS)) - 1])
            embed.add_field(name="Question", value=f"**{question}**", inline=False)
            embed.add_field(name="Réponse", value=f"**{response}**", inline=True)
            embed.set_footer(text=f"Blague n°{id}")
        if type == "vdm":
            content = rjson["vdm"]["content"]
            id = int(rjson["vdm"]["id"])
            embed=discord.Embed(title=f"{author.name} a réclamé une VDM", color=random.randint(0, 0xffffff))
            embed.set_thumbnail(url=URLEMOJIS[random.randrange(len(URLEMOJIS)) - 1])
            embed.add_field(name="Vie de Merde :", value=f"**{content}**", inline=True)
            embed.set_footer(text=f"VDM n°{id}")

        msg = await message.channel.send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👌')
        await msg.add_reaction('👎')
        await msg.add_reaction('🔂')


    @commands.command(help='Le bot te raconte une blague aléatoire.')
    async def blague(self, ctx):
        await self.run_blague(ctx.message, ctx.author, "joke")
    
    @commands.command(help='Le bot te raconte une Vie de Merde (VDM) / FuckMyLife (FML) aléatoire.')
    async def vdm(self, ctx):
        await self.run_blague(ctx.message, ctx.author, "vdm")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if reaction.emoji == '🔂':
            message = reaction.message
            if "Blague " in str(message.embeds[0].footer):
                await self.run_blague(message, user, "joke")
            if "VDM " in str(message.embeds[0].footer):
                await self.run_blague(message, user, "vdm")
            if f"{PREFIX}fox" in str(message.embeds[0].footer):
                await Random(self.client).animals(name="fox", message=message)
            if f"{PREFIX}cat" in str(message.embeds[0].footer):
                await Random(self.client).animals(name="cat", message=message)
            if f"{PREFIX}dog" in str(message.embeds[0].footer):
                await Random(self.client).animals(name="dog", message=message)
            await reaction.remove(user)
            await reaction.remove(self.client.user)

def setup(bot):
    bot.add_cog(Blague(bot))