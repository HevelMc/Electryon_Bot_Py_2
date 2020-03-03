import discord
from discord.ext import commands
from discord.ext.commands import Bot

import numpy as np
import os
import json

PREFIX = os.getenv('BOT_PREFIX')

def load_dict(dict_name):
    if os.path.isfile(f'data/{dict_name}.npy'):
        dict = np.load(f'data/{dict_name}.npy',allow_pickle='TRUE').item()
        return dict
    else:
        dict = {}
        np.save(f'data/{dict_name}.npy', dict)
        return dict

def save_dict(dict, dict_name):
    np.save(f'data/{dict_name}.npy', dict)

class Afk(commands.Cog):
    def __init__(self, Bot):
        self.bot = Bot

    @commands.command(help='Active ou désactive votre mode AFK.')
    async def afk(self, ctx, *, message="Je suis AFK, je ne peux pas vous répondre."):
        afk = load_dict("afk")
        if afk.get(ctx.author.id) != None:
            afk.pop(ctx.author.id)
            save_dict(afk, "afk")
            await ctx.send(f":gear: :white_check_mark: C'est fait, **nous avons retiré votre mode `AFK`**. Bon retour parmis nous, {ctx.author.name}")
        else:
            afk[ctx.author.id] = message
            save_dict(afk, "afk")
            await ctx.send(f":gear: :white_check_mark: Bien sûr __{ctx.author.name}__, **nous activons votre mode `AFK`** pour le motif suivant :\n```{message}```")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith(PREFIX):
            if not message.author.bot:
                afk = load_dict("afk")
                if afk.get(message.author.id) is not None:
                    await message.channel.send(f":tada: Bon retour parmis nous **{message.author.name}**. \nAu fait, votre Mode `AFK` est toujours activé, n'hésitez pas à le retirer avec la commande `{PREFIX}afk`.")
            
                for index in afk:
                    if message.author != self.bot.get_user(index):
                        if "<@!" + str(index) + ">" in message.content:
                            await message.channel.send(f":gear: Désolé, **{message.guild.get_member(index).name}** est actuellement `AFK` pour la raison suivante :\n```{afk.get(index)}```")
def setup(bot):
    bot.add_cog(Afk(bot))