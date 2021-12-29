import pytest

import numpy as np

from dataicer import ice, list_handlers, deice
from dataicer.plugins import numpy as dinp
from dataicer.plugins import pandas as dipd
from dataicer.plugins import xarray as dixr


@pytest.mark.parametrize(
    "baseobj", [int, str, complex, float], ids=["int", "str", "complex", "float"]
)
def test_ice_baseobjects(directory_handler, baseobj):
    test_obj = baseobj(10)
    ice(directory_handler, a=test_obj)


@pytest.mark.parametrize("mode", ["txt", "npy", "npz"])
def test_ice_numpy(directory_handler, numpy_data, mode):
    dinp.register_handlers(directory_handler, mode=mode)
    ice(directory_handler, npar=numpy_data)

    di = deice(directory_handler.path)
    np.testing.assert_array_equal(di["npar"]["np_data"], numpy_data["np_data"])


@pytest.mark.parametrize("mode", ["csv", "h5"])
def test_ice_pandas(directory_handler, pandas_df, mode):
    dipd.register_handlers(directory_handler, mode=mode)
    ice(directory_handler, df=pandas_df)

    di = deice(directory_handler.path)
    assert pandas_df["df1"].equals(di["df"]["df1"])


@pytest.mark.parametrize("mode", ["nc"])
def test_ice_xarray_dataset(directory_handler, xarray_dataset, mode):
    dixr.register_handlers(directory_handler, mode=mode)
    ice(directory_handler, ds=xarray_dataset)

    di = deice(directory_handler.path)
    assert xarray_dataset["ds1"].equals(di["ds"]["ds1"])


@pytest.mark.parametrize("mode", ["nc"])
def test_ice_xarray_dataarray(directory_handler, xarray_dataarray, mode):
    dixr.register_handlers(directory_handler, mode=mode)
    ice(directory_handler, da=xarray_dataarray)

    di = deice(directory_handler.path)
    assert xarray_dataarray["da1"].equals(di["da"]["da1"])


def test_class_of_baseobjects(directory_handler, test_class):

    tc = test_class()
    ice(directory_handler, tc=tc)
    di = deice(directory_handler.path, classes=test_class)

    assert di["tc"] == tc


def test_list_handlers():
    handlers = list_handlers()
    assert isinstance(handlers, dict)
    assert "base" in handlers
    assert isinstance(handlers["base"], dict)
    assert "extra" in handlers
    assert isinstance(handlers["extra"], dict)


# @pytest.mark.parametrize(
#     "comp", ["gz", "bz2", "xz"]
# )
# def test_ice_tar(tmpdir, comp):
#     filename = pathlib.Path(tmpdir / "fakepath")
#     ice(tmpdir/"fakepath", compression=comp, a=2)

#     assert filename.with_suffix(".tar.{}".format(comp)).exists()

# @pytest.mark.parametrize(
#     "comp", ["zip"]
# )
# def test_ice_zip(tmpdir, comp):
#     filename = pathlib.Path(tmpdir / "fakepath")
#     ice(tmpdir/"fakepath", compression=comp, a=2)

#     assert filename.with_suffix(".{}".format(comp)).exists()
