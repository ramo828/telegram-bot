import time
import telepot
from command import Command
from time import sleep

bot_init = telepot.Bot('')
com = Command(bot_init)

def handle(msg):
    content_type = telepot.glance(msg)[0]
    chat_type = telepot.glance(msg)[1]
    chat_id = telepot.glance(msg)[2]
    com.initCommand(chat_id=chat_id, chat_type=chat_type, command_type=content_type)
    com.getCommand(msg)
   
bot_init.message_loop(handle)
print('Əmrlər gözlənilir...')

while 1:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print('\n Program sonlandı')
        exit()
    except:
        print('Hata')
