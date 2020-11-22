from __future__ import annotations

from persistent import Persistent
from persistent.mapping import PersistentMapping


class Redirectable(Persistent):
    def __init__(self):
        super().__init__()
        self.redirect: PersistentMapping[Redirectable, Redirectable] = PersistentMapping()
