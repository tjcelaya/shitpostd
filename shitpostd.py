from os import environ
from sys import exit
import time
import re
from slackclient import SlackClient
import giphy_client
from giphy_client.rest import ApiException

RTM_READ_DELAY = 1
GIPHY_CLIENT = giphy_client.DefaultApi()
SLACK_CLIENT = SlackClient(environ.get('SLACK_BOT_ACCESS_TOKEN'))

if not SLACK_CLIENT.rtm_connect(with_team_state=False):
    print('failed to connect')
    exit(1)

print('connected')
USER_ID = SLACK_CLIENT.api_call("auth.test")["user_id"]

def extract_words(e):
    return e['channel'], e['text'].split()

def is_chatter_and_not_us(e):
    return (e is not None
            and 'type' in e 
            and e['type'] == 'message' 
            and 'user' in e 
            and e['user'] != USER_ID)

def build_shitpost(words):
    while len(words) is not 0:
        print('searching: [', '%20'.join(words), ']')
        results = GIPHY_CLIENT.gifs_search_get(
                environ.get('GIPHY_API_KEY'),
                '%20'.join(words))
        
        if len(results.data) == 0:
             words.pop(randint(0, len(words)-1))
             continue

        return results.data[0].images.original.url

    return 'I got nothin'

while True:
    words_by_channel = dict()
    for e in SLACK_CLIENT.rtm_read():
        print('e: ', e)
        if not is_chatter_and_not_us(e):
            continue
        print('it wasnt chatter')

        chan, words = extract_words(e)
        print('from chan', chan, 'got words: ', words)
        if len(words) is 0:
            continue

        current_words = words_by_channel.get(chan, [])
        current_words.extend(words)
        words_by_channel[chan] = current_words 

    print('saw words: ', words_by_channel)

    for chan, all_words in words_by_channel.items():
        shitpost = build_shitpost(all_words)

        SLACK_CLIENT.api_call(
                'chat.postMessage',
                channel=chan,
                text=shitpost)

    time.sleep(RTM_READ_DELAY)











