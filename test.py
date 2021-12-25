import os
path = 'playlists'

files = '\n'.join([f[:-4] for f in os.listdir(path)])

print(files)