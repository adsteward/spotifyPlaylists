import requests
import helper_functions
# import all_music
import globals
'''
1. get song title and artist
2. generate list of playlist songs 
3. find matches and add return list with name of playlists
GET https://api.spotify.com/v1/search
'''


def get_track(title, artist):
    search_endpoint = f'https://api.spotify.com/v1/search?q={title}%20artist:{artist}&type=track'
    response = requests.get(search_endpoint, headers={"Content-Type": "application/json",
                                                          "Authorization": "Bearer {}".format(globals.token)})
    helper_functions.check_response(response)
    json_response = response.json()
    return json_response['tracks']["items"][0]["uri"]




tracks_playlists = []
title = input("What's the name of the song? \n")
artist = input("who is the artist?\n")
track_uri = get_track(title, artist)
print("track gotten")
print(track_uri)
list_of_playlists = helper_functions.get_playlist_list()
print("list gotten")
i = 0
for playlist in list_of_playlists:
    print(f'{i + 1} down...')
    if track_uri in helper_functions.get_playlist_tracks(playlist):
        tracks_playlists.append(playlist)
        print(playlist)
    i = i +1
print(tracks_playlists)

'spotify:track:7CfIX8LSukzEHvbV82WDWz'