from abc import abstractmethod

from DBModels.TgBotStorage import TgBotStorage
from Handlers.GeneralStorageManager import GeneralStorageManager
from Utilities.typings import TgBotId


class TgBotHandler(GeneralStorageManager):
    def __init__(self, bot_id: TgBotId):
        super().__init__()
        self.bot_settings: TgBotStorage = self._connection.root().bots[bot_id]

    def __call__(self, *args, **kwargs):
        self.start_bot()

    @abstractmethod
    def start_bot(self):
        raise NotImplementedError()

    @abstractmethod
    def send_message_to_user(self):
        raise NotImplementedError()
