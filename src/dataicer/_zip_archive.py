from typing import Literal
import shutil
import os
import pathlib
import tempfile
import zipfile
import time

from ._errors import DataIceExists
from ._base_archive import BaseArchiveHandler
from ._utils import PathType
from ._dir_archive import DirectoryHandler


class ZipHandler(DirectoryHandler):
    """A handler for saving/loading files to/from a zip file.
    Writes are only atomic on close with the context manager.

    This is mostly a thin wrapper around a DirectoryHandler that zips/unzips to
    a temporary directory.

    Best performance will be achieved with a single context session.
    """

    _archive_type = "zip"
    i = 1

    def __init__(
        self,
        zip_path: PathType,
        handlers: dict = None,
        mode: Literal["r", "w", "a"] = "r",
        working_path=None,
    ):
        """

        Args:
            zip_path: The path of the zip file, (always has a .ice.zip suffix)
            handlers: type and handler pairs, handlers are `jsonpickle` extensions.
            mode: how to open the file.
        """
        self._zip_mode = mode
        self.zip_path = pathlib.Path(zip_path).with_suffix(".ice.zip")
        self._working_path = working_path
        self._handlers = handlers
        self._open = False

        if mode in ["r", "a"] and not self.zip_path.exists():
            raise FileNotFoundError

        if mode == "w" and self.zip_path.exists():
            os.remove(self.zip_path)

        self._tempdir = tempfile.TemporaryDirectory(
            prefix="dataicer_", suffix=".ice", dir=self._working_path
        )
        self.working_dir = pathlib.Path(self._tempdir.name)
        super().__init__(
            self.working_dir, self._handlers, mode="w" if mode in ["w", "a"] else "r"
        )

    def open(self):
        super().open()
        if self._zip_mode in ["r", "a"]:
            zip_file = zipfile.ZipFile(self.zip_path, "r")
            zip_file.extractall(self.working_dir)
        self._open = True

    def close(self):
        super().close()
        zip_file = zipfile.ZipFile(self.zip_path, "w")

        for file in self.path.iterdir():
            zip_file.write(file.absolute(), arcname=file.name)
        zip_file.close()
        self._open = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        pass
