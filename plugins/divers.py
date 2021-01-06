import discord, asyncio, time, os, requests, random, json, praw
from discord.ext import commands
from discord.ext.commands import Bot
from vacances.vacances import vacances_create_image
# from series.main import draw_image, message
from mcstatus import MinecraftServer
# from imdb import IMDb
from lxml import html

# imdb = IMDb()
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('BOT_PREFIX')

reddit = praw.Reddit(client_id=os.getenv('REDDIT_ID'),
  client_secret=os.getenv('REDDIT_SECRET'), 
  password=os.getenv('REDDIT_PASSWORD'),
  user_agent='electryon-bot',
  username='hevelmc')

subreddit = reddit.subreddit("rance")

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


class Series(commands.Cog):
    def __init__(self, client):
        self.client = client

    def check(self, file, title):
        with open(file, 'r+') as f:
            for l in f:
                if title in l:
                    return False
        return True

    @commands.command(help='Envie une description, une image et quelques informations sur la série entrée.')
    async def serie(self, ctx, *, arg=""):
        if arg:
            m = await ctx.send("Je recherche votre série... Une petite seconde.")
            if await draw_image(arg):
                text, comment = await message()
                e = discord.Embed(description=text)
                e.set_footer(text=f"©️ SeriesBot - 2020")
                await m.delete()
                await ctx.send(embed=e, file=discord.File('./series/export.png'))
            else:
                await m.delete()
                await ctx.send("Désolé, je n'ai pas trouvé cette série dans la base de données !")
        else: await ctx.send("Veuillez entrer une série.")
    
    # @commands.command(help='Propose une série à envoyer sur Twitter.')
    # async def add_serie(self, ctx, *, arg=""):
    #     if arg:
    #         m = await ctx.send("Je recherche votre série... Une petite seconde.")
    #         try:
    #             imdb_show = imdb.search_movie(arg)[0]
    #             title = imdb_show["title"]
    #         except:
    #             await m.delete()
    #             return await ctx.send("Désolé, je n'ai pas trouvé cette série dans la base de données !")
    #         await m.delete()
    #         if self.check("./series/suggest_list.txt", title) and self.check("./series/basic_list.txt", title):
                
    #             m2 = await ctx.send(f"👁️ Nous avons trouvé la série `{title}`.\nSi le titre correspond à la série que vous avez vu et que vous souhaitez partager, cliquez sur la réaction ✅.\nAttention, parfois le titre original est différent du titre en Français :flag_fr: !\n\nVous avez 30 secondes, dans le cas contraire l'action sera annulée.")
    #             await m2.add_reaction("✅")

    #             def confirmation(reaction, user):
    #                 return user == ctx.author and str(reaction.emoji) == '✅'

    #             try:
    #                 reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=confirmation)
    #             except asyncio.TimeoutError:
    #                 await m2.delete()
    #                 return await ctx.send("⏲️ Le temps est écoulé, la série ne sera pas ajoutée.")
    #             else:
    #                 await m2.delete()
    #                 await ctx.send(f"✅ Merci pour votre suggestion, la série `{title}` apparaîtra dans les publications dans les quelques jours.")

    #                 with open("./series/suggest_list.txt",'a') as f:
    #                     f.write(f"{title}||Suggéré par {ctx.author.name} sur http://discord.electryon-mc.fr\n")
    #         else:
    #             await ctx.send(f"🔴 Désolé, la série `{title}` a déjà était suggérée; vous pouvez en proposer une autre.")
        
    #     else: await ctx.send("❗ Veuillez entrer une série.")



