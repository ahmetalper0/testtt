from discord.ext import commands
import discord
import requests
from random import randint
import asyncio
from PIL import Image
from io import BytesIO

#-------------------------------------------------- << VARIABLES >> --------------------------------------------------#

TOKEN = 'MTA5NDIzMzQxOTkyNTQyMjIwMg.GAHXfN.7LuHaqsLOwUsEYflucYhEWuscbZgNNAxr_q-Xk'

#-------------------------------------------------- << BOT >> --------------------------------------------------#

command_prefix = '/'
intents = discord.Intents.all()
status = discord.Status.idle
activity = discord.Activity(type = discord.ActivityType.listening, name = '/help') 

bot = commands.Bot(command_prefix = command_prefix, intents = intents, help_command = None, status = status, activity = activity)

#-------------------------------------------------- << EVENTS >> --------------------------------------------------#

@bot.event
async def on_ready():

    print(f'\n[ {bot.user} ] has connected to Discord!\n')

#-------------------------------------------------- << COMMANDS >> --------------------------------------------------#

@bot.command()
async def help(ctx):

    await ctx.send('/help')

@bot.command()
async def test(ctx, *, prompt):

    def imagine(prompt, guild_id, channel_id, token):

        headers = {
            'authorization': token,
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryovwotFdnidjPp7wJ'
        }

        data = f'------WebKitFormBoundaryovwotFdnidjPp7wJ\r\nContent-Disposition: form-data; name="payload_json"\r\n\r\n{{"type":2,"application_id":"1049413890276077690","guild_id":"{guild_id}","channel_id":"{channel_id}","session_id":"e747a9ff72102f5a7cecd2cd92832124","data":{{"version":"1049422742912507995","id":"1049422742912507994","name":"imagine","type":1,"options":[{{"type":3,"name":"prompt","value":"{prompt}"}}],"application_command":{{"id":"1049422742912507994","application_id":"1049413890276077690","version":"1049422742912507995","default_member_permissions":null,"type":1,"nsfw":false,"name":"imagine","description":"There are endless possibilities...","dm_permission":true,"options":[{{"type":3,"name":"prompt","description":"…","required":true}}]}}, "attachments":[]}}, "nonce":"{str(randint(10**18, (10**19)-1))}"}}\r\n------WebKitFormBoundaryovwotFdnidjPp7wJ--\r\n'.encode()
        
        response = requests.post('https://discord.com/api/v9/interactions', headers = headers, data = data)

    def get_image_urls(channel_id, token):

        headers = {
            
            'authorization': token

        }

        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'

        response = requests.get(url, headers = headers)

        return [message['attachments'][0]['url'] for message in response.json()]

    tokens = [
        'MTA5NTY2NTIxOTYxMjcwODkyNg.GvBoFX.sv3DgTs6K_oVkGc_XMVuF-4o6bxbemV9SHmV_M',
        'MTA5NTY2NTk0ODkzNTA4MjEwNg.Geohhf.BiVKaXZL8UykWIG8jziso5rAHayp4ccmm1FGHc',
        'MTA5NTcwMDk2MzkyMDE4MzQ1OA.GkTzsX.a9bp0qTJ_KmZvtD_fkSnPvkbwWOyresxH2mCpI',
        'MTA5NTcwMTYwMjMyNjgyNzAwOQ.GE0w92.OEvuPXDX4HKvygSg8-ikDEYGaeSM1lZN2PD9n8'
    ]

    guild_id = 1094231559428653056

    channel_ids = [
        1094621776547426354,
        1095671050794184714,
        1095672212071125042,
        1095672241053782127,
        # 1095672296527638588
    ]

    for channel_id in channel_ids:

        channel = await bot.fetch_channel(channel_id)

        await channel.purge(limit = 100)

        print(f'--> {channel.name} kanalı temizlendi.')

    print('\n--> Resimler oluşturuluyor....')

    for i in range(5):

        for j in range(5):

            imagine(prompt, guild_id, channel_ids[0], tokens[0])
            imagine(prompt, guild_id, channel_ids[1], tokens[1])
            imagine(prompt, guild_id, channel_ids[2], tokens[2])
            imagine(prompt, guild_id, channel_ids[3], tokens[3])


            await asyncio.sleep(3)

        await asyncio.sleep(20)

    await asyncio.sleep(20)

    print('\n--> Resimler oluşturuldu.')

    print('\n--> Resimler indiriliyor...\n')

    number = 0

    for i in range(len(channel_ids)):

        for url in get_image_urls(channel_ids[i], tokens[i]):

            while True:

                try:

                    image = Image.open(BytesIO(requests.get(url).content))

                    image.crop((0, 0, 512, 512)).save(f'images/image_{number + 1}.png')
                    print(f'--> images/image_{number + 1} kaydedildi.')

                    image.crop((512, 0, 1024, 512)).save(f'images/image_{number + 2}.png')
                    print(f'--> images/image_{number + 2} kaydedildi.')

                    image.crop((0, 512, 512, 1024)).save(f'images/image_{number + 3}.png')
                    print(f'--> images/image_{number + 3} kaydedildi.')

                    image.crop((512, 512, 1024, 1024)).save(f'images/image_{number + 4}.png')
                    print(f'--> images/image_{number + 4} kaydedildi.')

                    break

                except:

                    continue

            number += 4

#-------------------------------------------------- << RUN >> --------------------------------------------------#

bot.run(TOKEN)