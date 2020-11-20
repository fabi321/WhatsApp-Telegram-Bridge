from __future__ import annotations

from typing import Optional

from persistent import Persistent

from Utilities.typings import WaMessageId, TgMessageId


class Redirectable(Persistent):
    def __init__(self, redirects: Redirectable = None):
        super().__init__()
        self.redirect: Optional[Redirectable] = redirects

    def get_pipe(self, msg_id: [WaMessageId, TgMessageId]) -> str:
        return f'Message\x1f{msg_id}'
