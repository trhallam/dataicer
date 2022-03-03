from typing import Type
from typing import Type
import uuid

from .._base_archive import BaseArchiveHandler


class BaseFileHandler:
    def __init__(self):
        self._ah = None

    def set_archive_handler(self, archive_handler: Type[BaseArchiveHandler]):
        self._ah = archive_handler

    def get_uuid(self) -> str:
        # jsonpickle doesn't supply any info about the parents to the
        # handlers so we need to just use a random uuid
        return str(uuid.uuid1())
