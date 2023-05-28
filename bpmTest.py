import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
CLIENT_ID = 'your client id'
CLIENT_SECRET = 'your client secret'
REDIRECT_URI = 'your redirect uri'
USERNAME = 'your spotify user (id from share link)'

# Initialize the Spotify API client
scope = 'user-library-read playlist-modify-private playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope,
                                               username=USERNAME))

# Get all liked songs from the user's library
liked_songs = sp.current_user_saved_tracks(limit=50)  # Increase the limit as per your requirement

# Define the playlist IDs for the respective BPM ranges
#Create as many playlists and BPM ranges as you like to change level of granularity
playlist_ids = {
    '0-50bpm': 'playlist 1 id',
    '50.01-85bpm': 'playlist 2 id',
    '85.01-100bpm': 'playlist 3 id',
    '100.01-110bpm': 'playlist 4 id',
    '110.01-115bpm': 'playlist 5 id',
    '115.01-150bpm': 'playlist 6 id'
}

# Loop through each liked song
for song in liked_songs['items']:
    track = song['track']
    track_details = sp.audio_features(track['id'])[0]
    bpm = track_details['tempo']

    # Find the appropriate playlist based on the tempo range
    for playlist_name, playlist_id in playlist_ids.items():
        playlist_bpm_range = playlist_name[:-3]  # Remove the 'bpm' suffix
        min_bpm, max_bpm = map(float, playlist_bpm_range.split('-'))
        if min_bpm <= bpm <= max_bpm:
            sp.playlist_add_items(playlist_id, [track['uri']])
            break

print("Songs added to the respective playlists based on tempo.")
