from os import environ
from sys import exit
from random import randint
import time
import re
from slackclient import SlackClient
import giphy_client
from giphy_client.rest import ApiException

def extract_words(e):
    """
    Extracts the channel from which a message was received and the words in that message.

    :param e: a Slack RTM event
    :rtype: (string, list(string))
    :return: the interesting bits of a message
    """
    return e['channel'], e['text'].split()

def is_chatter_and_not_us(e):
    """
    Determines if an event is a message that was not sent by us
    (so we don't react to our own messages).

    :param e: a Slack RTM event
    :rtype: boolean
    :return: whether we should care about a message
    """
    return (e is not None
            and 'type' in e 
            and e['type'] == 'message' 
            and 'user' in e 
            and e['user'] != USER_ID
            and 'thread_ts' not in e)

def build_shitpost(words):
    """
    Builds a GIF link response to a string of words.
    Drops a random word from the list before trying again if there were no results.

    :param e: a Slack RTM event
    :rtype: string
    :return: the shitpost
    """
    while len(words) is not 0:
        print('searching: [', '%20'.join(words), ']')
        results = GIPHY_CLIENT.gifs_search_get(
                environ.get('GIPHY_API_KEY'),
                '%20'.join(words))
        
        if len(results.data) == 0:
             words.pop(randint(0, len(words)-1))
             continue

        return '{} | {}'.format(
                ' '.join(words),
                results.data[0].images.original.url)

    return 'I got nothin'

# CONSTANTS
RTM_READ_DELAY = 1
GIPHY_CLIENT = giphy_client.DefaultApi()
SLACK_CLIENT = SlackClient(environ.get('SLACK_BOT_ACCESS_TOKEN'))
URL_EMOJI_POO = 'https://emojipedia-us.s3.amazonaws.com/thumbs/120/mozilla/36/pile-of-poo_1f4a9.png'

if __name__ == '__main__':

    if not SLACK_CLIENT.rtm_connect(with_team_state=False):
        print('failed to connect')
        exit(1)

    print('connected')
    USER_ID = SLACK_CLIENT.api_call("auth.test")["user_id"]

    while True:
        words_by_channel = dict()
        for e in SLACK_CLIENT.rtm_read():
            if not is_chatter_and_not_us(e):
                continue

            chan, words = extract_words(e)
            if len(words) is 0:
                continue

            current_words = words_by_channel.get(chan, [])
            current_words.extend(words)
            words_by_channel[chan] = current_words

        for chan, all_words in words_by_channel.items():
            shitpost = build_shitpost(all_words)

            SLACK_CLIENT.api_call(
                    'chat.postMessage',
                    channel=chan,
                    text=shitpost,
                    as_user=False,
                    icon_url=URL_EMOJI_POO)

        time.sleep(RTM_READ_DELAY)

