from persistent import Persistent
from persistent.list import PersistentList
from DBModels.MessageStorage import MessageStorage
from typing import List
from Utilities.typings import TgMessageId, WaMessageId


class ConversationStorage(Persistent):
    def __init__(self, messages: List[MessageStorage] = None):
        if messages:
            assert all([isinstance(i, MessageStorage) for i in messages])
        super().__init__()
        self.messages: PersistentList[MessageStorage] = PersistentList(messages)

    def add_message(self, message: MessageStorage):
        assert isinstance(message, MessageStorage)
        if message not in self.messages:
            self.messages.append(message)

    def remove_message(self, message: MessageStorage):
        if message not in self.messages:
            raise NotImplementedError('Tried to remove message ' + str(message) + ' from group ' + str(self.tg_id) +
                                      ' without being in the List.')
        self.messages.pop(self.messages.index(message))

    def remove_message_by_id(self, message_id: [TgMessageId, WaMessageId]):
        if isinstance(message_id, TgMessageId):
            if not any([i.tg_id == message_id for i in self.messages]):
                raise KeyError('Tried to remove TgMessageId ' + str(message_id) +
                               ' from UserConversation, but it was not in the list')
            for i in self.messages:
                if i.tg_id == message_id:
                    self.messages.pop(self.messages.index(i))
            return
        assert isinstance(message_id, WaMessageId)
        if not any([i.wa_id == message_id for i in self.messages]):
            raise KeyError('Tried to remove WaMessageId ' + str(message_id) +
                           ' from UserConversation, but it was not in the list')
        for i in self.messages:
            if i.wa_id == message_id:
                self.messages.pop(self.messages.index(i))
