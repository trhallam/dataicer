"""This plugin is modelled on jsonpickles extensions.

Instead of saving pandas DataFrames to json they are saved to either CSV or HDF files.
"""

from typing import Literal, Type
from jsonpickle.handlers import BaseHandler

import xarray as xr

from .file import BaseFileHandler


class XarrayBaseHandler(BaseHandler, BaseFileHandler):
    def __init__(self, mode: Literal["nc"] = "nc", write_kwargs=None):
        BaseFileHandler.__init__(self)

        self._mode = mode
        self._write_kwargs = write_kwargs

    def get_file_id(self):
        return self.get_uuid() + f".{self._mode}"


class XarrayDataArrayHandler(XarrayBaseHandler):
    def flatten(self, obj, data):

        data["file_uuid"] = self.get_file_id()

        meta = {
            "shape": obj.shape,
            "mode": self._mode,
            "dims": obj.dims,
        }

        data.update(meta)

        kwargs = {"engine": "h5netcdf", "mode": "w"}

        if self._write_kwargs:
            kwargs.update(data["write_kwargs"])
        data["write_kwargs"] = kwargs

        if self._mode == "nc":
            with self._ah.open_file(data["file_uuid"], mode="w") as open_file:
                obj.to_netcdf(
                    self._ah.path / data["file_uuid"],
                    **data["write_kwargs"],
                )

        return data

    def restore(self, data):

        mode = data["mode"]

        if mode == "nc":
            da = xr.open_dataarray(self._ah.path / data["file_uuid"])
        return da


class XarrayDatasetHandler(XarrayBaseHandler):
    def flatten(self, obj, data):

        data["file_uuid"] = self.get_file_id()

        meta = {
            "info": str(obj.info()),
            "mode": self._mode,
            "dims": dict(obj.dims),
            "vars": list(obj.keys()),
        }

        data.update(meta)

        kwargs = {"engine": "h5netcdf", "mode": "w"}

        if self._write_kwargs:
            kwargs.update(data["write_kwargs"])
        data["write_kwargs"] = kwargs

        if self._mode == "nc":
            with self._ah.open_file(data["file_uuid"], mode="w") as open_file:
                obj.to_netcdf(
                    self._ah.path / data["file_uuid"],
                    **data["write_kwargs"],
                )

        return data

    def restore(self, data):

        mode = data["mode"]

        if mode == "nc":
            ds = xr.open_dataset(self._ah.path / data["file_uuid"])
        return ds


def get_xarray_handlers(mode: Literal["nc"] = "nc") -> dict:
    """Get a dictionary of xarray, handler pairs."""
    type_handlers = {
        xr.DataArray: XarrayDataArrayHandler(mode=mode),
        xr.Dataset: XarrayDatasetHandler(mode=mode),
    }
    return type_handlers
