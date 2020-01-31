import requests
import helper_functions
import globals
import sys


'''
Creates playlists with either every song the user 
has in a playlist somewhere or a playlist with
every song they have saved or saved in an album
'''

# My personal playlist ids/token/id from a separate file
oauth_token = globals.token
my_user_id = globals.my_user_id
all_music_playlist_ids = globals.all_music_playlist_ids
all_music_0 = globals.all_music_0
all_music_1 = globals.all_music_1
all_music_2 = globals.all_music_2
all_music_3 = globals.all_music_3
playlist_tracks_1 = globals.playlist_tracks_1
playlist_tracks_2 = globals.playlist_tracks_2
playlist_playlist_ids = globals.playlist_tracks_ids

def get_playlist_list():
    '''
    :return: A list of every id of a playlist
    created by the user and except for the playlists
    created by this script
    '''
    playlist_list = []
    # more_playlists and offset exist to deal with spotify's
    # limitations on how many playlists you can get at once
    more_playlists= True
    offset = 0
    while more_playlists:
        my_playlists_url = f'https://api.spotify.com/v1/users/{my_user_id}/playlists?limit=50&offset={offset}'
        response = requests.get(my_playlists_url, headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(oauth_token)})
        helper_functions.check_response(response)
        json_response = response.json()

        count = 0
        for i in json_response["items"]:
            if i["owner"]["id"] == my_user_id and i['id'] not in all_music_playlist_ids and i["id"] not in playlist_playlist_ids:
                playlist_list.append(i["id"])
            count = count + 1
        offset = offset + 50
        if count < 50:
            more_playlists = False
    return playlist_list

def get_all_playlist_tracks():
    '''
    Gets a the list of playlist ids, loops over them,
    and adds any track id not already in the list to it.
    :return: A list of every track id from every playlist
    '''
    all_playlist_tracks = []
    playlist_list = get_playlist_list()
    for playlist_id in playlist_list:
        all_playlist_tracks.extend(x for x in helper_functions.get_playlist_tracks(playlist_id) if x not in all_playlist_tracks)
    print('all playlist tracks gotten!')
    return all_playlist_tracks


def get_all_liked_tracks():
    '''
    :return: A list of every track id of every
    one of the user's liked/saved tracks
    '''
    all_liked_tracks = []
    more_tracks = True
    offset = 0
    while more_tracks:
        playlist_tracks_url = f'https://api.spotify.com/v1/me/tracks?limit=50&offset={offset}'
        response = requests.get(playlist_tracks_url, headers={"Content-Type": "application/json",
                                                              "Authorization": "Bearer {}".format(oauth_token)})
        helper_functions.check_response(response)
        json_response = response.json()

        count = 0
        for track in json_response["items"]:
            all_liked_tracks.append(track["track"]["uri"])
            count = count + 1
        offset = offset + 50
        if count < 50:
            more_tracks = False
    print("all liked tracks gotten!")
    return all_liked_tracks

def get_albums_list():
    '''
    :return: A list of every album id that
    the user has saved
    '''
    album_list = []
    more_albums= True
    offset = 0
    while more_albums:
        my_albums_url = f'https://api.spotify.com/v1/me/albums?limit=50&offset={offset}'
        response = requests.get(my_albums_url, headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(oauth_token)})
        helper_functions.check_response(response)
        json_response = response.json()

        count = 0

        for album in json_response["items"]:
            album_list.append(album["album"])
            count = count + 1
        offset = offset + 50
        if count < 50:
            more_albums = False
    return album_list


def get_album_tracks():
    '''
    :return: A list of every track id in
    every one of the user's saved albums
    '''
    all_album_tracks = []
    album_list = get_albums_list()
    for album in album_list:
        for track in album["tracks"]["items"]:
            all_album_tracks.append(track["uri"])
    print("all album tracks gotten!")
    return all_album_tracks

def split_tracklist_to_playlist_size_and_add(tracklist, playlist_id_list):
    '''
    Due to spotifys limits on playlist size (10,000) and limits
    on get/push sizes, this function takes a (long long long)
    list of tracks, splits it into playlist length then
    splits it into push lengths and adds each of those segments
    :param tracklist: the really long list of tracks
    :param playlist_id_list: a list of possible track ids to put
    the tracks into
    '''

    num_of_playlists = len(tracklist) // 10000 + 1
    for i in range(num_of_playlists):
        #makes a list
        start = (i * 10000)
        end = start + 9999
        #fills current_list with 10,000 tracks
        current_list = tracklist[start:end]
        # current_list_split is now a list of lists of 100 tracks
        current_list_split = helper_functions.split_track_list(100, current_list)

        playlist_id = playlist_id_list[i]
        helper_functions.add_list_of_tracklists_to_playlist(current_list_split, playlist_id)
        print(f"{i} playlist added")


def add_playlist_tracks():
    '''
    Gets all the playlist tracks and adds them into
    multiple playlists
    '''
    for playlist_id in playlist_playlist_ids:
        helper_functions.clear_playlist(playlist_id)
    all_playlist_tracks = get_all_playlist_tracks()
    print("list of all playlist tracks built")
    split_tracklist_to_playlist_size_and_add(all_playlist_tracks, playlist_playlist_ids)


def add_saved_tracks():
    '''
    Gets all the liked tracks/album tracks and
    adds them into multiple playlists
    '''
    for playlist_id in all_music_playlist_ids:
        helper_functions.clear_playlist(playlist_id)
    all_album_tracks = get_album_tracks()
    all_liked_tracks = get_all_liked_tracks()

    all_music_uri_list = all_liked_tracks
    all_music_uri_list.extend(x for x in all_album_tracks if x not in all_liked_tracks)
    print("all_music_uri_list built")

    split_tracklist_to_playlist_size_and_add(all_music_uri_list, all_music_playlist_ids)


# The part that actually runs
token_input = input("Do you need to enter a new token? y/n\n")
if token_input == "y":
    print("Get a token here: https://developer.spotify.com/console/get-users-profile/")
    oauth_token = input("Enter your new token below:\n")
    helper_functions.set_token(oauth_token)



user_input_1 = input("Would you like to make a playlist/s of all the songs in your playlists? y/n \n")
if user_input_1 == "y" or user_input_1 == "Y":
    print("this will probably take a few minutes... \nProgress Updates:")
    add_playlist_tracks()
user_input_2 = input("Would you like to make a playlist/s of all the songs in your library (both saved songs and albums)? y/n \n")
if user_input_2 == "y" or user_input_2 == "Y":
    print("this will probably take a few minutes... \nProgress Updates:")
    add_saved_tracks()
print("done")