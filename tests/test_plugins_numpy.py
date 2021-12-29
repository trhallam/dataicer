from base64 import decode
from _pytest.mark import param
import pytest
import jsonpickle as jp
import numpy as np

from dataicer import DirectoryHandler
from dataicer.plugins.numpy import register_handlers


@pytest.mark.parametrize("mode", ["txt", "npy", "npz"])
def test_ndarray(directory_handler, numpy_data, mode):
    register_handlers(directory_handler, mode=mode)
    json = jp.encode(numpy_data)
    np.testing.assert_array_equal(numpy_data["np_data"], jp.decode(json)["np_data"])
