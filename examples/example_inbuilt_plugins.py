from typing import Dict
from dataicer import DirectoryHandler
from dataicer.plugins import (
    get_numpy_handlers,
    get_pandas_handlers,
    get_xarray_handlers,
)

import numpy as np
import pandas as pd

# import pandas as pd

import xarray as xr
import jsonpickle as jp

a = dict(
    b=1,
    c=2,
    d=dict(e=3, f=4),
    e=np.array([1, 2, 3, 4]),
    f=pd.DataFrame(data=dict(a=[1, 2, 3, 4])),
    g=xr.DataArray(np.zeros((4, 4))),
)

handlers = get_pandas_handlers(array_mode="npz", mode="h5")
handlers.update(get_xarray_handlers())

dh = DirectoryHandler("test", handlers, "w")

dh.ice(a=a, b=a)


dh2 = DirectoryHandler("test", handlers, "r")

data = dh.deice()

print(data)
