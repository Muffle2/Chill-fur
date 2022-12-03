import nextcord, datetime, math, time, os, asyncio
from nextcord.ext import commands
from utils.utils import readJSON, writeJSON, createJSON, checkifexits
from utils.bot_utils import checkTIME

class stats(commands.Cog):
    def __init__(self, client):
        self.client=client

    @commands.Cog.listener()
    async def on_ready(self):
        print("stats on")

    @commands.Cog.listener()
    async def on_message(self, message):   
        if message.author.bot == True: return
        if checkifexits(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json") == False:
            createJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            stats = readJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            stats["fecha"] = f"{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}"
            stats["mensajes"] = 0+1
            stats["join"] = 0
            stats["leave"] = 0
            writeJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json", stats)
        else:
            stats = readJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            stats["mensajes"] +=1
            writeJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json", stats)


    @commands.command(aliases=["stats"])
    async def estadisticas(self, ctx):
        StatsEmbed = nextcord.Embed(title="📊 |Aquí te presento las estadisticas del servidor!", description="¡Las estadisticas son de el dia de hoy!", color=nextcord.Color.random())
        StatsEmbed.set_author(name = f"🦷 | Chill Fur » Comando estadisticas.")
        StatsEmbed.set_footer(text = f"© Powered by Muffle | {datetime.datetime.now().year}", icon_url = self.client.user.avatar.url)
        StatsEmbed.set_thumbnail(url=ctx.guild.icon)
        if checkifexits(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json") == True:
            stats = readJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            stats["mensajes"]
            stats["join"]
            stats["leave"]
            StatsEmbed.add_field(name="🌐 | Mensajes totales del dia", value=stats['mensajes'], inline=False)
            StatsEmbed.add_field(name="🧍‍♂️ | Usuarios que se han unidos", value=stats['join'], inline=True)
            StatsEmbed.add_field(name="⚠ | Usuarios que han abandonado", value=stats['leave'], inline=True)
        await ctx.reply(embed= StatsEmbed)

def setup(client):
    client.add_cog(stats(client))