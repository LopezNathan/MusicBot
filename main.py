import discord
import youtube_dl
from os import environ

client = discord.Client()
yt_dl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})


class Bot(object):

    # Pull Discord Bot Token from Environment Variable "BOT_TOKEN"
    if environ.get('BOT_TOKEN') is not None:
        BOT_TOKEN = environ.get('BOT_TOKEN')

    def bot_runner():
        client.run(Bot.BOT_TOKEN)

    async def bot_connector(message):
        try:
            channel = message.author.voice.channel
            return await channel.connect()
        except AttributeError:
            await message.channel.send("Connect to a Voice channel first.")
        # TODO - Capture proper exception
        except:
            await message.channel.send("Already connected to Voice channel..")

    async def set_bot_status(video_title):
        activity = discord.Activity(name=video_title, type=discord.ActivityType.watching)
        return await client.change_presence(activity=activity)

    @client.event
    async def on_ready():
        print(client.user.name + " connected successfully.")
        print("-------------------")


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

            connection.play(discord.FFmpegPCMAudio(video_url))

        if message.content.startswith("!disconnect"):
            for connection in client.voice_clients:
                await connection.disconnect()


Bot.bot_runner()
