import requests
import json
import globals
'''
Various functions used across the scripts
    1. split_track_list(limit, track_list)
    2. add_tracklist_to_playlist(track_list, playlist_id, replace_tracks=False)
    3. add_list_of_tracklists_to_playlist(list_of_track_lists, playlist_id="", replace_tracks=False)
    4. clear_playlist(playlist_id)
    5. get_playlist_tracks(playlist_id, include_duplicates=False)
    6. create_playlist(name, description="", public=False)
    7. check_response(response):
    
'''

def split_track_list(limit, track_list):
    '''
    Splits a list of tracks into a list of lists of length limit
    :param limit: how long to make each mini-list
    :param track_list: the list of tracks to split up
    :return: A list of lists of tracks
    '''
    num_of_lists = len(track_list) // limit + 1
    split_list = []
    for i in range(num_of_lists + 1):
        if len(track_list) > limit:
            split_list.append(track_list[:limit])
            del track_list[:limit]
        else:
            split_list.append(track_list)
    return split_list


def add_tracklist_to_playlist(track_list, playlist_id, replace_tracks=False):
    '''
    Adds one list of tracks to a playlist.
    :param track_list: the list of track ids to add
    :param playlist_id: the playlist to add them to
    :param replace_tracks: whether or not to replace all
    existing tracks in the playlist (or to add the new
    ones to the existing)
    :return: nothin'
    '''
    if replace_tracks:
        clear_playlist(playlist_id)

    playlist_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    request_body = json.dumps({
        "uris": track_list
    })
    response = requests.post(url=playlist_endpoint,
                            data=request_body,
                            headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer {}".format(globals.token)})
    check_response(response)



def add_list_of_tracklists_to_playlist(list_of_track_lists, playlist_id, replace_tracks=False):
    '''
    Just a loop to add a list of lists of track ids to a playlist
    :param list_of_track_lists:
    :param playlist_id:
    :param replace_tracks:
    :return:
    '''
    for list in list_of_track_lists:
        add_tracklist_to_playlist(list, playlist_id, replace_tracks)

def clear_playlist(playlist_id, tracks_to_delete=[]):
    '''
    Deletes all the songs in a playlist.
    Once again, the while loop is to deal with spotify's
    limits but in this case they had no specified limits
    for delete so I just guessed (this could also be because
    of a more general "pipe size" issue)
    :param playlist_id: the playlist from which to delete
    :return: nothin'
    '''
    if len(tracks_to_delete) == 0:
        tracks_to_delete = get_playlist_tracks(playlist_id, include_duplicates=True)
    more_tracks = True
    while more_tracks:
        playlist_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        request_body = json.dumps({
            "uris": tracks_to_delete[:99]
        })
        response = requests.delete(url=playlist_endpoint,
                               data=request_body,
                               headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(globals.token)})
        check_response(response)
        tracks_to_delete = tracks_to_delete[99:]
        if len(tracks_to_delete) < 100:
            more_tracks = False


def get_playlist_tracks(playlist_id, include_duplicates=False):
    '''
    Gets all of the tracks of a certain playlist
    :param playlist_id: the playlist to get tracks from
    :param include_duplicates: whether or not to keep any duplicate
    tracks in the playlist
    :return: A list of all the tracks in a playlist
    '''
    playlist_tracks = []
    # more_playlists and offset exist to deal with spotify's
    # limitations on how many playlists you can get at once
    more_tracks = True
    offset = 0
    while more_tracks:
        playlist_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100&offset={offset}'
        response = requests.get(playlist_tracks_url, headers={"Content-Type": "application/json",
                                                              "Authorization": "Bearer {}".format(globals.token)})
        check_response(response)
        json_response = response.json()

        count = 0
        #print(json_response)
        for track in json_response["items"]:
            if not include_duplicates:
                if track["track"]["uri"] not in playlist_tracks:
                    playlist_tracks.append(track["track"]["uri"])
            else :
                playlist_tracks.append(track["track"]["uri"])
            count = count + 1
        offset = offset + 100
        if count < 100:
            more_tracks = False
    return playlist_tracks

def create_playlist(name, description="", public=False):
    '''
    Creates a new playlist
    :param name:
    :param description:
    :param public:
    :return: the newly created playlist's id
    '''
    playlists_endpoint = f"https://api.spotify.com/v1/users/{globals.my_user_id}/playlists"
    request_body = json.dumps({
        "name": name,
        "description": description,
        "public": public
    })
    response = requests.post(url=playlists_endpoint, data = request_body,
                             headers={"Content-Type":"application/json",
                            "Authorization":"Bearer {}".format(globals.token)})

    check_response(response)
    return response.json()['id']

def get_playlist_by_name(playlist_name):
    '''
    Goes through the user's playlist to find the one
    named "playlist_name"
    :return: the id of that playlist
    '''

    last_weeks_playlist_id = ""
    my_playlists_url = f'https://api.spotify.com/v1/users/{globals.my_user_id}/playlists?limit=50'
    response = requests.get(my_playlists_url, headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(globals.token)})
    check_response(response)
    json_response = response.json()

    for i in json_response["items"]:
        if i['name'] == playlist_name:
            last_weeks_playlist_id = i["id"]
    if last_weeks_playlist_id == "":
        last_weeks_playlist_id = input("Playlist not found, please enter the URI of the playlist you're looking for: \n")
    return last_weeks_playlist_id

def check_response(response):
    '''
    raises an error if the request hasn't worked for whatever reason
    :param response:
    :return:
    '''
    if response.status_code != 200 and response.status_code != 201:
        raise ValueError(f"Error: response.status_code = {response.status_code}")

