import pprint
import sys

import spotipy
import spotipy.util as util
import simplejson as json
import aiy.audio

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

scope = 'user-read-playback-state, user-modify-playback-state, user-read-recently-played'
token = util.prompt_for_user_token(username, scope)

if token:
    #print(token)
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    devices = sp.devices()
    #print(json.dumps(devices, sort_keys=True, indent=4))
    #print(json.dumps(devices['devices'][0]['id'], sort_keys=True, indent=4))
    try:
        device1 = devices['devices'][0]['id']
    except:
        print("No devices!")

    while True:
        print()
        print("1. Play")
        print("2. Pause")
        print("3. Recent tracks")
        print("4. Quit")
        print()
        userchoice = input("Select: ")

        if userchoice=="1":
            try:
                sp.start_playback(device_id=device1, context_uri=None, uris=None, offset=None)
            except:
                pass

        if userchoice=="2":
            try:
                sp.pause_playback(device_id=device1)
            except:
                pass

        if userchoice=="3":
            print()
            top50 = sp.current_user_recently_played(20)
            for i, trackobj in enumerate(top50['items']):
                print(i + 1, ":", trackobj['track']['name'], "//", trackobj['track']['artists'][0]['name'])
            print()
            topchoice = input("Select: ")

            try:
                sp.stop_playback(device_id=device1, context_uri=None, uris=None, offset=None)
            except:
                pass

            try:
                sp.start_playback(device_id=device1, context_uri=None, uris=[top50['items'][int(topchoice) - 1]['track']['uri']], offset=None)
            except:
                pass

        if userchoice=="4":
            break


    #sp.start_playback(device_id=device1, context_uri=None, uris=None, offset=None)
    #    results = sp.current_user_top_tracks(time_range=range, limit=50)
    #    for i, item in enumerate(results['items']):
    #        print (i, item['name'], '//', item['artists'][0]['name'])
    #    print

else:
    print("Can't get token for", username)
