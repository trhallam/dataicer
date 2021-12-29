from base64 import decode
from _pytest.mark import param
import pytest
import jsonpickle as jp
import pandas as pd

from dataicer import DirectoryHandler
from dataicer.plugins.pandas import register_handlers


@pytest.mark.parametrize("mode", ["csv", "h5"])
def test_dataframe(directory_handler, pandas_df, mode):
    register_handlers(directory_handler, mode=mode)
    json = jp.encode(pandas_df)

    assert pandas_df["df1"].equals(jp.decode(json)["df1"])
