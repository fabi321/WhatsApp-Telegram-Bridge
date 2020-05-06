from DBAccess.GeneralStorageManager import GeneralStorageManager
from Utilities.typings import TgBotId
from DBModels.TgBotStorage import TgBotStorage


class BotManager(GeneralStorageManager):
    def __init__(self, bot_id: TgBotId):
        super().__init__()
        bot_settings: TgBotStorage = self._connection.root().bots[bot_id]
