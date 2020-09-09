import os, bmemcached

from classes.tg.botApi import Bot

class Public:

    def __init__(self, message):

        try:

            mc_servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
            mc_user = os.environ.get('MEMCACHIER_USERNAME', '')
            mc_passw = os.environ.get('MEMCACHIER_PASSWORD', '')
            token = os.getenv("TOKEN")
            master = int(os.getenv("MASTER"))
            debug = os.getenv("DEBUG")

            mc = bmemcached.Client(mc_servers, username=mc_user, password=mc_passw)
            mc.enable_retry_delay(True)

            groupHutor = -464572634 # group
            groupHutor2 = -1001471520704 # supergroup
            groupHutor3 = -1001393395949 # supergroup

            testerBotoff = 351009636

            # инициализация телеграм бота
            tg = Bot(token)

            message_id = message.getMessageId()
            text = message.getText()

            if (text == "/start"):

                response = tg.sendMessage(master, "Зачем жмёшь старт?")

            else:
                response = tg.sendMessage(master, "Ха!")

        except:

            return HttpResponse("ok")


        return HttpResponse("ok")

