from projects.new_direction import vk_dark_api

vk = vk_dark_api.message_handler().connect_to_methods()
# vk.messages.send(chat_id=14, message='Системы подключены. Вы можете начать работать за здраву душу.', random_id=0)


def Main():
    while True:
        event = vk_dark_api.Main().listen()
        if event is not None:
            if event['type'] == 'message_new':
                text = event['object']['text']
                user_id = event['object']['from_id']
                peer_id = event['object']['peer_id']
                chat_id = peer_id - 2000000000
                if text == 'Где я':
                    vk.messages.send(chat_id=chat_id, message=f'Ты в {chat_id}', random_id=0)
                if text == 'crash':
                    z = vk.messages.getConversations()
                    w = ' '
                    for i in z['response']['items']:
                        w = f'\n\nid{i["last_message"]["peer_id"]}\n{i["last_message"]["text"]}' + w
                    vk.messages.send(chat_id=chat_id, message=w, random_id=0)
                if text == 'get_info':
                    f = vk.groups.getById(group_id=145807954365322543554)
                    f = f"""
                    {'=' * 10}
                    Название группы: {f['response'][0]['name']}
                    {'=' * 10}
                    Ссылка на группу: vk.com/{f['response'][0]['screen_name']}
                    {'=' * 10}
                    """
                    vk.messages.send(chat_id=chat_id, message=f, random_id=0)
                if text == 'a':
                    z = vk.method('messages.getConversationMembers', peer_id=peer_id)
                    for i in z['response']['items']:
                        if i['member_id'] == user_id:
                            print('TRUE')


Main()
