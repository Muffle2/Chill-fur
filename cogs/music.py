from ast import alias
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL



class music(commands.Cog):
    def __init__(self, client):
        self.client = client
    
        #all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
        


        async def on_message(message):
            if message.content.lower() == '$play':
                if message.content.lower() == '$play':
                    channel = client.get_channel(547155964328149007)
                    vc = await channel.connect()
                    vc.play(discord.FFmpegPCMAudio('mp3.mp3'), after=lambda e: print('done', e))
                    vc.is_playing()
                    vc.pause()
                    vc.resume()
                    vc.stop()
                    vc = await channel.connect()
                    vc.play(discord.FFmpegPCMAudio(executable="C:/path/ffmpeg.exe", source="mp3.mp3"))  

     #searching the item on youtube
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

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.reply("No se puede conectar con el vc")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="Play una musica de youtube")
    async def play(self, ctx, *args):
        await ctx.reply("Añadiendo cancion espere.", delete_after=5)
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
                await ctx.reply("Cancion añadida a la lista")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pausa la cancion")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name = "resume", aliases=["r"], help="Resume la cancion puesta")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)


    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            embed = discord.Embed(title="Lista de Musica en espera", description=f"{retval}")
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("No hay mas musica en la lista.")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.reply("Lista limpiada")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()

def setup(client):
    client.add_cog(music(client))