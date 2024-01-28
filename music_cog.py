import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 - reonnected_streamed 1 - reconnected_delay_max 5'}

        self.vc = None

    def search_yt(self,item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'[0]['url']], 'title': info['title']}
    
    def play_next(self):
        """
        lambda used because after requires a function
        recursive, continues playing while there exists a next in the queue
        """
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegAudio(m_url, **self.FFMPEG_OPTIONS) , after=lambda x: self.play_next())
        else:
            self.is_playing = True

    async def play_music(self, ctx):
        """
        ctx = context
        """
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                if self.vc == None:
                    await ctx.send("Frogg can't join your channel.")
                    return
            else: 
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda x: self.play_next())
        else:
            self.is_playing = False

    
    @commands.command(name="play",aliases=["p","playing","sing"], help="Play the selected song from Youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice_channel
        # get user vc
        if voice_channel is None:
            await ctx.send("My brother in Christ, connect to a voice channel. NOW!")
        # if paused then resume existing
        elif self.is_paused:
            self.vc.resume()
        else: 
            # search for music
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format, try a different keyword.")
            else:
                await ctx.send("Song added to the Froggy queue.")
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", aliases=["p"], help="Pauses current song.")
    async def pause(self, ctx, *args): 
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"], help="Resumes current song.")
    async def pause(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips current song.")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Shows the current music queue.")
    async def queue(self, ctx, *args):
        retval = ""
        for i in range(len(self.music_queue)):
            if i > 4:
                break
            retval += self.music_queue[i][0]['title'] + "\n"
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Frogg has no music for you. This is a sad day.")

    @commands.command(name="clear", aliases=["c"], help="Clears the current music queue of all music.")
    async def queue(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Frogg just threw away all yo music.")

    @commands.command(name="leave", aliases=["l","disconnect","d"], help="Kicks bot from the voice channel.")
    async def queue(self, ctx, *args):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()