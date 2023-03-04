from types import NoneType

import msender
from youtubesearchpython import VideosSearch, Video, ResultMode, Playlist
import yt_dlp as youtube_dl
import os
import discord
import asyncio
import re
from datetime import datetime
import subprocess

# TODO repeat tpggle
# TODO add now playing

past_q = []

instances = []


# controls


async def play(bot, link, message, play_top=False, no_message=False):
    global vc, state, total_songs, q, link_queue

    if state == 2:
        await pause(message)
    if not link == '':

        vc = await join(bot, message)
        if vc == None:
            return 1

        file = ''

        if link.startswith("https://"):
            if 'list=' in link:
                await play_yt_playlist(bot, link, message)
                return 0
            else:
                file = await get_title(link)

        else:
            link = await youtube_search(link)
            file = await get_title(link)

        if not os.path.exists(file):
            await download(link, file)

        if not play_top and len(q) > 0:
            q.append(file)
            link_queue.append(link)
        else:
            q.insert(pos + 1, file)
            link_queue.insert(pos + 1, link)

        total_songs += 1
        if not no_message:
            await msender.send(f"{q.index(file) + 1}. {file[6:-4]}", message.channel)


        await queue_code() # because yt_dlp freezes shit

        return 0


async def pause(message):
    global state, vc, pause_time, song_start_time

    if state == 0:
        await msender.send("Так ниче не играет 😳", message.channel)

    elif state == 1:
        state = 2
        vc.pause()

        pause_time = datetime.now()

        await msender.send("Пауза так пауза", message.channel)

    elif state == 2:
        state = 1

        delta = datetime.now() - pause_time
        song_start_time = song_start_time + delta

        vc.resume()
        await msender.send("Включаем", message.channel)


async def stop(bot=None, message=None):
    if message == None:
        try:
            vc
        except NameError:
            return
        else:
            await vc.disconnect()
            await init()
            return

    for i in bot.voice_clients:
        if i.guild == message.guild:
            await i.disconnect()
            await msender.send('Ладно, давай', message.channel)
            break
    await init()


async def volume_(vol, message, bot):
    global volume
    if vol == '':
        await msender.send(f"Текущая громкость: {volume}", message.channel)
    else:
        volume = float(vol) * 0.01
        vc.source.volume = volume
        await msender.send(f"Громкость {int(vc.source.volume * 100)}", message.channel)


# playlists


async def list_playlist(name, message, bot):
    path = 'playlists'
    filepath = f'playlists/{name}.txt'

    if name == '':
        files = '\n'.join([f[:-4]
                          for f in os.listdir(path) if f.endswith('.txt')])
        await msender.send_long(str(files), message.channel, title='Плейлисты:\n\n')
    else:
        if not os.path.exists(filepath):
            await msender.send('Такого плейлиста нет', message.channel)
        else:
            with open(filepath, 'r', encoding='utf-8') as file:
                songs = file.read()
                await msender.send_long(str(songs), message.channel, title=f'Плейлист {name}:')


async def save_playlist(name, message):
    if name == "":
        await msender.send("А название?!??!?!", message.channel)
        return

    with open(f'playlists/{name}.txt', 'w', encoding="utf-8") as file:
        file.write("\n".join([i[6:-4] for i in q]))

    with open(f'playlists/{name}.links', 'w', encoding="utf-8") as file:
        file.write("\n".join([i for i in link_queue]))

    await msender.send(f"Плейлист '{name}' сохранен", message.channel)


async def play_playlist(name, message, bot):
    if name == "":
        await msender.send("А название?!??!?!", message.channel)
        return

    txt = f'playlists/{name}.txt'
    links = f'playlists/{name}.links'

    if os.path.isfile(links):
        with open(txt, 'r', encoding="utf-8") as file:
            await msender.send_long(file.read(), message.channel, f"Включаю плейлист {name}")

        with open(links, 'r', encoding="utf-8") as file:
            asd = file.read().split('\n')

            for i in asd:
                s = await play(bot, i, message, no_message=True)
                if s == 1:
                    return

        await msender.send(f"Загрузка плейлиста '{name}' завершена", message.channel)

    else:
        await msender.send('Нет такого плейлиста', message.channel)


