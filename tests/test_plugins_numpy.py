import pytest
import jsonpickle as jp
import numpy as np

from dataicer import DirectoryHandler
from dataicer.plugins.numpy import get_numpy_handlers


@pytest.mark.parametrize("mode", ["txt", "npy", "npz", "json"])
def test_ndarray(tmpdir, numpy_data, mode):
    dh = DirectoryHandler(tmpdir, get_numpy_handlers(array_mode=mode), "w")
    with dh as _:
        json = jp.encode(numpy_data)
        test = jp.decode(json)
    np.testing.assert_array_equal(numpy_data["np_data"], test["np_data"])
