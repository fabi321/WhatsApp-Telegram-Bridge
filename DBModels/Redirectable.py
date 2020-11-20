from __future__ import annotations

from typing import Optional

from persistent import Persistent

from Utilities.typings import WaMessageId, TgMessageId


class Redirectable(Persistent):
    def __init__(self, redirects: Redirectable = None):
        super().__init__()
        self.redirect: Optional[Redirectable] = redirects

    def get_pipe(self, msg_id: [WaMessageId, TgMessageId]) -> str:
        return f'{self.get_pipe_name()}\x1f{msg_id}\x1f{self.get_pipe_id()}'

    def get_pipe_id(self) -> str:
        raise NotImplemented('Redirectable needs get_pipe_id')

    def get_pipe_name(self) -> str:
        raise NotImplemented('Redirectable needs get_pipe_name')
