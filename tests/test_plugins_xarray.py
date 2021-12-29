from base64 import decode
from _pytest.mark import param
import pytest
import jsonpickle as jp
import pandas as pd

from dataicer import DirectoryHandler
from dataicer.plugins.xarray import register_handlers


@pytest.mark.parametrize("mode", ["nc"])
def test_dataset(directory_handler, xarray_dataset, mode):
    register_handlers(directory_handler, mode=mode)
    json = jp.encode(xarray_dataset)

    assert xarray_dataset["ds1"].equals(jp.decode(json)["ds1"])


@pytest.mark.parametrize("mode", ["nc"])
def test_dataarray(directory_handler, xarray_dataarray, mode):
    register_handlers(directory_handler, mode=mode)
    json = jp.encode(xarray_dataarray)

    assert xarray_dataarray["da1"].equals(jp.decode(json)["da1"])
