import time
import telepot
from command import Command

bot1 = telepot.Bot('5882426733:AAGHhagkLD_4rmShINuWXmbmZM_5_gr3EOI')
def handle(msg):
    content_type = telepot.glance(msg)[0]
    chat_type = telepot.glance(msg)[1]
    chat_id = telepot.glance(msg)[2]
    com = Command(bot1)
    com.initCommand(chat_id=chat_id, chat_type=chat_type, command_type=content_type)
    com.getCommand(msg)
   
bot1.message_loop(handle)
print('Əmrlər gözlənilir...')

while 1:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print('\n Program sonlandı')
        exit()
    except:
        print('Hata')
