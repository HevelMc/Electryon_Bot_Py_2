import discord
from discord.ext import commands
from discord.ext.commands import Bot
from plugins.divers import Random

import os
import requests
import random

from datetime import datetime

class News(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def run_news(self, message):
        url = ('http://newsapi.org/v2/top-headlines?'
            'country=fr&'
            'apiKey=d2da2456241e4edc922258f88ceffcca')
        response = requests.get(url)
        r_json = json_object = response.json()

        Hours = [7, 9, 11, 13, 15, 17, 19, 21]

        n = 0
        for article in r_json.get("articles"):
            if article["description"] and article["title"]:
                n += 1
                url = article["url"]
                embed=discord.Embed(title=article["title"], url=url, description=article["description"], color=0xff8040)
                dict = article["source"]
                embed.set_author(name=dict["name"])
                embed.set_thumbnail(url=article["urlToImage"])
                content = str(article["content"])
                content = content.replace("[+", "\n[+")
                content = content.replace("chars]", f"caractères, cliquez pour lire l'article.]({url})")
                embed.add_field(name="contenu de l'article :", value=content, inline=False)
                daten = datetime.strptime(article["publishedAt"], '%Y-%m-%dT%H:%M:%SZ')
                daten_string = daten.strftime("%d/%m/%Y - %H:%M")
                embed.set_footer(text=f"{daten_string} - Powered by News API")
                msg = await message.channel.send(embed=embed)
                if n >= 3:
                    break


    @commands.command(help='Le bot te liste les 3 news importantes les plus récentes.')
    async def news(self, ctx):
        await self.run_news(ctx.message)

def setup(bot):
    bot.add_cog(News(bot))