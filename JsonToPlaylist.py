import pprint
import sys
import spotipy
import spotipy.util as util

"""
Takes a list of song names and artist and creates a spotify playlist.

Requires spotipy, which you can get here:
http://spotipy.readthedocs.io/en/latest/#
Follow instructions in shell and read comments in code!
Max songs added per run is 100. (Spotify API limit)
Remember to insert your information where comments indicate

Usage:
$ python JsonToPlaylist.py 'nameoffile' [offset]

Offset is for when you have lists for over 100 entries and need several runs.
E.G: First run is 0->99, then you set offset = 100, and it will grab 100->end

File should be Json or txt, formatted like this:
songname, artist
songname, artist
...

Do manual cleanup in working directory after use - it creates some cache!
"""

SPOTIPY_CLIENT_ID = 'xxxxxx'#Insert your ID here
SPOTIPY_CLIENT_SECRET = 'xxxxxx'#Insert your ID here
redir = 'http://www.example.com/'#just use this website, should be fine

scope = 'playlist-modify-public'
username = 'placeholder'#insert your username here
tracks = []
track_ids = []
use_ids = []
if len(sys.argv)<=1:
	sys.exit(0)
# File should be in this format:
# songname, artist
# songname, artist
# ...
file = sys.argv[1]

for line in open(file):
	#Error-handling print out
	#print(line)
	x, y = line.split(',')
	tracks.append(x + ' ' + y)

token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, redir)
if token:
	sp = spotipy.Spotify(auth=token)
	sp.trace = False

	for x in tracks:
		#search all of the results and add track ID's
		result = sp.search(q=x, type='track', limit=1)
		for i, t in enumerate(result['tracks']['items']):
			#Print for error-handling
			#print(t['id'])
			track_ids.append( t['id'])
		#Print for error-handling
		#pprint.pprint(result)
	
	#Printing for error-handling
	#print(track_ids)

	#Create playlist
	playlists = sp.user_playlist_create(username, 'Parse2Playlist')
	playlist_id = playlists['id']
	
	#Print errors
	#pprint.pprint(playlists)
	
	#API only takes 100 requests pr. authentication.
	#start-index
	var = 0
	
	if len(sys.argv) > 3:
		var = argv[2]
	
	var_org = var
	
	while var < len(track_ids):
		use_ids.append(track_ids[var])
		var = var + 1
		if var_org +100 > var:
			break

	#Add all the tracks found to the playlist
	final = sp.user_playlist_add_tracks(username, playlist_id, use_ids)
	#Prints so you can see it has finished
	print(final)
else:
	print("Can't get token for", username)