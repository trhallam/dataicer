import pytest
import numpy as np
import pandas as pd
import xarray as xr

from dataicer import DirectoryHandler


@pytest.fixture(scope="module", params=[1, 2, 3], ids=["1d", "2d", "3d"])
def numpy_data(request):
    return {"np_data": np.zeros((5,) * request.param)}


@pytest.fixture(scope="module")
def pandas_df():
    size = 10
    return {
        "df1": pd.DataFrame(
            data=dict(
                float_range=np.arange(size),
                int_range=np.arange(size, dtype=int),
                time_range=pd.date_range(1, 10, size),
                str_list=["abcd"] * 10,
            )
        )
    }


@pytest.fixture(scope="module")
def xarray_dataarray():
    data = np.random.rand(4, 3)
    locs = ["IA", "IL", "IN"]
    times = pd.date_range("2000-01-01", periods=4)
    foo = xr.DataArray(data, coords=[times, locs], dims=["time", "space"])
    return {"da1": foo}


@pytest.fixture(scope="module")
def xarray_dataset():
    temp = 15 + 8 * np.random.randn(2, 2, 3)
    precip = 10 * np.random.rand(2, 2, 3)
    lon = [[-99.83, -99.32], [-99.79, -99.23]]
    lat = [[42.25, 42.21], [42.63, 42.59]]
    ds = xr.Dataset(
        {
            "temperature": (["x", "y", "time"], temp),
            "precipitation": (["x", "y", "time"], precip),
        },
        coords={
            "lon": (["x", "y"], lon),
            "lat": (["x", "y"], lat),
            "time": pd.date_range("2014-09-06", periods=3),
            "reference_time": pd.Timestamp("2014-09-05"),
        },
    )
    return {"ds1": ds}


@pytest.fixture(scope="function")
def directory_handler(tmpdir):
    tmpdir.remove()
    handler = DirectoryHandler(tmpdir, mode="w")
    return handler


@pytest.fixture()
def test_class():
    class TestClass:
        def __init__(
            self,
        ):
            self.a = 1
            self.b = 2.0
            self.c = 1 + 4j
            self.d = (1, 2, 3)
            self.e = [1, 2, 3]
            self.f = {"a": 1, "b": 2}

        def __eq__(self, other):

            for key, val in self.__dict__.items():
                other_val = getattr(other, key)
                if other_val is None:
                    return False

                if other_val != val:
                    return False

            return True

    return TestClass
