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
parser.add_argument('--username', '-u', dest='username', help='your Last.fm username', type=str, required=True)
parser.add_argument('--history', dest='history_time', help='number of seconds ago to display scrobbles from', type=int, default=600)
parser.add_argument('--max_tracks', '-t', dest='max_tracks', help='maximum number of tracks in history to display per friend', type=int, default=10)
parser.add_argument('--run_indefinitely', action='store_true', dest='run_indefinitely', help='Keep running', default=False)
parser.add_argument('--colorize', '-c', action='store_true', dest='colorize', help='Colorize terminal output', default=False)
args = vars(parser.parse_args())

print "Getting your friends..."
network = pylast.get_lastfm_network(api_key=API_KEY, api_secret=API_SECRET)
user = network.get_user(args['username'])
friends = user.get_friends()
friends.append(user)
prev_scrobbles = set()

print "Getting recent scrobbles..."
while True: # Keep running if the 'run_indefinitely' command line switch is on
    scrobbles = []
    for friend in friends:
        try:
            tracks = friend.get_recent_tracks(args['max_tracks'])
        except Exception as e:
            # API error. Skip this update (might cause out-of-order scrobbles later, but is better than starting the round over)
            continue
        for played_track in tracks:
            # Only keep scrobble if it's recent enough
            timestamp = int(played_track.timestamp)
            if timestamp > time() - args['history_time'] and repr(played_track) not in prev_scrobbles:
                prev_scrobbles.add(repr(played_track)) # Print every scrobble only once
                scrobbles.append(Scrobble(played_track.timestamp, friend, played_track.track))

    # Print all recent scrobbles
    for scrobble in sorted(scrobbles, key=lambda s: s.timestamp): # Sort them by timestamp
        friendname = scrobble.user.get_name().encode('utf-8')
        artist = scrobble.track.get_artist().get_name().encode('utf-8')
        title = scrobble.track.get_title().encode('utf-8')
        timestring = ctime(scrobble.timestamp)
        if args['colorize']:
            print "\033[41m%s \033[43m %s - %s \033[46m %s\033[0m" % (friendname, artist, title, timestring)
        else:
            print "%s: %s - %s (%s)" % (friendname, artist, title, timestring)
    if args['run_indefinitely']:
        sleep(10) # Limit API calls
    else:
        break