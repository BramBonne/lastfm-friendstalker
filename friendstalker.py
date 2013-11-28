__author__ = 'Bram Bonne <bram.bonne+friendstalker@gmail.com>'
API_KEY = "53195f6f87c0e19f487bdd98998799f4"
API_SECRET = ""

import pylast
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from time import time, ctime, sleep

class Scrobble:
    def __init__(self, timestamp, user, track):
        self.timestamp = int(timestamp)
        self.user = user
        self.track = track

parser = ArgumentParser(description="Show your friends' last scrobbles on Last.fm",
                                 formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--username', '-u', dest='username', help='your Last.fm username', type=str, default='megooz')
parser.add_argument('--history', dest='history_time', help='number of seconds ago to display scrobbles from', type=int, default=600)
parser.add_argument('--max_tracks', '-t', dest='max_tracks', help='maximum number of tracks to display per friend', type=int, default=3)
parser.add_argument('--run_indefinitely', action='store_true', dest='run_indefinitely', default=False)
args = vars(parser.parse_args())

network = pylast.get_lastfm_network(api_key=API_KEY, api_secret=API_SECRET)
user = network.get_user(args['username'])
friends = user.get_friends()
while args['run_indefinitely']: # Keep running if this switch is on
    scrobbles = []
    for friend in friends:
        tracks = friend.get_recent_tracks(args['max_tracks'])
        for played_track in tracks:
            # Only keep scrobble if it's recent enough
            if int(played_track.timestamp) > time() - args['history_time']: # Less than 10 minutes ago
                scrobbles.append(Scrobble(played_track.timestamp, friend, played_track.track))

    print chr(27) + "[2J" # Clear screen
    # Print all recent scrobbles
    for scrobble in sorted(scrobbles, key=lambda s: s.timestamp, reverse=True):
        friendname = scrobble.user.get_name()
        artist = scrobble.track.get_artist()
        title = scrobble.track.get_title()
        timestring = ctime(scrobble.timestamp)
        print "%s: %s - %s (%s)" % (friendname, artist, title, timestring)
    if args['run_indefinitely']:
        sleep(10) # Limit API calls