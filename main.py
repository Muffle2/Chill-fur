import asyncio, random, os, database, nextcord, youtube_dl
from database import token
from nextcord.ext import commands



youtube_dl.utils.bug_reports_message = lambda: ''
client = commands.Bot(command_prefix="!", case_insensitive=True, owner_id=333363893546123264, intents=nextcord.Intents.all())

client.remove_command("help")

@client.event
async def on_ready():
    print("client Online")
    await client.change_presence(status=nextcord.Status.idle,activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Server en desarollo"))

@client.event
async def on_member_join(member):
	embed=nextcord.Embed(title=f"Bienvenido al servidor {member.mention}!", description="Recuerda leer las reglas para evitar ser sancionado y disfruta del servidor!")
	await client.get_channel(981862648264163348).send(embed = embed)

@client.command()
async def help(ctx):
    embed = nextcord.Embed(title="Menu de ayuda")
    embed.add_field(name="Comandos de musica", value="!musica", inline=False)
    embed.set_footer(text="Powered by Muffle")
    await ctx.reply(embed=embed)

@client.command()
async def musica(ctx):
    embed = nextcord.Embed(title="Comandos de musica")
    embed.add_field(name="Musica", value="|!play|!stop|!clear|!queue|!resume|!skip|!dc|!pause|")
    embed.set_footer(text="Powered by Muffle")
    await ctx.reply(embed=embed)

@client.command(name="user")
async def user(ctx, user:nextcord.Member=None):
	if user == None:
		user=ctx.author

@client.command()
async def load(ctx, cog=None):
	if ctx.author.id == 333363893546123264:
		if cog == None:
			await ctx.reply("Especifica una cog")
		else:
			try:
				client.load_extension(f"cogs.{cog}")
				await ctx.reply(f"{cog} cargada.")
			except:
				await ctx.reply(f"Error cargando {cog}")
	else: 
		user == None
		await ctx.reply("Quien eres? No pareces mi dueño")


@client.command()
async def unload(ctx, cog=None):
	if ctx.author.id == 333363893546123264:
		if cog == None:
			await ctx.reply("Especifica una cog.")
		else:
			try:
				client.unload_extension(f"cogs.{cog}")
				await ctx.reply(f"{cog} deshabilitada.")
			except:
				await ctx.reply(f"Error deshabilitando {cog}")
	else: 
		user == None
		await ctx.reply("Quien eres? No pareces mi dueño")

	
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

client.run(token)