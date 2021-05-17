import sqlite3

import requests

import ConfigForFactory as CFF
from projects.new_direction import vk_dark_api

conn = sqlite3.connect('Factory.db')
cur = conn.cursor()
vk = vk_dark_api.message_handler().connect_to_methods()


class methods():
    def __init__(self):
        self.message = None
        self.chat_id = None
        self.user_id = None
        self.peer_id = None
        self.v = '5.130'
        self.method_course = 'https://api.vk.com/method'

    def report(self, lower, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id
        pers = lower[8:]
        cur.execute("SELECT Id from Report order by Id desc limit 1")
        res = cur.fetchall()
        if not res:
            Id = 0
        else:
            Id = res[0][0] + 1
        cur.execute('select * from Report where report is ?', (pers[1],))
        ros = cur.fetchone()
        if ros is None:
            if pers is not None and pers != '':
                lost = (Id, self.chatname_and_username(0), pers)
                cur.execute('insert into Report values(?, ?, ?)', lost)
                conn.commit()
                self.sender(
                    message=f'{self.chatname_and_username(0)} отправил репорт:\n{pers} c Id {Id}\n@animanshnik (Тебе там репорт кинули)')
            else:
                self.sender(dis_ment=0, message='Пустое поле.')
        else:
            self.sender(dis_ment=0, message='Запись уже есть.')

    def delete_report(self, lower, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id
        pers = lower.split(': ')
        if len(pers) == 2:
            if pers[1].isnumeric():
                pers[1] = int(pers[1])
                cur.execute('select * from Report where Id is ?', (pers[1],))
                ros = cur.fetchone()
                if ros is not None:
                    cur.execute('DELETE FROM Report WHERE Id is ?', (pers[1],))
                    conn.commit()
                    self.sender(dis_ment=0, message=f'Репорт {pers[1]} удален.', bool_hi=1)
                else:
                    self.sender(dis_ment=0, message='Такого репорта не существует.', bool_hi=1)
            else:
                self.sender(dis_ment=0, message='Такого репорта не существует.', bool_hi=1)
        elif pers[1] == 'all':
            cur.execute('select * from Report')
            ros = cur.fetchall()
            self.sender(dis_ment=0, message='Ожидайте, удаляю.')
            for i in ros:
                cur.execute('DELETE FROM Report WHERE Id is ?', (i[0],))
            self.sender(dis_ment=0, message='Список репортов очищен.', bool_hi=1)
            conn.commit()
        else:
            self.sender(dis_ment=0, message='delrep: [id, all]]', bool_hi=1)

    def allrep(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id
        cur.execute("select * from Report")
        row = cur.fetchall()
        mess = bool(row)
        if mess:
            mess = []
            for i in row:
                mess.append(f'\n[{i[0]}] {i[2]} (от {i[1]})')
            self.sender(dis_ment=0, message='Список репортов:' + ' '.join(mess))
        else:
            self.sender(dis_ment=0, message='Репорты не обнаружены. Я идеален.')

    def chatname_and_username(self, boolean):
        if boolean == 1:
            return vk.messages.getConversationsById(peer_ids=self.peer_id)['items'][0]['chat_settings']['title']
        else:
            return f'{vk.users.get(user_ids=self.user_id)["response"][0]["first_name"]} {vk.users.get(user_ids=self.user_id)["response"][0]["last_name"]}'

    def sender(self, dis_ment=0, message=None, attach=None, bool_hi=0):
        params = {'v': self.v, 'chat_id': self.chat_id, 'access_token': CFF.token, 'message': None,
                  'random_id': 0, 'disable_mentions': dis_ment, 'attachment': attach}
        if bool_hi == 0:
            params['message'] = message
        else:
            params['message'] = f'{message}\nС уважением, Цербер :P.'
        print(f'Отправляю сообщение:\n {message} в {self.chat_id}. {dis_ment}')
        requests.post(f'{self.method_course}/messages.send', params=params)
