from __future__ import annotations

from typing import Dict

from persistent import Persistent

from Utilities.typings import WaMessageId, TgMessageId


class Redirectable(Persistent):
    def __init__(self):
        super().__init__()
        self.redirect: Dict[Redirectable] = {}

    def get_pipe(self, msg_id: [WaMessageId, TgMessageId]) -> str:
        return f'Message\x1f{msg_id}'
