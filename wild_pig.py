import vk_api, random, time
import ast #.literal_eval()
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from vk_api.upload import VkUpload
import requests
from io import BytesIO

import sqlite3, sys # db lib's
from os.path import abspath
import os
from wild_pig_classes import *


#Блок функций

#send photo
def upload_photo(upload, photo):
    response = upload.photo_messages(photo)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key

def upload_photo_url(upload, url):
    img = requests.get(url).content
    f = BytesIO(img)

    response = upload.photo_messages(f)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key

def send_photo(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment
    )

def update_player(player):
    player_id_str = player.player_id_str
    
    player_obj_str = player.return_prop_str() # объект игрока
    req = "UPDATE users SET info = \"{}\" WHERE id = \"{}\"".format(player_obj_str, player_id_str)
    
    cursor.execute(req)
    db.commit()

def sender(u_id, text, dop_id = None):
    try:
        vk_session.method('messages.send', {'user_id' : u_id, 'message' : text, 'random_id' : get_random_id() })#random.randint(0, 1000)})
    except:
        if dop_id != None:
            vk_session.method('messages.send', {'user_id' : dop_id, 'message' : '💩Прости чел я еще не умею отправлять такое(((', 'random_id' : get_random_id() })
        else:
            vk_session.method('messages.send', {'user_id' : u_id, 'message' : '💩Прости чел я еще не умею отправлять такое(((', 'random_id' : get_random_id() })




#Блок "системных" переменных
#------------------------------
main_token = 'c46cd6350bd66bbe20b9eaf6a56189c434453555b827e23e58fc2feaaef48890fa2df4508515431e4385a'
vk_session = vk_api.VkApi(token = main_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = VkUpload(session_api)
#------------------------------

#Блок глобальных переменных
#------------------------------
users = {}#{'340297072': \
        #            { 'connect': False, 'location': 1, 'pig': \
        #            { 'name': 'Лёнчик', 'level': 1, 'health': 3, 'inventory': [] } }}
free_users = []
IMG_PATH = 'D:\\Code\\vkbot\\img\\pigs\\'
#------------------------------


# db connect
#------------------------------
db = sqlite3.connect(sys.path[0]+'\\server.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id TEXT,
    info TEXT
)""")
db.commit()
#------------------------------

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text#.lower()
            u_id = event.user_id
            u_id_str = str(u_id)
            #photo_url = 'https://sun9-62.userapi.com/impg/0gGN-ROTeakuhk0AMQ8x4k3bFSgq4ZSasicGww/Ut8335M6ByI.jpg?size=1280x854&quality=96&sign=89421a1f36f66be28cf47c510248f298&type=album'
            #url валеры
            
            
            
            # Регистрация нового пользователя/Подключение неактивного
            if not(u_id_str in users): # new user
                cursor.execute( f"SELECT info FROM users WHERE id = {u_id_str}" )
                bd_ans = cursor.fetchone() # ответ базы данных на запрос
                
                if bd_ans is None:
                    
                    default_prop = {'connect': False, 'img': None, 'name': None, 'level': 1, 'points': 0, 'inventory': {}, 'location': ''} # Свойста игрока по умолчанию
                    users[u_id_str] = Player(user_id, default_prop)
                    player = users[u_id_str] # объект игрока
                    
                    #Процесс регистрации:
                    pigs_imgs = os.listdir(IMG_PATH) #список изображений кабанчиков
                    pig_img_fname = random.choice(pigs_imgs)
                    pig_img_path = IMG_PATH + pig_img_fname # полный адресс изображения
                    
                    player.img = pig_img_path
                    
                    sender(u_id, 'Теперь это твой личный кабанчик. Заботься о нем!')
                    send_photo(session_api, u_id, *upload_photo(upload, pig_img_path))
                    player.name = -1 # процесс регистрации имени
                    sender(u_id, 'Придумай своему кабанчику имя:')
                    
                    obj = player.return_prop_str() # объект игрока
                    cursor.execute("INSERT INTO users VALUES (?, ?)", (u_id_str, obj))
                    db.commit()
                    
                    #send_photo(session_api, u_id, *upload_photo_url(upload, photo_url)) # отправка валеры
                else:
                    users[u_id_str] = Player(u_id, ast.literal_eval(bd_ans[0])) # загрузка объекта игрока из бд
                    player = users[u_id_str] # объект игрока
                    
                    sender(u_id, 'С возвращением, ' + player.name)
                    send_photo(session_api, u_id, *upload_photo(upload, player.img))
                    #send_photo(session_api, u_id, *upload_photo_url(upload, photo_url)) # отправка валеры
                continue
            else:
                player = users[u_id_str] # объект игрока
                    
            
            
            if player.is_connect():
                companion_id = player.companion()
                companion = users[companion_id] # Объект собеседника
            
            
            # Блок обработки сообщения
            if msg == '/find': # Поиск собеседника
                
                if player.is_connect(): #(users[str(u_id)]['connect'] != False): # 
                    companion.disconnect()
                    sender(companin.player_id '😭Кабанчик отключился. Напишите /find чтобы найти нового чепушилу')
                    player.disconnect()
                
                sender(player.player_id, '🔎Ищу бойчика...')
                sender(player.player_id, 'Сейчас хотят тебя: ' + str(len(free_users)))
                sender(player.player_id, 'В качалке: ' + str(len(users)))
                
                if not(player.player_id in free_users):
                    free_users.append(player.player_id)
                   
            #Админ команды
            # ----------------------------------------------------
            elif msg == '/show_u':
                sender(player.player_id, str(users))
                sender(player.player_id, 'Ждут: '+str(free_users))
            elif msg == '/close': # отключение бота
                for user in users:
                    sender(int(user), '🦍Валера ушел пить пиво и пернул на прощание')
                    player_obj = users[user]
                    if player_obj.changes: # Если были изменены свойства объекта игрока
                        update_player(player)
                break
            # ----------------------------------------------------
            
            else:
                #общение с другим кабаном
                if player.is_connect(): #(users[str(u_id)]['connect'] != False): # проверка подключения
                    sender(companin.player_id , companion.name + ': ' + msg, player.player_id)
                    
                #Установка имени кабана
                elif player.name == -1
                    player.name = msg
                    update_pig(player)
                    sender(player.player_id, 'Поздвравляю!!! Теперь твоего красавца зовут ' + msg)
                    #send_photo(session_api, u_id, *upload_photo(upload, users[u_id_str]['img']))
                else:
                    sender(u_id, '💞Сладенький, твои сообщения не доходят.\n \
                    😖Если не хочешь повстречаться с моим зеленым змеем напиши /find и найди бойчика себе по силам.\n \
                    🤼‍♂Не понравился бойчик? Смени его командой /find')
                
            
            
            
            #Процесс сведения свободных пользователей
            if len(free_users) > 1:
                #room = []
                user1 = random.choice(free_users)
                free_users.remove(user1)
                
                user2 = random.choice(free_users)
                free_users.remove(user2)
                
                #room.append(user1)
                #room.append(user2)
                
                player1 = users[str(user1)]
                player2 = users[str(user2)]
                
                player1.connect, player2.connect = user2, user1 # connect
                
                sender(user1, 'На узкой лесной тропинке вы повстречали кабанчика по имени ' + player2.name)
                send_photo(session_api, user1, *upload_photo(upload, player2.img))
                
                sender(user2, 'На узкой лесной тропинке вы повстречали кабанчика по имени ' + player1.name)
                send_photo(session_api, user2, *upload_photo(upload, player1.img))

db.close()


