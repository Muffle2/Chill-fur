import nextcord, datetime
from nextcord.ext import commands
from utils.utils import readJSON, writeJSON, createJSON, checkifexits

class Bienvenidas(commands.Cog):
    def __init__(self, client):
        self.client=client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bienvenida on")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if checkifexits(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json") == False:
            createJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            join = readJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            join["fecha"] = f"{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}"
            join["mensajes"] = 0
            join["join"] = 0+1
            join["leave"] = 0
            writeJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json", join)
        else:
            join = readJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            join["join"] +=1
            writeJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json", join)
        
        true_member_count = len([m for m in member.guild.members if not m.bot])
        embed=nextcord.Embed(title=f"Bienvenido al servidor {member.name}!", description=f"""Recuerda pasarte por las reglas para no tener ningún problema!
        Esperemos que lo pases bien en el servidor {member.mention}.""".replace("	", ""))
        embed.set_footer(text=f"Eres el usuario {true_member_count}")
        embed.set_image(url="https://c.tenor.com/SHu_Ynq3EGEAAAAC/welcome.gif")
        await self.client.get_channel(1048691139483533372).send(embed=embed)



    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if checkifexits(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json") == False:
            createJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            leave = readJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            leave["fecha"] = f"{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}"
            leave["mensajes"] = 0
            leave["leave"] = 0+1
            leave["join"] = 0
            writeJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json", leave)
        else:
            leave = readJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json")
            leave["leave"] +=1
            writeJSON(f"estadisticas/{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year}.json", leave)
        
        true_member_count_leave = len([m for m in member.guild.members if not m.bot])
        leave=nextcord.Embed(title=f"Se retiro del servidor {member.name}", description="Esperemós que vuelvas algún día")
        leave.set_footer(text=f"Ahora somos {true_member_count_leave} usuarios")
        leave.set_image(url="https://c.tenor.com/REzcaDkuv68AAAAC/katezuh-foxynian.gif")
        await self.client.get_channel(1048691139483533372).send(embed=leave)



def setup(client):
    client.add_cog(Bienvenidas(client))