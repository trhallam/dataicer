from ._errors import DataIceExists
from ._base_archive import BaseArchiveHandler
from ._utils import PathType


class FileHandler:
    def __init__(self, parent_dir, file_name, mode="r"):
        self.file_obj = open(parent_dir / file_name, mode=mode)

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        self.file_obj.close()


class DirectoryHandler(BaseArchiveHandler):
    """A handler for saving/loading files to/from a directory."""

    _archive_type = "directory"

    def __init__(self, dir_path: PathType, overwrite: bool = False):
        """

        Args:
            dir_path
        """
        super().__init__(dir_path)

        if not overwrite and self.path.exists():
            raise DataIceExists(
                f"The {self._archive_type} {self.path} already exists, set overwrite option to replace."
            )
        elif overwrite and self.path.exists():
            self.path.rmdir()
        else:
            self.path.mkdir()

    def open_file(self, file_name, mode="r"):
        return FileHandler(self.path, file_name, mode=mode)

    def save(self, **kwargs):
        """Save objects to file with names from keyword arguments."""
        for arg, val in kwargs.items():
            with open(self.path / arg, "w") as open_file:
                open_file.write(val)
