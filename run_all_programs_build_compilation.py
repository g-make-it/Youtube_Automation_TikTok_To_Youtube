from get_videos_from_tiktok import FetchVideos
from join_videos_together import CreateCompilation
from make_thumbnails import BuildThumbnail

song_directory = './songs_directory/'

def save_songs_we_have_used(song):
    global song_directory
    with open(song_directory + 'songs_used.txt', 'a') as f:
        f.write('\n'+song)
    print(f'{song} saved')

# load in data
def get_list_from_files():
    global song_directory
    f = open(song_directory+'songs_used.txt', 'r')
    set_of_songs_we_have_used = set(f.read().split('\n'))

    f = open(song_directory+'songs.txt', 'r')
    songs = (f.read().split('\n'))
    return songs, set_of_songs_we_have_used

songs, set_of_songs_we_have_used = get_list_from_files()
fv = FetchVideos()
cc = CreateCompilation()
bt = BuildThumbnail()

# one song per day
for song in songs:
    if song in set_of_songs_we_have_used:
        continue
    fv.run(song)
    try:
        cc.run(song)
    except Exception as e:
        print(e, 'error occurred when joining videos together')
    try:
        bt.run(song)
    except Exception as e:
        print(e, 'error occurred when creating the thumbnails')
    save_songs_we_have_used(song)
    break

