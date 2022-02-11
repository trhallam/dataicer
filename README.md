# dataicer - [![latest-version](https://img.shields.io/pypi/v/dataicer?color=006dad&label=pypi_version&logo=Python&logoColor=white)](https://pypi.org/project/dataicer)

<p align="left">
    <a href="https://github.com/trhallam/digirock/actions" 
       alt="Python Tests">
        <img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/trhallam/0da415ee1bf30b0fc37a2fc4ddafbdee/raw/dataicer_test.json" />
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
later? Do you want to use a data structures natural save methods? Do you want it
to be easy and manageable, capturing key information so you can come back and load
your data again later if you need to?

`dataicer` can help you with all this. Build on top of `jsonpickle`, `dataicer` 
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

## Usage

First, create a new `DirectoryHandler` class. This points at the archive folder
you want to use.

```
from dataicer import ice, deice, DirectoryHandler, register_handlers

dh = DirectoryHandler("my_archive", mode="w")
```

Then register the archive handler together with any special handlers you need.
Currently, the extra supported data structures are `numpy.ndarray`, `xarray.Dataarray` and `xarray.Dataset` and `pandas.DataFrame`.

Numpy arrays can be saved in single column `"txt"`, `"npy"` binary, or `"npz"` compressed.
Xarray structures can only be saved as `"nc"` netcdf.
Pandas DataFrames can be saved as `"h5"` hdf5 or `"csv"` text files.

```
register_handlers(dh, numpy="txt", xarray="nc", pandas="h5")
```

Objects are then passed to the `ice` function as keyword arguments.

```
import numpy as np
import xarry as xr
import pandas as pd

ice(dh, nparr=np.zeros(10), df=pd.DataFrame(data={"a":[1, 2, 3]}), xarrds=xr.tutorial.scatter_example_dataset())
```

`dataicer` will create the directory `my_archive` and place three files identified via a uuid
in the directory for each object. There is also a JSON file with the key name containing all
the meta information for the object saved and a `meta.json` file which contains information
about the system state at the time the archive was created.

The `deice` command can be passed the path to an archive (it does not require a handler). And
will reload all of the arguments into a dictionary.

```
state = deice("my_archive")
state["nparr"]

    array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
```