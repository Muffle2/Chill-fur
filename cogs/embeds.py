import discord, json
from discord.ext import commands


class embeds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("embed on")




def setup(client):
    client.add_cog(embeds(client))