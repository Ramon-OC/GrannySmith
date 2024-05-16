import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = 'tu_cliente_id'
client_secret = 'tu_token_cliente'
csv_file = 'Canciones.csv' # Limited for 100 songs
redirect_uri = 'http://localhost:8888/callback'

scope = 'playlist-modify-public' # Modify this if u need it private 
# scope = 'playlist-modify-private'
playlist_name = 'CSV playlist'
description = 'Lista creada con un CSV simple de Itunes [Canción, Artista]'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

username = sp.current_user()['id']

playlist = sp.user_playlist_create(user=username, name=playlist_name, public=True, description= description)

def get_track_ids_from_csv(csv_file):
    track_ids = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            track_name, artist_name = row
            query = f'track:{track_name} artist:{artist_name}'
            result = sp.search(q=query, type='track', limit=1)
            tracks = result['tracks']['items']
            if tracks:
                track_ids.append(tracks[0]['id'])
    return track_ids


track_ids = get_track_ids_from_csv(csv_file)
if track_ids:
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids)
    print(f'La playlist "{playlist_name}" fue creada con éxito!')
else:
    print('No se encontraron canciones para agregar a la playlist.')

