from abc import abstractmethod
from typing import List

from DBModels.MessageStorage import MessageStorage
from DBModels.TgBotStorage import TgBotStorage
from DBModels.TgGroupStorage import TgGroupStorage
from DBModels.TgUserStorage import TgUserStorage
from Handlers.GeneralStorageManager import GeneralStorageManager
from Utilities.Pipes import Pipes
from Utilities.typings import TgBotId


class TgBotHandler(GeneralStorageManager):
    def __init__(self, bot_id: TgBotId):
        super().__init__()
        self.bot_settings: TgBotStorage = self._connection.root.bots[bot_id]
        self.pipe = Pipes(str(self.bot_settings.id))

    def __call__(self, *args, **kwargs):
        self.start_bot()

    def handle_pipe_output(self, pipe_string: str):
        splitted: List[str] = pipe_string.split(':')
        if splitted[0] == 'MessageUser':
            message: MessageStorage = self._root.messages[splitted[1]]
            user: TgUserStorage = self._root.users[splitted[2]]
            self.send_message_to_user(message=message, user=user)
            self._commit()
        elif splitted[0] == 'MessageGroup':
            message: MessageStorage = self._root.messages[splitted[1]]
            group: TgGroupStorage = self._root.groups[splitted[2]]
            self.send_message_to_group(message=message, group=group)
            self._commit()
        elif splitted[0] == 'Quit':
            self.__del__()

    def __del__(self):
        self.stop_bot()

    @abstractmethod
    def start_bot(self):
        raise NotImplementedError()

    @abstractmethod
    def send_message_to_user(self, message: MessageStorage, user: TgUserStorage):
        raise NotImplementedError()

    @abstractmethod
    def send_message_to_group(self, message: MessageStorage, group: TgGroupStorage):
        raise NotImplementedError()

    @abstractmethod
    def stop_bot(self):
        raise NotImplementedError()
