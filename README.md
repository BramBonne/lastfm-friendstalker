# Friendstalker for Last.fm
Program that allows you to see what your Last.fm friends are listening to in real-time.

Run with:
```
python friendstalker.py -u <your_lastfm_username>
```
Optional arguments:
```
  -h, --help            show this help message and exit
  --history HISTORY_TIME
                        number of seconds ago to display scrobbles from
                        (default: 600)
  --max_tracks MAX_TRACKS, -t MAX_TRACKS
                        maximum number of tracks in history to display per
                        friend (default: 10)
  --run_indefinitely    Keep running (default: False)
  --colorize, -c        Colorize terminal output (default: False)
```