async def play_yt_playlist(bot, link, message):
    playlist = None
    print('playlist detected')

    if not 'playlist?' in link:
        print('shitty link detected')
        ind = link.index('list=')
        link = link[ind+5:]

        if '&index=' in link:
            ind = link.index('&index=')
            link = link[:ind]

        link = f'https://www.youtube.com/playlist?list={link}'

    try:
        playlist = Playlist(link)
    except:
        await msender.send('Плейлист не найден', message.channel)
        return

    while True:
        for igor in playlist.videos:
            if '&list=' in igor['link']:
                ind = igor['link'].index('&list=')
                igor['link'] = igor['link'][:ind]

            await play(bot, igor['link'], message, no_message=True)
            print('adding song')

        if not playlist.hasMoreVideos:
            print('ed songs')
            break

        playlist.getNextVideos()
        print('getting more')

    await msender.send('Загрузка плейлиста завершена', message.channel)


async def del_playlist(name, message):
    path = f'playlists/{name}'
    deleted = 0
    if os.path.isfile(path + '.txt'):
        os.remove(path + '.txt')
        deleted += 1
    if os.path.isfile(path + '.links'):
        os.remove(path + '.links')
        deleted += 1

    if deleted == 2:
        await msender.send(f'Удалил плейлист {name}', message.channel)
    elif deleted == 1:
        await msender.send(f'Удалил плейлист {name} (Старый формат)', message.channel)
    elif deleted == 0:
        await msender.send(f'Такого плейлиста я не нашел(', message.channel)
    else:
        await msender.send(f'че блять? ты как сюда попал? вове сообщи это баг', message.channel)


# queue stuff


async def remove(song_id, message):
    global pos, current, total_songs, q, link_queue
    song_id = int(song_id) - 1

    if song_id >= 0 and song_id <= len(q):
        if song_id <= pos:
            if song_id == pos:
                await skip()
            total_songs -= 1
            pos -= 1
            current -= 1

        await msender.send(f"Удаляем {q[song_id][6:-4]}", message.channel)
        q.pop(song_id)
        link_queue.pop(song_id)
        if total_songs == 0:
            if vc.is_playing():
                vc.stop()
            await init()

    else:
        await msender.send("Такой песни нету", message.channel)


async def queue():
    while True:
        await queue_code()
        await check_disconnect()

async def queue_code():
    global q, pos, current, state
    
    if not q == [] and not state == 2:
        if not vc.is_playing() and state == 1:
            if len(q) == 1:
                await play_file(vc, q[current])
            else:
                await skip()

        if not current == pos:
            current = pos

            await play_file(vc, q[current])
    await asyncio.sleep(1)

async def check_disconnect():
    if state == 0:
        return

    try:
        vc
    except NameError:
        await stop()
    else:

        # check if bot was disconnected by hand
        if not vc.is_connected():
           await stop()
           print('someone disconnected me :(')

        # check if only the bot is connected
        if len(vc.channel.voice_states) < 2:
            print('im the only one in the channel :( imma leave')
            await stop()


async def print_queue(message):
    if q == []:
        await msender.send("Очередь пустая а шо", message.channel)
    else:
        song_name = f'{pos + 1}. {q[pos][6:-4]}'

        emb = discord.Embed(
            title=f'Сейчас играет: \n {song_name} ({await get_time_str()})')
        emb.color = discord.Color.from_rgb(255, 166, 201)
        emb.add_field(name='Очередь:', value="\n".join(
            [f'{i+1}. ' + q[i][6:-4] for i in range(len(q))]))
        await message.channel.send(embed=emb)


async def print_past_queue(message):
    if past_q == []:
        await msender.send("Очередь пустая а шо", message.channel)
    else:
        emb = discord.Embed(
                title=f'Вот что играло пораньше:')
        for i in past_q:
            emb.add_field(name='-----', value="\n".join(
                [f'{k+1}. ' + i[k][6:-4] for k in range(len(i))]))
        await message.channel.send(embed=emb)



