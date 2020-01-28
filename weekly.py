import requests
import helper_functions
import globals
from datetime import datetime, timedelta


'''
Adds songs the user has liked that aren't in "last week's" 
playlist (and have been liked within the past two weeks.

(A lot of things here are fairly dependent on this being 
run once a week so such things as "last week's playlist"
actually exist)

future todos:
move rotating to archive
GET songs in rotating
filter by date added (over 1 month)
POST those to 2019 archive
DELETE them from rotating

'''
# My personal playlist ids/token/id from a separate file
my_user_id = globals.my_user_id
oauth_token = globals.token
rotating_id = globals.rotating_id
twenty_archive_id = globals.twenty_archive_id

def get_added_at_datetime(string):
    '''
    Takes a date/time string from spotify
    and converts it into a datetime object
    :param string: usually the "added_at" attribute of a track
    :return: the dt object
    '''
    datetime_obj = datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')
    return datetime_obj

def datetime_to_string(date):
    '''
    Converts a datetime object to my
    preferred date format (ex: "1/04/20")
    :param date: a datetime object
    :return: the formatted string
    '''
    last_week_str = date.strftime("%m/%d/%y")
    if last_week_str.startswith("0"):
        last_week_str = last_week_str[1:]
    return last_week_str

def get_last_weeks_playlist():
    '''
    Goes through the user's playlist to find the one created
    7 days ago (this is where it's important to actually have
    an aptly named playlist from a week ago). If no such playlist
    exists, it will prompt the user to input the playlist id of
    one to consider as "last week's"
    :return: the id of last week's playlist
    '''
    last_week_date = datetime.today() - timedelta(days=7)
    last_week_str = datetime_to_string(last_week_date)

    last_weeks_playlist_id = ""
    my_playlists_url = f'https://api.spotify.com/v1/users/{my_user_id}/playlists?limit=50'
    response = requests.get(my_playlists_url, headers={"Content-Type": "application/json",
        "Authorization": "Bearer {}".format(oauth_token)})
    helper_functions.check_response(response)
    json_response = response.json()

    for i in json_response["items"]:
        if i['name'] == last_week_str:
            last_weeks_playlist_id = i["id"]
    if last_weeks_playlist_id == "":
        last_weeks_playlist_id = input("There's been an issue, please enter the URI of last week's playlist: \n")
    return last_weeks_playlist_id



def get_saved_tracks_from_last_week():
    '''
    Gets a list of tracks saved within the last two weeks
    that also aren't on last week's playlist
    :return: the list of track ids
    '''
    saved_tracks = []
    last_weeks_tracks = helper_functions.get_playlist_tracks(get_last_weeks_playlist())
    two_weeks_ago = datetime.today() - timedelta(days=14)
    # more_playlists and offset exist to deal with spotify's
    # limitations on how many playlists you can get at once
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
            if track["track"]["uri"] not in last_weeks_tracks:
                if get_added_at_datetime(track["added_at"]) > two_weeks_ago:
                    saved_tracks.append(track["track"]["uri"])
                else: more_tracks = False
            else: more_tracks = False

            count = count + 1
        offset = offset + 50
        if count < 50:
            more_tracks = False
    return saved_tracks



# def get_old_rotating_tracks():
#     # old if over 1 month (28 days)
    #jkjk old if track is in playlist from 4 weeks ago
#     old_rotating_tracks = []
#     return old_rotating_tracks
#
# def delete_old_from_rotating(old_rotating_tracks):
#
#
# def add_to_archive(tracks_to_add):
token_input = input("Do you need to enter a new token? y/n\n")
if token_input == "y":
    print("Get a token here: https://developer.spotify.com/console/get-users-profile/")
    oauth_token = input("Enter your new token below:\n")

user_input = input("Would you like to make a playlist with your newly liked songs? y/n \n")
if user_input == "y" or user_input =="Y":
    playlist_id = helper_functions.create_playlist(datetime_to_string(datetime.today()))
    helper_functions.add_tracklist_to_playlist(get_saved_tracks_from_last_week(), playlist_id)
print("done")