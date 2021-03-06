#!/usr/bin/python3

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

import os, smtplib, requests, json, bmemcached

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from classes.tg.botApi import Bot


mc_servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
mc_user = os.environ.get('MEMCACHIER_USERNAME', '')
mc_passw = os.environ.get('MEMCACHIER_PASSWORD', '')

mc = bmemcached.Client(mc_servers, username=mc_user, password=mc_passw)
mc.enable_retry_delay(True)


def send(request):

    if request.method != "POST" or "email" not in request.POST or "message" not in request.POST:
        return HttpResponseRedirect("/")

    global tg, master, admin_group, smtp_login, smtp_pass, smtp_port, smtp_server

    token = os.getenv("TOKEN")
    master = int(os.getenv("MASTER"))
    admin_group = int(os.getenv("ADMIN_GROUP"))
    smtp_login = str(os.getenv("SMTP_LOGIN"))
    smtp_pass = str(os.getenv("SMTP_PASSWORD"))
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_server = str(os.getenv("SMTP_SERVER"))

    tg = Bot(token)

    response = ""

    if request.POST["email"] != "":
        # if request.POST["message"] != "":

            if request.get_host() != '127.0.0.1:8000':
                if mc.get("repeat") is None:
                    mc.set("repeat", "yes", 30)

                    if "product" in request.POST:
                        product = "Куплю: " + request.POST["product"]
                        if "color" in request.POST:
                            product += " " + request.POST["color"]
                            if "promo" in request.POST:
                                product += "\n\nПромо-код: " + request.POST["promo"]
                        
                        response += mailing(request.POST["email"], request.POST["message"], product)
                    else:
                        msg = request.POST["message"]
                        index = msg.find("http") # функция возвращает -1 если совпадения не найдены
                        if index == -1:
                            response += mailing(request.POST["email"], request.POST["message"])
                        else:
                            response = "Письмо отправленно в СПАМ!"

                else:                    
                    response += "Письмо уже отправленно!"
            else:
                # сохранение сессии
                # для localhost SESSION_ENGINE необходимо закоментировать в settings.py
                if "repeat" not in request.session:
                    # удаление через 30 секунд
                    request.session.set_expiry(30)
                    request.session["repeat"] = "yes"

                    if "product" in request.POST:
                        product = "Куплю: " + request.POST["product"]
                        if "color" in request.POST:
                            product += " " + request.POST["color"]
                            if "promo" in request.POST:
                                product += "\n\nПромо-код: " + request.POST["promo"]
                        response += mailing(request.POST["email"], request.POST["message"], product)
                    else:
                        msg = request.POST["message"]
                        index = msg.find("http") # функция возвращает -1 если совпадения не найдены
                        if index == -1:
                            response += mailing(request.POST["email"], request.POST["message"])
                        else:
                            response = "Письмо отправленно в СПАМ!"

                else:                    
                    response += "Письмо уже отправленно!"
        # else:
        #     response += "Необходимо описать суть вопроса или предложения!"
    else:
        response += "Необходимо указать Ваш email!"

    return render(request, "support/sendmail.html", {'response':response})


''' отправка письма '''
def sendMailTo(to_whom, body):

    try:
        message = MIMEMultipart()
        message['Subject'] = "Клиент " + to_whom +" c сайта hutoryanin.ru"
        message['From'] = smtp_login
        #message['To'] = 'someone@else.com'
        message.attach(MIMEText(body, 'plain'))
        #message.attach(MIMEText('<h1 style="color: blue">A Heading</a><p>Something else in the body</p>', 'html'))
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        #server.starttls()
        server.login(smtp_login, smtp_pass)

        #server.sendmail(smtp_login, to_whom, message.as_string())
        server.sendmail(smtp_login, smtp_login, message.as_string())

        server.quit()

        return "Письмо отправленно! Ожидайте ответного сообщения."
    except:
        return "Ошибка! Не смог отправить письмо!"
        #return "Письмо отправленно."


''' рассылка письма, в телеграм и на почту '''
def mailing(email, message, product = ""):

    if product != "":
        body = email + "\n\n" + product +  "\n\n" + message
    else:
        body = email + "\n\n" + message

    try:
        tg.sendMessage(admin_group, body)

        return sendMailTo(email, body)#return "Письмо отправленно!"#

    except:
        return "Ошибка! Не смог отправить сообщение!"





