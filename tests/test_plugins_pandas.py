import pytest
import jsonpickle as jp

from dataicer import DirectoryHandler
from dataicer.plugins.pandas import get_pandas_handlers


@pytest.mark.parametrize("array_mode", ["txt", "npy", "npz", "json"])
@pytest.mark.parametrize("mode", ["csv", "h5"])
def test_dataframe(tmpdir, pandas_df, mode, array_mode):
    dh = DirectoryHandler(
        tmpdir, get_pandas_handlers(mode=mode, array_mode=array_mode), "w"
    )
    with dh as _:
        json = jp.encode(pandas_df)
        test = jp.decode(json)
    assert pandas_df["df1"].equals(test["df1"])
