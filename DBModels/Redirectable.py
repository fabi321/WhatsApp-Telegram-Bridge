from __future__ import annotations

from persistent import Persistent
from persistent.mapping import PersistentMapping

from Utilities.typings import WaMessageId, TgMessageId


class Redirectable(Persistent):
    def __init__(self):
        super().__init__()
        self.redirect: PersistentMapping[Redirectable, Redirectable] = PersistentMapping()

    def get_pipe(self, msg_id: [WaMessageId, TgMessageId]) -> str:
        return f'Message\x1f{msg_id}'
