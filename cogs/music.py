from ast import alias
import nextcord, ffmpeg
from nextcord.ext import commands
from youtube_dl import YoutubeDL


class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
        
        async def on_message(message):
            if message.content.lower() == '$play':
                if message.content.lower() == '$play':
                    channel = client.get_channel(547155964328149007)
                    vc = await channel.connect()
                    vc.play(nextcord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source='mp3.mp3'), after=lambda e: print('done', e))
                    vc.is_playing()
                    vc.pause()
                    vc.resume()
                    vc.stop()
                    vc = await channel.connect()
                    vc.play(nextcord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="mp3.mp3"), after=lambda e: print('done', e))  

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(nextcord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS, executable="C:/ffmpeg/bin/ffmpeg.exe"), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.reply("No se puede conectar con el vc")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)
            self.vc.play(nextcord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS, executable="C:/ffmpeg/bin/ffmpeg.exe"),  after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Musica on")

    @commands.command()
    async def play(self, ctx, *args):
        await ctx.reply("Añadiendo cancion espere.", delete_after=2)
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.reply("Conectado a un vc")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.reply("No se pudo descargar la canción. Formato incorrecto pruebe con otra palabra clave. Esto podría deberse a una lista de reproducción o un formato de transmisión en vivo.")
            else:
                cancion = nextcord.Embed(title="Cancion añadida en la lista!", description=f"Cancion sonando ahora: {song['title']}")
                await ctx.reply(embed=cancion)
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command()
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.reply(embed=nextcord.Embed(title="Cancion parada!"))
        elif self.is_paused:
            self.vc.resume()
            self.is_playing = True
            self.is_paused = False
            await ctx.reply(embed=nextcord.Embed(title="Cancion reanuada"))

    @commands.command()
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()
            self.is_playing = False
            self.is_paused = True
            await ctx.reply(embed=nextcord.Embed(title="Cancion reanuada"))
        if self.is_paused:
            self.vc.resume()
            self.is_playing = True
            self.is_paused = False
        else:
            self.is_paused
            self.vc.resume()
            self.is_playing=True
            self.is_paused=False
            await ctx.reply(embed=nextcord.Embed(title="La cancion no esta parada!"))

    @commands.command()
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
            await ctx.reply(embed=nextcord.Embed(title="Cancion skipeada!"))


    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"
        if retval != "":
            embed = nextcord.Embed(title="Lista de Musica en espera", description=f"**{retval}**")
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("No hay mas musica en la lista.")

    @commands.command(aliases=["c", "bin"])
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.reply("Lista limpiada")

    @commands.command(aliases=["disconnect", "l", "d"])
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()

def setup(client):
    client.add_cog(music(client))