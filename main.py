import toListenTo
import allMusic
import weekly



if __name__ == '__main__':
    print("running scripts now")
    a1 = input("Would you like to make a to Listen to playlist? y/n \n")
    if a1 == "y" or a1 == "Y" :
        toListenTo.to_listen_complete()
    a4 = input("Would you like to make a playlist with your newly liked songs? y/n \n")
    if a4 == "y" or a4 =="Y":
        weekly.run_weekly()
    a2 = input("Would you like to make a playlist/s of all the songs in your playlists? y/n \n")
    if a2 == "y" or a2 == "Y":
        print("this will probably take a few minutes... \nProgress Updates:")
        allMusic.add_playlist_tracks()
    a3 = input("Would you like to make a playlist/s of all the songs in your library (both saved songs and albums)? y/n \n")
    if a3 == "y" or a3 == "Y":
        print("this will probably take a few minutes... \nProgress Updates:")
        allMusic.add_saved_tracks()

    print("done")



