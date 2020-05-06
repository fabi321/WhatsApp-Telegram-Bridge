from typing import List

from DBModels.ConversationStorage import ConversationStorage
from DBModels.MessageStorage import MessageStorage
from DBModels.TgGroupStorage import TgGroupStorage
from DBModels.WaGroupStorage import WaGroupStorage


class GroupConversationStorage(ConversationStorage):
    def __init__(self, tg: TgGroupStorage, wa: WaGroupStorage, messages: List[MessageStorage] = None):
        super().__init__(messages=messages)
        self.tg: TgGroupStorage = tg
        self.wa: WaGroupStorage = wa

    def __str__(self) -> str:
        return str(self.tg)