class Random(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Donne une image aléatoire de renards.')
    async def fox(self, ctx):
        await self.animals("fox", ctx.message)
    @commands.command(help='Donne une image aléatoire de joli chats.')
    async def cat(self, ctx):
        await self.animals("cat", ctx.message)
    @commands.command(help='Donne une image aléatoire de joli chiens.')
    async def dog(self, ctx):
        await self.animals("dog", ctx.message)
    @commands.command(help="Envie d'une blague de développeur ?")
    async def stupidcode(self, ctx):
        await self.stupidcode_img(ctx.message)
    @commands.command(help="Envie d'un meme reddit ?")
    async def meme(self, ctx):
        await self.meme_img(ctx.message)

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

    async def meme_img(self, message):

        while True:
            meme = subreddit.random()
            if ".jpg" in meme.url:
                e = discord.Embed(title=meme.title)
                e.set_footer(text=f"Reddit: {meme.name}")
                e.set_image(url=meme.url)

                msg = await message.channel.send(embed=e)
                await msg.add_reaction('👍')
                await msg.add_reaction('👌')
                await msg.add_reaction('👎')
                await msg.add_reaction('🔂')
                break

    async def stupidcode_img(self, message):

        r = requests.get("https://foutucode.fr/?random=1")
        html_page = html.fromstring(r.content)
        url = html_page.xpath('/html/body/div[1]/div[1]/div[6]/a/img')[0].attrib['src']

        # text = html_page.xpath("/html/body/div[1]/section/div/div/div[1]/div[1]/h2/a")[0]
        # try:
        #     imageSrc = html_page.xpath("/html/body/div[1]/section/div/div/div[1]/div[3]/figure/img")[0].attrib['data-srcset'].split(" ")[0]
        # except:
        #     text = "Erreur : l'API a rencontré un problème !"
        
        embed=discord.Embed(title="test")
        if imageSrc:
            embed.set_image(url=url)
        embed.set_footer(text="FoutuCode - ©️ foutucode.fr")
        msg = await message.send(embed=embed)

        await msg.add_reaction('👍')
        await msg.add_reaction('👌')
        await msg.add_reaction('👎')
        await msg.add_reaction('🔂')

    @commands.command(help='Donne une image aléatoire de cadeau d\'anniversaire.')
    async def anniv(self, ctx, target: commands.Greedy[discord.Member] = None):
        apikey = "95I7UHIC0P1P"
        lmt = 50

        search_term = "birthday"

        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        if target:

            if r.status_code == 200:
                # load the GIFs using the urls for the smaller GIF sizes
                gifs = json.loads(r.content)

                random1 = random.randrange(1, lmt)

                _1 = gifs.get("results")[random1].get("media")[0].get("gif").get("url")
                print(_1)
                await ctx.channel.send(f"Joyeux anniversaire <@{target[0].id}> !\n\n" + _1)
            else:
                return await ctx.channel.send("Erreur api :'(")
        
        else:
            return await ctx.channel.send("Désolé mais vous devez spécifier un pseudonyme.")


class Ninety_Nine(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='99', help='Répond que c\'est la forme humaine de l\'émoji 💯')
    async def command_ninety_nine(self, ctx):
        await ctx.send('Je suis la forme humaine de l\'emoji 💯')
    @commands.command(help='Donne la latence du bot.')
    async def ping(self, ctx):
        """ Pong! """
        await ctx.message.delete()
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")
    @commands.command(help='Spam Hevel sur son téléphone')
    async def spamhevel(self, ctx):
        await ctx.send('J\'ai spammé Hevel 💯 !')
        r = requests.post("https://api.pushover.net/1/messages.json", data = {
            "token": "avx6mvx98apqd6igkq9nsyphpu1ap1",
            "user": "u59d1dwsms1y1fc5rdbeasoqsgpv3j",
            "title": "SPAMMMMM!",
            "message": f"SPAMMMMMM!",
            "sound" : "persistent"
        })
    @commands.command(help='Spam Jujua sur son téléphone')
    async def spamjujua(self, ctx):
        await ctx.send('J\'ai spammé Jujua_c 💯 !')
        r = requests.post("https://api.pushover.net/1/messages.json", data = {
            "token": "avx6mvx98apqd6igkq9nsyphpu1ap1",
            "user": "uhuu3o8iofx18tzewit5djb53py87d",
            "title": "SPAMMMMM!",
            "message": f"SPAMMMMMM!",
            "sound" : "alien"
        })
    @commands.command(help='Spam quelqu\'un par MP')
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, user: commands.Greedy[discord.Member], *, message="Il n'a pas laissé de message"):
        for i in range(10):
            await user[0].send(f'Hey {user[0].name} tu as été SPAMMÉ par {ctx.author.name} !\n**{message}**')
        await ctx.send(f'C\'est fait, 10 messages envoyés à {user[0].name} !')


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

    @commands.command(help='Donne le nombre de joueurs en ligne sur le serveur Minecraft.')
    async def mc(self, ctx):
        await self.minecraft(ctx)
    @commands.command(help='Donne le nombre de joueurs en ligne sur le serveur Minecraft.')
    async def minecraft(self, ctx):
        server = MinecraftServer("electryon-mc.fr", 25565)
        query = server.query()
        s = "s" if query.players.online > 1 else ""
        await ctx.send(f"Il y a actuellement `{query.players.online} joueur{s} connecté{s}` sur le serveur minecraft.")
        [await ctx.send(f"- {player}") for player in query.players.names]

        status = await Online.status_task(self)
        if status:
            await ctx.send("Mise à jour du salon joueurs connectés !")

    @commands.Cog.listener()
    async def on_ready(self):

        embed = self.GetMembersOnline(["online", "idle", "dnd"])

        print((embed.title + "\n\n" +
               embed.description).replace("*", "").replace("_", ""))

        for field in embed.fields:
            print('\n\n')
            print((field.name + "\n" + field.value).replace("*", "").replace("_", ""))

        self.client.loop.create_task(Online.status_update(self))

        print("")

    async def status_update(self):
        channel = self.client.get_channel(705335574520791060)
        server = MinecraftServer("electryon-mc.fr", 25565)
        status = server.status()
        s = "s" if status.players.online > 1 else ""
        if channel.name != f"Connecté{s} : {status.players.online} joueur{s}":
            await channel.edit(reason="Update number of online players", name=f"Connecté{s} : {status.players.online} joueur{s}")
            return True
        else:
            return False
    
    async def status_task(self):
        while True:
            await Online.status_update(self)
            await asyncio.sleep(300)

def setup(bot):
    bot.add_cog(Random(bot))
    bot.add_cog(Vacances(bot))
    bot.add_cog(Series(bot))
    bot.add_cog(Online(bot))
    bot.add_cog(Ninety_Nine(bot))
