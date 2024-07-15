from __future__ import annotations
import dataclasses
import os

import phaistos


@dataclasses.dataclass
class KubrainResourceManager:
    __instance: KubrainResourceManager | None = dataclasses.field(init=False, default=None)
    _validators: phaistos.Manager = dataclasses.field(init=False)

    @classmethod
    def start(cls) -> KubrainResourceManager:
        if cls.__instance is None:
            cls.__instance = cls()
            cls._initialize_validators_manager()
        return cls.__instance

    @classmethod
    def _initialize_validators_manager(cls):
        cls._validators = phaistos.Manager.start(discover=False)
