import pytest
import jsonpickle as jp

from dataicer import DirectoryHandler
from dataicer.plugins.xarray import get_xarray_handlers


@pytest.mark.parametrize("mode", ["nc"])
def test_dataset(tmpdir, xarray_dataset, mode):
    dh = DirectoryHandler(tmpdir, get_xarray_handlers(mode=mode), "w")
    with dh as _:
        json = jp.encode(xarray_dataset)
        test = jp.decode(json)
    assert xarray_dataset["ds1"].equals(test["ds1"])


@pytest.mark.parametrize("mode", ["nc"])
def test_dataarray(tmpdir, xarray_dataarray, mode):
    dh = DirectoryHandler(tmpdir, get_xarray_handlers(mode=mode), "w")
    with dh as _:
        json = jp.encode(xarray_dataarray)
        test = jp.decode(json)

    assert xarray_dataarray["da1"].equals(test["da1"])
