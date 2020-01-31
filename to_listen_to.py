import requests
import datetime
import helper_functions
import globals

'''
Makes a new playlist (or updates and existing one) with all 
the songs from three playlists (for me: my discover weekly,
my release radar, and new music friday).
'''
oauth_token = globals.token
my_user_id = globals.my_user_id

discover_weekly_id = globals.dw_id
relase_radar_id = globals.rr_id
new_music_friday_id = globals.nmf_id
to_listen_to_id = globals.to_listen_to_id

# Formats the date to be used as the playlist description
def todays_date():
    now = datetime.datetime.now()
    return f'{now.month}/{now.day}/{now.year}'


def totalList(track_list_1, track_list_2, track_list_3) :
    '''
    Combines the three tracklists into one list of track ids
    :param track_list_1:
    :param track_list_2:
    :param track_list_3:
    :return: The list of all track ids
    '''
    total_track_list = []
    for track_id in track_list_1:
        total_track_list.append(track_id)
    for track_id in track_list_2:
        if track_id not in total_track_list:
            total_track_list.append(track_id)
    for track_id in track_list_3:
        if track_id not in total_track_list:
            total_track_list.append(track_id)
    return total_track_list


def to_listen_complete():
    '''
    Runs everything to get all the tracks and add them into a playlist
    :return:
    '''
    discover_tracklist = helper_functions.get_playlist_tracks(discover_weekly_id)
    release_tracklist = helper_functions.get_playlist_tracks(relase_radar_id)
    new_music_tracklist = helper_functions.get_playlist_tracks(new_music_friday_id)
    total_list = totalList(discover_tracklist, release_tracklist, new_music_tracklist)
    split_list = helper_functions.split_track_list(50, total_list)
    helper_functions.add_list_of_tracklists_to_playlist(split_list, to_listen_to_id, True)

token_input = input("Do you need to enter a new token? y/n\n")
if token_input == "y":
    print("Get a token here: https://developer.spotify.com/console/get-users-profile/")
    oauth_token = input("Enter your new token below:\n")
    helper_functions.set_token(oauth_token)


user_input = input("Would you like to make a to Listen to playlist? y/n \n")
if user_input == "y" or user_input == "Y" :
    helper_functions.clear_playlist(to_listen_to_id)
    to_listen_complete()
print("done")