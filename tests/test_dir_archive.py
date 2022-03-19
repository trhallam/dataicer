from typing import Dict
import pytest
import pathlib

import numpy as np

from dataicer._dir_archive import FileHandler, DirectoryHandler
from dataicer.plugins import (
    get_numpy_handlers,
    get_pandas_handlers,
    get_xarray_handlers,
)


@pytest.fixture(scope="function")
def directory_handler(tmpdir):
    tmpdir.remove()
    handler = DirectoryHandler(tmpdir, mode="w")
    return handler


@pytest.mark.parametrize("mode", ("w", "a"))
def test_FileHandler_writeable(tmpdir, mode):
    fname = "FileHandlerTest.txt"
    with FileHandler(tmpdir, fname, mode=mode) as fh:
        fh.write("test text")

    with open(tmpdir / fname, "r") as fr:
        assert fr.readlines() == ["test text"]


def test_FileHandler_readable(tmpdir):
    fname = "FileHandlerTest.txt"
    fpath = pathlib.Path(tmpdir) / fname
    with open(fpath, "w") as fw:
        fw.write("test text")
    with FileHandler(tmpdir, fname, mode="r") as fh:
        assert fh.readlines() == ["test text"]


def test_DirectoryHandler_has_archive_type(directory_handler):
    assert directory_handler._archive_type == "directory"


@pytest.fixture(scope="function")
def mock_directory_handler(tmpdir):
    dirname = "mock_directory_handler"
    mockdir = pathlib.Path(tmpdir) / dirname
    mockdir.mkdir(exist_ok=True)

    for test_file in ["A", "B", "C"]:
        (mockdir / f"{test_file}.json").touch()

    return mockdir


@pytest.mark.parametrize("mode", ("w", "a"))
def test_DirectoryHandler_init_fresh_writeable(tmpdir, mode):
    tmpdir_unique = pathlib.Path(tmpdir) / f"mock_directory_handler_mode_{mode}"
    dh = DirectoryHandler(tmpdir_unique, mode=mode)


@pytest.mark.parametrize("mode", ("w", "a"))
def test_DirectoryHandler_init_exists_writeable(mock_directory_handler, mode):
    dh = DirectoryHandler(mock_directory_handler, mode)


@pytest.mark.parametrize("mode", ("r"))
def test_DirectoryHandler_init_fresh_readable(mock_directory_handler, mode):
    dh = DirectoryHandler(mock_directory_handler, mode)


@pytest.mark.parametrize("mode", ("r"))
def test_DirectoryHandler_init_fresh__not_readable(tmpdir, mode):
    with pytest.raises(FileNotFoundError):
        dh = DirectoryHandler(tmpdir / "this_dir_does_not_exist", mode)


def test_DirectoryHandler_open_exists(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    with dh.open_file("A.json") as f:
        x = f.read()
    assert x == ""


def test_DirectoryHandler_open_new(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    with dh.open_file("D.json", "w") as f:
        f.write("test text")
    with dh.open_file("D.json", "r") as f:
        assert f.read() == "test text"


def test_DirectoryHandler_save_obj(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)

    dh.save_json(tc="test text")
    assert (mock_directory_handler / "tc.json").exists()

    with dh.open_file("tc.json", "r") as f:
        assert f.read() == "test text"


def test_DirectoryHandler_keys(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    for v in ["A", "B", "C"]:
        assert v in dh.keys()


def test_DirectoryHandler_getitem(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    for v in ["A", "B", "C"]:
        assert "" == dh[v]


def test_DirectoryHandler_iter_json(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    for key, contents in dh.iter_json():
        assert key in ["A", "B", "C"]
        assert contents == ""

    # with dh.open_file("tc.json")


@pytest.mark.parametrize(
    "baseobj", [int, str, complex, float], ids=["int", "str", "complex", "float"]
)
def test_DirectoryHandler_ice_deice_baseobjects(tmpdir, baseobj):
    test_obj = baseobj(10)
    dh = DirectoryHandler(tmpdir, mode="w")
    dh.ice(a=test_obj)

    test = dh.deice()["a"]
    assert test == test_obj


@pytest.mark.parametrize("mode", ["txt", "npy", "npz"])
def test_DirectoryHandler_ice_deice_numpy(tmpdir, numpy_data, mode):
    dh = DirectoryHandler(tmpdir, get_numpy_handlers(array_mode=mode), mode="w")
    dh.ice(npar=numpy_data)

    test = dh.deice()
    np.testing.assert_array_equal(test["npar"]["np_data"], numpy_data["np_data"])


@pytest.mark.parametrize("mode", ["csv", "h5"])
def test_DirectoryHandler_ice_pandas(tmpdir, pandas_df, mode):
    dh = DirectoryHandler(tmpdir, get_pandas_handlers(mode=mode), "w")
    dh.ice(df=pandas_df)

    test = dh.deice()
    assert pandas_df["df1"].equals(test["df"]["df1"])


@pytest.mark.parametrize("mode", ["nc"])
def test_DirectoryHandler_ice_xarray_dataset(tmpdir, xarray_dataset, mode):
    dh = DirectoryHandler(tmpdir, get_xarray_handlers(mode=mode), "w")
    dh.ice(ds=xarray_dataset)

    test = dh.deice()
    assert xarray_dataset["ds1"].equals(test["ds"]["ds1"])


@pytest.mark.parametrize("mode", ["nc"])
def test_DirectoryHandler_ice_xarray_dataarray(tmpdir, xarray_dataarray, mode):
    dh = DirectoryHandler(tmpdir, get_xarray_handlers(mode=mode), "w")
    dh.ice(da=xarray_dataarray)

    test = dh.deice()
    assert xarray_dataarray["da1"].equals(test["da"]["da1"])


def test_DirectoryHandler_class_of_baseobjects(directory_handler, test_class):

    tc = test_class()
    directory_handler.ice(tc=tc)
    di = directory_handler.deice(classes=test_class)
    assert di["tc"] == tc