async def now_playing(message):
    if q == []:
        await msender.send("А ниче не играет", message.channel)
    else:
        song_name = f'{pos + 1}. {q[pos][6:-4]}'

        emb = discord.Embed(
            title=f'Сейчас играет: \n {song_name} ({await get_time_str()})')
        emb.color = discord.Color.from_rgb(255, 166, 201)

        await message.channel.send(embed=emb)



async def skip(num=None, message=None):
    global pos, total_songs
    if num == None:
        pos += 1
        if pos > total_songs - 1:
            pos = 0
    else:
        num = int(num)
        if num <= total_songs and num > 0:
            pos = num - 1
            await msender.send(f'Включаю трек {q[num - 1][6:-4]}', message.channel)
        else:
            await msender.send('Такой цифры в очереди нету', message.channel)


async def back(message):
    if pos == 0:
        await skip(num=total_songs, message=message)
    else:
        await skip(num=pos, message=message)


async def next(message):
    await skip(num=(pos + 2) % total_songs, message=message)


async def clear_queue(message):
    await init()
    try:
        if vc.is_playing():
            vc.stop()
    except Exception as e:
        print(e)
    finally:
        await msender.send('Очистил очередь', message.channel)


# technical stuff


async def init():
    global pos, q, past_q, current, total_songs, state, volume, link_queue, song_start_time, pause_time, song_len
    try:
        if q:
            pass
    except:
        q = []

    if len(q) > 0:
        past_q.append(q)
    if len(past_q) > 3:
        past_q.pop(0)
    
    q = []
    link_queue = []
    song_start_time = datetime.now()
    pause_time = datetime.now()
    song_len = 0
    pos = 0
    total_songs = 0
    current = -1
    volume = 1.0
    state = 0  # 0 stopped, 1 playing, 2 pause


async def play_file(vc, file):
    global state, song_start_time, song_len
    if vc.is_playing():
        vc.stop()

    song_len = await get_song_length(file)

    vc.play(discord.FFmpegPCMAudio(file))
    # ,after=lambda e: print('done', e))
    vc.source = discord.PCMVolumeTransformer(vc.source, volume=volume)
    song_start_time = datetime.now()

    state = 1
    print(f'started playing "{file[6:-4]}"')


async def get_song_length(file):
    args = ("ffprobe", "-show_entries", "format=duration", "-i", file)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

    # windows method
    song_len = str(popen.stdout.read())[21:-18]
    song_len = int(float(song_len))

    print('SONG LEN:' + str(song_len))

    return song_len


async def get_time_played():
    st = datetime.now() - song_start_time
    st = st.total_seconds()
    if state == 2:
        st = st - pause_time
    return st


async def get_time_str():
    played = await get_time_played()
    hrs = int(song_len / 60 / 60)
    mins = int(song_len / 60 - hrs * 60)
    sec = int(song_len % 60)

    hrsp = int(played / 60 / 60)
    minsp = int(played / 60 - hrsp * 60)
    secp = int(played % 60)

    if hrs > 0:
        stime = f'{hrs}:{mins:02}:{sec:02}'
    else:
        stime = f'{mins}:{sec:02}'
    if hrsp > 0:
        ptime = f'{hrsp}:{minsp:02}:{secp:02}'
    else:
        ptime = f'{minsp}:{secp:02}'

    return f'{ptime} / {stime}'


async def join(bot, message) -> discord.VoiceClient:
    # if author is not in vc return
    if type(message.author.voice) == NoneType:
        await msender.send('Вы не в голосовом канале', message.channel)
        return None
    
    # this has to be reworked at some point
    for i in bot.voice_clients:
        if i.guild == message.guild:
            if bot.user in message.author.voice.channel.members:
                return i
            else:
                await i.move_to(message.author.voice.channel)
                return i

    vc = await message.author.voice.channel.connect()
    print('joined')
    return vc


async def download(video_url, filename):

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
        'ratelimit': 100000000,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    return filename


async def youtube_search(prompt: str):
    videosSearch = VideosSearch(prompt, limit=2)
    vid = dict(videosSearch.result())["result"][0]['id']
    return f'https://www.youtube.com/watch?v={vid}'


async def get_title(link):
    vid = Video.get(link, mode=ResultMode.json)
    title = vid['title']
    title = 'queue/' + re.sub(r'[\|/,:&$#"]', '', title) + '.mp3'

    return title
