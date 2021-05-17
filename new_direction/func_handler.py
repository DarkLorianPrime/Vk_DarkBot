import re
import time

import requests

from projects.new_direction import logger
import vk_dark_api
import methods

dictionary = {}
vk = vk_dark_api.message_handler().connect_to_methods()


def message_handler(*argss):
    def message_dec(fn):
        dictionary[tuple(argss)] = fn

        def message_wrap(*args):
            return args

        return message_wrap

    return message_dec


@message_handler('remove_people', 'kick', 'ban', 'delete')
@logger.logger('remove')
def remove_chelix(lower):
    params = {'chat_id': 14, 'message': (time.time()) - int(lower), 'random_id': 0, 'access_token': vk_dark_api.token,
              'v': vk_dark_api.v}
    requests.post("https://api.vk.com/method/messages.send", data=params)


@message_handler('delrep')
@logger.logger('New Report')
def _delete_report_call(lower, user_id, chat_id):
    methods.methods().delete_report(lower, user_id, chat_id)


@message_handler('newreport', 'репорт', 'addrep', 'sendrep', 'addreport')
@logger.logger('New Report')
def _report_call(lower, user_id, chat_id):
    methods.methods().report(lower, user_id, chat_id)


@message_handler('allrep', 'все репорты')
@logger.logger('All reports')
def _allreport_call(lower, user_id, chat_id):
    methods.methods().allrep(user_id, chat_id)


def Main():
    while True:
        event = vk_dark_api.Main().listen()
        if event is not None:
            if event['type'] == 'message_new':
                text = event['object']['text']
                user_id = event['object']['from_id']
                peer_id = event['object']['peer_id']
                chat_id = peer_id - 2000000000
                for i in dictionary:
                    for z in i:
                        if re.search(z, text):
                            time.time()
                            dictionary[i](text, user_id, chat_id)


Main()
