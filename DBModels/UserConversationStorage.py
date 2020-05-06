from DBModels.WaGroupStorage import WaGroupStorage
from DBModels.WaUserStorage import WaUserStorage
from DBModels.TgBotStorage import TgBotStorage
from DBModels.TgUserStorage import TgUserStorage
from DBModels.MessageStorage import MessageStorage
from DBModels.ConversationStorage import ConversationStorage
from typing import List


class UserConversationStorage(ConversationStorage):
    def __init__(self, wa_group: WaGroupStorage, wa_user: WaUserStorage, tg_user: TgUserStorage, tg_bot: TgBotStorage,
                 messages: List[MessageStorage] = None):
        super().__init__(messages=messages)
        self.wa_group: WaGroupStorage = wa_group
        self.wa_user: WaUserStorage = wa_user
        self.tg_user: TgUserStorage = tg_user
        self.tg_bot: TgBotStorage = tg_bot

    def __str__(self) -> str:
        return str(self.tg_user) + '-' + str(self.wa_user)
