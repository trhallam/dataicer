from base64 import decode
from _pytest.mark import param
import pytest
import jsonpickle as jp
import numpy as np

from dataicer import DirectoryHandler
from dataicer.plugins.numpy import register_handlers


@pytest.fixture()  # scope="function")
def directory_handler(tmpdir):
    handler = DirectoryHandler(tmpdir, overwrite=True)
    register_handlers(handler)
    return handler


@pytest.fixture(scope="module", params=[1, 2, 3], ids=["1d", "2d", "3d"])
def numpy_data(request):
    return {"np_data": np.zeros((5,) * request.param)}


@pytest.mark.parametrize("mode", ["txt", "npy", "npz"])
def test_ndarray(tmpdir, numpy_data, mode):
    tmpdir.remove()
    handler = DirectoryHandler(tmpdir)
    register_handlers(handler, mode=mode)
    json = jp.encode(numpy_data)
    np.testing.assert_array_equal(numpy_data["np_data"], jp.decode(json)["np_data"])
