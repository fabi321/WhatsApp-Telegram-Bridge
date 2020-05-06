from Utilities.typings import AccountName, TgBotName, TgBotToken
from Utilities.config import Config
from typing import List, Dict
from pytglib.client import Telegram
from pytglib.functions import Message
from pytglib.utils import AsyncResult
from random import randint
import time


botfather_id: int = 123# TODO: find it out


class TgBot():
    __lock: bool = False
    _config = Config().SETTINGS
    _bot: Telegram = Telegram(
        api_id=_config['tg_id'],
        api_hash=_config['tg_hash'],
        database_encryption_key=_config['db_key'])
    _bot.login()

    def __init__(self):
        self._bots: Dict[int, str] = {}

    def create_bot(self, name: AccountName):
        while self.__lock:
            time.sleep(0.1)
        self.__lock = True

        self._bot.functions.send_message(chat_id=botfather_id, text='/newbot').wait()
        time.sleep(1)
        self._bot.functions.send_message(chat_id=botfather_id, text=name).wait()
        time.sleep(1)
        while True:
            name: TgBotName = TgBotName(str(randint(1000000000000000000, 9999999999999999999)) + 'bot')
            self._bot.functions.send_message(botfather_id, name).wait()
            time.sleep(1)
            message: AsyncResult = self._bot.functions.get_chat_history(chat_id=botfather_id, limit=1)
            message.wait()
            message: Message = message.update.messages[0]
            time.sleep(1)
            if message != 'Sorry, this username is already taken. Please try something different.':
                return
            elif 'Done! Congratulations on your new bot.' in message:
                break
        message: List[str] = message.content.text.text.splitlines()
        token: TgBotToken = TgBotToken('')
        for i in range(len(message)):
            if 'token' in message[i]:
                token = TgBotToken(message[i + 1])
                break
        if token == '':
            self._bot.functions.send_message(
                chat_id=self._config['owner'],
                text="The communication with botfather has changed, please check my account and repair it"
            ).wait()
            raise NotImplementedError(
                "The communication with botfather has been changed, my commands don't work anymore")
        # TODO: Set commands for each bot?
        # TODO: use /setprivacy? so a bot can read messages?

        self.__lock = False

    def create_group(self, name: AccountName):
        self._bot
