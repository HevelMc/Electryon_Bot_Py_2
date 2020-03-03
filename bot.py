from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions, CommandNotFound
import discord

import os
from dotenv import load_dotenv

load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('BOT_PREFIX')

client = commands.Bot(command_prefix=f"{PREFIX}")

startup_extensions = ["blague", "afk", "divers", "events", "musique", "help"]

client.remove_command('help')


@client.event
async def on_ready():
    print('Connecté en tant que')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client.change_presence(activity=discord.Activity(game=discord.Game(name=':joy: Testing status', type=4)))


@client.command(help="Affiche ou définit le préfixe de commande du bot.")
@commands.has_permissions(administrator=True)
async def prefix(ctx, cmd=None, new_prefix=PREFIX):
    if cmd:
        if cmd == "set":
            if new_prefix:
                print("test5")
                os.environ["BOT_PREFIX"] = new_prefix
                await ctx.channel.send(f"Le préfixe du bot Electryon est désormais `{PREFIX}`.")
                print("test4")
            else:
                print("test3")
                await ctx.channel.send(f"Vous n'avez pas défini de préfixe à définir.")
        else:
            print("test2")
            await ctx.channel.send(f"`commande {PREFIX}prefix {cmd}` inconnue, utlisez `{PREFIX}prefix set <prefix>` pour définir.")
    else:
        print("test")
        await ctx.channel.send(f"Le préfixe du bot Electryon est `{PREFIX}`.")

@client.command()
async def load(extension_name: str):
    """Charge une extension."""
    try:
        client.load_extension("plugins." + extension_name)
    except (AttributeError, ImportError) as e:
        await client.say(f"```py\n{type(e).__name__}: {str(e)}\n```")
        return
    await client.say(f"{extension_name} chargée.")


@client.command()
async def unload(extension_name: str):
    """Décharge une extension."""
    client.unload_extension("plugins." + extension_name)
    await client.say(f"{extension_name} déchargée.")


@client.event
async def on_member_join(member):
    embed = discord.Embed(title="▶️ Hey ! Un nouveau membre vient de rejoindre le Discord ! 👏",
                          description=f"**Bienvenue sur Electryon <@{member.id}>.** \n\nN'hésite pas à visiter le salon <#511660954690256899> pour te renseigner sur le serveur et obtient le grade Membre en acceptant le <#447791775164268554>.", color=0x00ff40)
    embed.set_footer(text="Electryon - Serveur Discord Communautaire",
                     icon_url="https://cdn.discordapp.com/attachments/440073352581873676/621370927858319360/3.png")
    channel = client.get_channel(444523954757959680)
    await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    embed = discord.Embed(title="💀 Aïe, quelqu'un vient de quitter le Discord. 😥",
                          description=f"**Dites au revoir à __{member.display_name}__.**", color=0x7f7f7f)
    embed.set_footer(text="Electryon - Serveur Discord Communautaire",
                     icon_url="https://cdn.discordapp.com/attachments/440073352581873676/621370927858319360/3.png")
    channel = client.get_channel(444523954757959680)
    await channel.send(embed=embed)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            client.load_extension("plugins." + extension)
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(
                f'Error: Echec du chargement de l\'extension {extension}\n{exc}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        error = discord.Embed(title=f"⛔ Oups commande `{ctx.message.content.split()[0]}` inconnue.\n<:404_1:672060701535371284> <:404_2:672060701778509865> <:404_3:672061112140955670>", description=f"**Vous pouvez utiliser la commande `{PREFIX}help` pour afficher la liste des commandes disponibles.**", color=0xff0000)
        print(f"ERROR Commande {ctx.message.content} inconnue (auteur: {ctx.author})")
        return await ctx.message.channel.send(embed=error)
    raise error

client.run(os.getenv('DISCORD_TOKEN'))