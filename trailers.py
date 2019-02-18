import configparser
import os

from plexapi.server import PlexServer
import youtube_dl

CONFIG = configparser.ConfigParser()
CONFIG.read("trailers.ini")

PLEX = PlexServer(CONFIG['Plex']['baseURL'], CONFIG['Plex']['token'])
SETTINGS = PLEX.settings.get('CinemaTrailersPrerollID')
OPTS = {
    'playlistend': CONFIG['General'].getint('playlist_end'),
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '{}/%(title)s.%(ext)s'.format(CONFIG['General']['save_path']),
}
with youtube_dl.YoutubeDL(OPTS) as ydl:
    ydl.download([CONFIG['General']['youtube_playlist_url']])
TRAILERS = map(lambda trailer: '{}/{}'.format(CONFIG['General']['save_path'], trailer),
               os.listdir(CONFIG['General']['save_path']))
TRAILERS = ';'.join(TRAILERS)

SETTINGS.set(TRAILERS)
PLEX.settings.save()
