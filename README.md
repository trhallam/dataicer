# dataicer - [![latest-version](https://img.shields.io/pypi/v/dataicer?color=006dad&label=pypi_version&logo=Python&logoColor=white)](https://pypi.org/project/dataicer)

<p align="left">
    <a href="https://github.com/trhallam/digirock/actions"
       alt="Python Tests">
        <img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/trhallam/0da415ee1bf30b0fc37a2fc4ddafbdee/raw/dataicer_test.json" />
    </a>
    <a href="https://github.com/trhallam/digirock/actions"
       alt="Python Test Coverage">
        <img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/trhallam/0da415ee1bf30b0fc37a2fc4ddafbdee/raw/dataicer_coverage.json" />
    </a>
    <a href="https://github.com/psf/black"
       alt="black">
        <img src="https://img.shields.io/badge/code_style-black-000000.svg" />
    </a>
    </a>
        <a href="https://github.com/trhallam/digirock/blob/main/LICENSE"
       alt="License">
        <img src="https://img.shields.io/badge/license-MIT-brightgreen" />
    </a>
</p>

Ice (save) your data and high level objects for use later.

Do you have complex classes or objects that you want to save to disk and reinstate
later? Do you want to use a data structure's natural save methods? Do you want it
to be easy and manageable, capturing key information so you can come back and load
your data again later if you need to?

`dataicer` can help you with all this. Built on top of `jsonpickle`, `dataicer`
allows you to create a central handler (just for a directory at the moment) where
Python objects can be saved in `json` format. However, while `json` format might
be ok for small objects or simple types it is not great for `numpy.ndarray` or
`pandas.DataFrame` or `xarray.Dataset` complex structures. Complex structures also
come with their own way of saving information and `dataicer` leverages this on top
of `jsonpickle` to create portable and recreatable saved Python state.

## Installation

Installation using `pip` via the source directory.

```
pip install .
```

or install from PyPi

```
pip install digirock
```

## Usage

First, create a new `DirectoryHandler` class. This points at the archive folder
you want to use.

If you have special classes you need to pickle they need a special handler. Dataicer includes handlers for `numpy.ndarray`, `xarray.Dataarray` and `xarray.Dataset` and `pandas.DataFrame`. Handlers are unique to the `DirectoryHandler` instance.

```
from dataicer import DirectoryHandler
from dataicer.plugins import get_numpy_handlers, get_pandas_handlers, get_xarray_handlers

handlers = get_pandas_handlers()
handlers.update(get_xarray_handlers())

dh = DirectoryHandler("my_archive", handlers, mode="w")
```

Numpy arrays can be saved in single column `"txt"`, `"npy"` binary, or `"npz"` compressed.
Xarray structures can only be saved as `"nc"` netcdf.
Pandas DataFrames can be saved as `"h5"` hdf5 or `"csv"` text files.

Objects are then passed to the `ice` function of the `DirectoryHandler` as keyword arguments.

```
import numpy as np
import xarry as xr
import pandas as pd

dh.ice(
    nparr=np.zeros(10),
    df=pd.DataFrame(data={"a":[1, 2, 3]}),
    xarrds=xr.tutorial.scatter_example_dataset()
)
```

Alternatively, the `DirectoryHandler` can be used within a context manager.

```
with DirectoryHandler("my_archive", handlers, mode="w") as dh:
    dh.ice(
        nparr=np.zeros(10),
        df=pd.DataFrame(data={"a":[1, 2, 3]}),
        xarrds=xr.tutorial.scatter_example_dataset()
    )
```

`dataicer` will create the directory `my_archive` and place three files identified via a uuid
in the directory for each object. There is also a JSON file with the key name containing all
the meta information for the object saved and a `meta.json` file which contains information
about the system state at the time the archive was created.

The `deice` command can be used to reload all of the arguments into a dictionary.

```
state = dh.deice()
state["nparr"]

    array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
```

If you desire to save other data structures to file, perhaps pickling a machine learning model or something custom, then a new handler plugin should be written following the style of the plugins in the `dataice.plugins` module.

Consider contributing your plugin to the pool of plugins currently available.