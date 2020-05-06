from __future__ import annotations
from persistent import Persistent
from DBModels.WaUserStorage import WaUserStorage
from DBModels.TgUserStorage import TgUserStorage
from Utilities.typings import TgMessageId, WaMessageId, MessageText
from typing import Optional
from Attachments.GenericAttachment import GenericAttachment


class MessageStorage(Persistent):
    def __init__(self, text: MessageText, sender: [WaUserStorage, TgUserStorage],
                 tg_id: TgMessageId = None, wa_id: WaMessageId = None, attachment: GenericAttachment = None,
                 reply_to: MessageStorage = None):
        super().__init__()
        if not tg_id and not wa_id:
            raise AttributeError('Got MessageStorage without TgMessageId and WaMessageId')
        assert (isinstance(sender, TgUserStorage) and tg_id) or (isinstance(sender, WaUserStorage) and wa_id)
        assert isinstance(text, MessageText)
        self.text: MessageText = text  # if attachment, this is the caption
        assert isinstance(sender, (TgUserStorage, WaUserStorage,))
        self.sender: [TgUserStorage, WaUserStorage] = sender
        if tg_id:
            assert isinstance(tg_id, TgMessageId)
        self.tg_id: Optional[TgMessageId] = tg_id
        if wa_id:
            assert isinstance(wa_id, WaMessageId)
        self.wa_id: Optional[WaMessageId] = wa_id
        if attachment:
            assert isinstance(attachment, GenericAttachment)
        self.attachment: Optional[GenericAttachment] = attachment
        if reply_to:
            assert isinstance(reply_to, MessageStorage)
        self.reply_to: Optional[MessageStorage] = reply_to
        self.download: bool = False if attachment else True
        self.delivered: bool = False

    def get_tg_sender(self) -> TgUserStorage:
        if isinstance(self.sender, TgUserStorage):
            return self.sender
        raise TypeError('Expected TgUserStorage as sender, got ' + str(type(self.sender)))

    def get_wa_sender(self) -> WaUserStorage:
        if isinstance(self.sender, WaUserStorage):
            return self.sender
        raise TypeError('Expected WaUserStorage as sender, got ' + str(type(self.sender)))

    def get_any_sender(self) -> [TgUserStorage, WaUserStorage]:
        return self.sender

    def get_tg_id(self):
        if not self.tg_id:
            raise ValueError('No TgMessageId set')
        return self.tg_id

    def get_wa_id(self):
        if not self.wa_id:
            raise ValueError('No WaMessageId set')
        return self.wa_id

    def downloaded(self, attachment: GenericAttachment):
        self.download = True
        self.attachment = attachment

    def sent(self, other_id: [TgMessageId, WaMessageId]):
        if not self.tg_id and self.wa_id:
            assert isinstance(other_id, TgMessageId)
            self.tg_id = other_id
        elif not self.wa_id and self.tg_id and isinstance(other_id, WaMessageId):
            assert isinstance(other_id, WaMessageId)
            self.wa_id = other_id
        self.delivered = True

    def __str__(self) -> str:
        return str(self.tg_id)
