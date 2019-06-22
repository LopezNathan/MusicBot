import discord
import youtube_dl
import logging

client = discord.Client()
yt_dl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Bot(object):

    # Pull Discord Bot Token from Docker Secrets
    BOT_TOKEN = open('/run/secrets/bot_token').read()

    def bot_runner():
        client.run(Bot.BOT_TOKEN)

    async def bot_connector(message):
        try:
            channel = message.author.voice.channel
            logger.info(client.user.name + " connected to voice channel.")
            return await channel.connect()
        except AttributeError:
            logger.exception('No voice channel available.')
            await message.channel.send("Connect to a Voice channel first.")
        # TODO - Capture proper exception
        except:
            logger.exception('bare Exception')
            await message.channel.send("Already connected to Voice channel..")

    async def set_bot_status(video_title):
        activity = discord.Activity(name=video_title, type=discord.ActivityType.listening)
        return await client.change_presence(activity=activity)

    @client.event
    async def on_ready():
        logger.info("-------------------")
        logger.info(client.user.name + " connected successfully.")
        logger.info("-------------------")


class Audio(object):

    def video_extracter(video_url):
        with yt_dl:
            video_data = yt_dl.extract_info(
                video_url,
                download=False
            )

        return video_data

    def video_url(video_data):
        return video_data['formats'][0]['url']

    def video_title(video_data):
        return video_data['title']

    @client.event
    async def on_message(message):

        if message.content.startswith("!play"):
            video_data = Audio.video_extracter(message.content[6:])
            video_url = Audio.video_url(video_data)
            video_title = Audio.video_title(video_data)

            connection = await Bot.bot_connector(message)
            await Bot.set_bot_status(video_title)

            logger.info(f'is playing: {connection.is_playing()}')
            connection.play(discord.FFmpegPCMAudio(video_url))

        if message.content.startswith("!disconnect"):
            for connection in client.voice_clients:
                await connection.disconnect()
                logger.info(client.user.name + " disconnected from voice channel.")


Bot.bot_runner()
