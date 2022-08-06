import nextcord, json
from nextcord.ext import commands


class embeds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("embed on")

    @commands.command()
    async def si(self,ctx):
        if ctx.author.id == 333363893546123264:
            rol = nextcord.Embed(title="Auto Roles de hobbies", description="Aquí puedes ponerte roles de los hobbies que hagas!")
            rol.add_field(name="Programacion", value=":keyboard:", inline=True)
            rol.add_field(name="Gamer", value=":video_game:", inline=True)
            rol.add_field(name="Artista", value=":art:", inline=True)
            await ctx.send(embed=rol)
        else: 
            await ctx.send("Tu no eres mi creador...")

        



def setup(client):
    client.add_cog(embeds(client))