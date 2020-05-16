from typing import List

from DBModels.ConversationStorage import ConversationStorage
from DBModels.MessageStorage import MessageStorage
from DBModels.TgUserStorage import TgUserStorage
from DBModels.WaGroupStorage import WaGroupStorage
from DBModels.WaUserStorage import WaUserStorage


class UserConversationStorage(ConversationStorage):
    def __init__(self, wa_group: WaGroupStorage, wa_user: WaUserStorage, tg_user: TgUserStorage,
                 messages: List[MessageStorage] = None):
        super().__init__(messages=messages)
        assert isinstance(wa_group, WaGroupStorage)
        self.wa_group: WaGroupStorage = wa_group
        assert isinstance(wa_user, WaUserStorage)
        self.wa_user: WaUserStorage = wa_user
        assert isinstance(tg_user, TgUserStorage)
        self.tg_user: TgUserStorage = tg_user

    def __str__(self) -> str:
        return f'{self.tg_user}-{self.wa_user}'
