
from youtubesearchpython import *

playlist = None

link = 'https://www.youtube.com/watch?v=bgsmr7t8zGE&list=PL90uWKIpHUob7f4raEOR_n1i_isnMyE5V'

if not 'playlist?' in link:
    ind = link.index('list=')
    link = link[ind+5:]

    if '&index=' in link:
        ind = link.index('&index=')
        link = link[:ind]

    link = f'https://www.youtube.com/playlist?list={link}'



print(link)


try:
    playlist = Playlist(link)
except:
    print('che bl')
while True:
    for igor in playlist.videos:
        if '&list=' in igor['link']:
                ind = igor['link'].index('&list=')
                igor['link'] = igor['link'][:ind]
        print(igor['link'])

    if not playlist.hasMoreVideos:
        break

    playlist.getNextVideos()
