from classes.tg.types.message import Message
from classes.tg.types.user import User
import json


class CallbackQuery:
    'класс типов телеграм объектов'

    #	String	Unique identifier for this query
    id = ""
    # объект класса User	Sender
    user_from = None

    # объект класса Message	Optional. Message with the callback button that originated the query. Note that message content and message date will not be available if the message is too old
    message = None
    #	String	Optional. Identifier of the message sent via the bot in inline mode, that originated the query.
    inline_message_id = ""
    #	String	Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in games.
    chat_instance = ""
    #	String	Optional. Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field.
    data = ""
    #	String	Optional. Short name of a Game to be returned, serves as the unique identifier for the game
    game_short_name = ""


    def __init__(self, obj):
        self.setId(obj['id'])
        self.setFrom(obj['from'])

        if 'message' in obj:
            self.setMessage(obj['message'])
        if 'inline_message_id' in obj:
            self.setInlineMessageId(obj['inline_message_id'])
        if 'chat_instance' in obj:
            self.setChatInstance(obj['chat_instance'])
        if 'data' in obj:
            self.setData(obj['data'])
        if 'game_short_name' in obj:
            self.setGameShortName(obj['game_short_name'])




    def get(self):
        response = {
            'id':self.id,
            'from':self.user_from.get()
        }

        if self.message is not None:
            response.update({'message':self.message.get()})
        if self.inline_message_id != "":
            response.update({'inline_message_id':self.inline_message_id})
        if self.chat_instance != "":
            response.update({'chat_instance':self.chat_instance})
        if self.data != "":
            response.update({'data':self.data})
        if self.game_short_name != "":
            response.update({'game_short_name':self.game_short_name})

        return response


    def getStr(self):
        return str(self.get())


    def getJson(self):
        return json.dumps(self.get())


    # запись id
    def setId(self, val):
        self.id = val

    # получение id
    def getId(self):
        return self.id


    # запись объекта класса User
    def setFrom(self, val):
        self.user_from = User(val)

    # получение объекта класса User
    def getFrom(self):
        return self.user_from


    # запись объекта класса Message
    def setMessage(self, val):
        self.message = Message(val)

    # получение объекта класса Message
    def getMessage(self):
        return self.message


    # запись
    def setInlineMessageId(self, val):
        self.inline_message_id = val

    # получение
    def getInlineMessageId(self):
        return self.inline_message_id


    # запись
    def setChatInstance(self, val):
        self.chat_instance = val

    # получение
    def getChatInstance(self):
        return self.chat_instance


    # запись
    def setData(self, val):
        self.data = val

    # получение
    def getData(self):
        return self.data


    # запись
    def setGameShortName(self, val):
        self.game_short_name = val

    # получение
    def getGameShortName(self):
        return self.game_short_name



