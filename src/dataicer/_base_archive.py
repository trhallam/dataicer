from typing import Dict, Union, Sequence
from pathlib import Path
import jsonpickle as jp
from ._utils import PathType
from ._core import _get_json_meta


class BaseArchiveHandler:
    """Base class for dealing with dataice handlers"""

    _archive_type = "base"

    def __init__(
        self,
        dir_path: PathType,
        handlers: dict = None,
    ):
        """"""
        self.path = Path(dir_path)
        self._handlers = handlers if handlers is not None else dict()

    def save_json(self, **kwargs):
        """Save objects to file with names from keyword arguments."""
        raise NotImplementedError

    def load_json(self, args):
        """Load objects from a file with names from keyword arguments."""
        raise NotImplementedError

    def keys(self) -> Sequence[str]:
        """Get all the objects keys that have been iced in the archive"""
        raise NotImplementedError

    def _read_key(self, key) -> str:
        """returns a JSON string from reading a key in an archive"""
        raise NotImplementedError

    def ice(self, meta: Union[dict, None] = None, **kwargs):
        meta = dict() if not meta else meta
        meta.update({"handlers": self._handlers})
        self.save_json(**{"meta": _get_json_meta(meta)})

        with self as _:
            for arg, val in kwargs.items():
                freeze = jp.encode(val)
                self.save_json(**{arg: freeze})

    def deice(self, *args, classes=None, **kwargs) -> dict:
        """deice your archive

        Args:
            args: the keys to load, if None, all will be loaded
            classes: Classes to deice that are not importable from the module store. Passed to jsonpickle.decode

        Returns:
            dict: A decoded dictionary of all the variables in archive.
        """
        if not args:
            args = tuple(key for key in self.keys() if key != "meta")

        restored = dict()
        with self as _:
            for name in args:
                var = self._read_key(name)
                restored[name] = jp.decode(var, keys=True, classes=classes)

        return restored

    def get_object_list(self):
        """Get the list of objects from the archive."""
        raise NotImplementedError

    def __enter__(self):
        for cls, handler in self._handlers.items():
            try:
                handler.set_archive_handler(self)
            except AttributeError:
                pass
            jp.register(cls, handler, base=True)
        return self

    def __exit__(self, *args):
        for cls, _ in self._handlers.items():
            jp.unregister(cls)
        return args
