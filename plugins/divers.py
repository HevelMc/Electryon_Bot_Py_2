import discord
from discord.ext import commands
from discord.ext.commands import Bot

from vacances.vacances import vacances_create_image

import os
import requests
import json

GUILD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('BOT_PREFIX')
ELECTRYON_GUILD_ID = 444183245542916106


class Vacances(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='vacances', help='Donne le nombre de jours restants avant les prochaines vacances.')
    async def vacances(self, ctx, *, arg="None"):
        vacances_create_image()
        await ctx.send(file=discord.File('./vacances/data/export_A.png'))
        await ctx.send(file=discord.File('./vacances/data/export_B.png'))
        await ctx.send(file=discord.File('./vacances/data/export_C.png'))


class Random(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def animals(self, name, message):
        print(name)
        if name == "fox":
            await self.random_img("Voici une image aléatoire d'un petit renard tout mignon !", "Certains préfèrent les chats, d'autres les chiens et bien moi c'est les renards. Lovely :orange_heart:", "fox", "https://randomfox.ca/floof/", "image", message)
        elif name == "cat":
            await self.random_img("Voici une image aléatoire d'un adorable chat trop mignon !", "Ne sont-ils pas adorables ? So cute :green_heart:", "cat", "https://aws.random.cat/meow", "file", message)
        elif name == "dog":   
            await self.random_img("Voici une image aléatoire d'un fantastique chien trop mignon !", "N'est-il pas sublime ? Sweety :blue_heart:", "dog", "https://random.dog/woof.json", "url", message)

    async def random_img(self, title, description, function_name, url, file, message):

        r = requests.get(url = url)
        rjson = r.json()
        e = discord.Embed(title=title, description=description)
        e.set_footer(text=f"Random: {PREFIX}{function_name}")
        e.set_image(url=rjson[file])

        msg = await message.channel.send(embed=e)
        await msg.add_reaction('👍')
        await msg.add_reaction('👌')
        await msg.add_reaction('👎')
        await msg.add_reaction('🔂')

    @commands.command(help='Donne une image aléatoire de renards.')
    async def fox(self, ctx):
        await self.animals("fox", ctx.message)
    @commands.command(help='Donne une image aléatoire de joli chats.')
    async def cat(self, ctx):
        await self.animals("cat", ctx.message)
    @commands.command(help='Donne une image aléatoire de joli chiens.')
    async def dog(self, ctx):
        await self.animals("dog", ctx.message)


class Ninety_Nine(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='99', help='Répond que c\'est la forme humaine de l\'émoji 💯')
    async def command_ninety_nine(self, ctx):
        await ctx.send('Je suis la forme humaine de l\'emoji 💯')


class Online(commands.Cog):
    def __init__(self, client):
        self.client = client

    def GetMembersOnline(self, statut=["online", "idle", "dnd", "offline"]):
        members_online = []
        members_idle = []
        members_dnd = []
        members_offline = []
        for guild in self.client.guilds:
            if guild.id == ELECTRYON_GUILD_ID:
                GUILD = guild
                break

        _botNum = 0
        _memberNum = 0

        for member in GUILD.members:

            if member.bot:
                member_n = "***[BOT]** " + member.name + "*"
                _botNum += 1
            else:
                member_n = member.name
                _memberNum += 1

            if member.status == discord.Status.online:
                members_online.append(member_n)
            elif member.status == discord.Status.idle:
                members_idle.append(member_n)
            elif member.status == discord.Status.dnd:
                members_dnd.append(member_n)
            else:
                members_offline.append(member_n)

            members_online_str = '\n - '.join(
                [member for member in members_online])
            members_idle_str = '\n - '.join(
                [member for member in members_idle])
            members_dnd_str = '\n - '.join([member for member in members_dnd])
            members_offline_str = '\n - '.join(
                [member for member in members_offline])

        embed = discord.Embed(title=f"{self.client.user} est connecté au serveur: {GUILD.name}",
                              description=f"**Voici la liste des membres du serveur**  ({str(_memberNum)} membres et {str(_botNum)} bots)", color=0x00ff40)
        if "online" in statut:
            embed.add_field(name=f"En Ligne",
                            value=f"\n - {members_online_str}", inline=False)
        if "dnd" in statut:
            embed.add_field(name=f"Ne pas déranger",
                            value=f"\n - {members_dnd_str}", inline=False)
        if "idle" in statut:
            embed.add_field(
                name=f"Absent", value=f"\n - {members_idle_str}", inline=False)
        if "offline" in statut:
            embed.add_field(name=f"Hors Ligne",
                            value=f"\n - {members_offline_str}", inline=False)
        # return(embed, f'{self.client.user} est connecté au serveur:\n{GUILD.name} (id: {GUILD.id})\nMembres du serveur:\n\nEn ligne:\n - {members_online_str}\n\nNe pas déranger:\n - {members_dnd_str}\n\nAbsents:\n - {members_idle_str}\n\nHors Ligne:\n - {members_offline_str}')
        return(embed)

    @commands.command(help='Retourne la liste des membres du serveur triés par status.')
    async def online(self, ctx, show='["online", "idle", "dnd"]'):
        embed = self.GetMembersOnline(show)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):

        embed = self.GetMembersOnline(["online", "idle", "dnd"])

        print((embed.title + "\n\n" +
               embed.description).replace("*", "").replace("_", ""))

        for field in embed.fields:
            print('\n\n')
            print((field.name + "\n" + field.value).replace("*", "").replace("_", ""))

        print("")


def setup(bot):
    bot.add_cog(Vacances(bot))
    bot.add_cog(Online(bot))
    bot.add_cog(Ninety_Nine(bot))
    bot.add_cog(Random(bot))
