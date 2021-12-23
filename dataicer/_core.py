"""
"""

# pylint: disable=protected-access
from abc import abstractmethod
from typing import Iterable, Union, Type, Any

import copy
import datetime
import importlib
from functools import reduce, partial
from inspect import isclass
from re import compile as recompile
from pathlib import Path
import jsonpickle as jp

from ._errors import UnknownTypeError, ImportModuleError, DataIceExists
from ._base_archive import BaseArchiveHandler
from ._dir_archive import DirectoryHandler
from ._pip import get_pip_freeze

jp.set_encoder_options("json", sort_keys=True, indent=4)
_class_name = recompile("(?<=')(.*)(?=')")

BASE_OBJECTS = (
    str,
    int,
    float,
    complex,
)


def get_full_class_definition(kls):
    """The full class definition from a variable. E.g. a.b.c"""
    kls = str(kls.__class__)
    return _class_name.findall(kls)[0]


def import_object_by_definition(definition):
    """Dynamic importing of an object by it's definition. E.g. 'a.b.c' returns c"""
    return reduce(
        getattr, definition.split(".")[1:], __import__(definition.partition(".")[0])
    )


def _recursive_save(parent, savename):
    """Recursively save an object."""

    jvars = list()  # json vars

    # get variables from class and separate types
    for var, val in parent.__dict__.items():
        # print(var, type(val), )
        # if isinstance(val, pd.DataFrame):
        #     dfvars.append(var)
        # elif isinstance(val, xr.Dataset):
        #     xrdsvars[var] = {
        #         ind: tuple(val.coords.indexes[ind].names)
        #         for ind in val.coords.keys()
        #     }
        # elif isinstance(val, xr.DataArray):
        #     xrdavars.append(var)
        # elif var in self._bdmcol:  # BaseDataModel are hidden in dict as collection.
        #     bdmvars[var] = {
        #         subvar: subval._recursive_save(subvar, savename)
        #         for subvar, subval in val.items()
        #     }
        # elif isinstance(val, BaseDataModel):
        #     bdmvars[var] = val._recursive_save(var, savename)
        # if str(type(val)).split(".")[0] in EXECLUDED_SAVE_CLASSES:
        #     pass  # ignore ecl class objects these cannot be saved
        # else:
        jvars.append(var)

    return {parent.__name__: jvars}


def _get_json_meta(meta=None):
    """Get the meta data for the archive"""
    jvars = dict()
    jvars["pip_freeze"] = get_pip_freeze()
    date = datetime.datetime.now()
    jvars["datestr"] = f"{date.year:4d}-{date.month:2d}-{date.day:2d}"
    jvars["timestr"] = f"{date.hour}:{date.minute}:{date.second}"
    if meta:
        jvars.update(meta)
    return jp.encode(jvars)


def ice(
    filepath: Union[str, Path],
    archive_handler: Union[BaseArchiveHandler, Any] = None,
    meta: dict = None,
    **kwargs,
):
    """ice your object using the registered rules for each type cotained within the object.

    Args:
        filepath: The filepath to output the data to.
        *args: The objects to save to the filepath.
        archive (Optional): Wrap the output in an archive file (tar unless zip=zip). Defaults to True.
        meta (Optional: None): Defaults to None, additional dictionary of metadata to ice to the archive.
        zip (Optional): Defaults to False.

    Raises:
        If an object is not recognised the process will return an error.
    """
    if archive_handler:
        Archive = archive_handler
    else:
        Archive = DirectoryHandler(filepath)

    Archive.save(**{"meta.json": _get_json_meta(meta)})

    for arg, val in kwargs.items():
        jvars = dict()
        if type(arg) in BASE_OBJECTS:
            jvars[arg] = val
        elif isinstance(val, Iterable) or isclass(val):
            jvars.update({arg: _recursive_save(val, filepath)})
        else:
            raise UnknownTypeError(type(arg))

        fname = arg + ".json"
        freeze = jp.encode(jvars)
        Archive.save(**{fname: freeze})


# class BaseDataModel:
#     """Abstract Base Class for data models. Handles saving and loading of data.
#     """

#     _save_header = "# etlpy DataModelBase class instance save file."

#     def __init__(self, save_header=None):
#         """Base Class init
#         Args:
#             save_header (string, optional): The description to put at the top of the
#                 output save file. Defaults to default description.
#         """
#         if save_header is not None:
#             self._save_header = "# " + save_header
#         self._dfvars = list()
#         self._xrdavars = dict()
#         self._xrdsvars = dict()
#         self._bdmcol = list()
#         self._bdmvars = list()
#         self._myclass = get_full_class_definition(self)

#     def _recursive_save(self, parent, savename):
#         """If BaseDataModel is parent of variable then recursively save it.
#         """

#         jvars = list()  # json vars
#         dfvars = list()  # dataframe vars
#         xrdavars = list()  # xarray dataarray vars
#         xrdsvars = dict()  # xarray dataset vars
#         bdmvars = dict()  # base data model vars

#         # get variables from class and separate types
#         for var, val in self.__dict__.items():
#             # print(var, type(val), )
#             if isinstance(val, pd.DataFrame):
#                 dfvars.append(var)
#             elif isinstance(val, xr.Dataset):
#                 xrdsvars[var] = {
#                     ind: tuple(val.coords.indexes[ind].names)
#                     for ind in val.coords.keys()
#                 }
#             elif isinstance(val, xr.DataArray):
#                 xrdavars.append(var)
#             elif var in self._bdmcol:  # BaseDataModel are hidden in dict as collection.
#                 bdmvars[var] = {
#                     subvar: subval._recursive_save(subvar, savename)
#                     for subvar, subval in val.items()
#                 }
#             elif isinstance(val, BaseDataModel):
#                 bdmvars[var] = val._recursive_save(var, savename)
#             elif str(type(val)).split(".")[0] in EXECLUDED_SAVE_CLASSES:
#                 pass  # ignore ecl class objects these cannot be saved
#             else:
#                 jvars.append(var)

#         # add special save classes to json so are loaded again.
#         self._dfvars = dfvars
#         self._xrdavars = xrdavars
#         self._xrdsvars = xrdsvars
#         self._bdmvars = bdmvars

#         # save DataFrame to disk
#         for var in dfvars:
#             self.__dict__[var].to_hdf(f"{savename}.hdf5", f"{parent}_{var}")
#         for var in xrdavars:
#             try:
#                 self.__dict__[var].to_netcdf(
#                     f"{savename}.nc",
#                     group=f"{parent}_{var}",
#                     mode="a",
#                     engine="h5netcdf",
#                 )
#             except FileNotFoundError:
#                 self.__dict__[var].to_netcdf(
#                     f"{savename}.nc",
#                     group=f"{parent}_{var}",
#                     mode="w",
#                     engine="h5netcdf",
#                 )
#         for var, dims in xrdsvars.items():
#             # remove multi level indexing to enable save to netcdf
#             drop_multi_index = list()
#             for _, values in dims.items():
#                 drop_multi_index = drop_multi_index + list(values)
#             self.__dict__[var] = self.__dict__[var].reset_index(drop_multi_index)
#             # output
#             try:
#                 self.__dict__[var].to_netcdf(
#                     f"{savename}.nc",
#                     group=f"{parent}_{var}",
#                     mode="a",
#                     engine="h5netcdf",
#                 )
#             except FileNotFoundError:
#                 self.__dict__[var].to_netcdf(
#                     f"{savename}.nc",
#                     group=f"{parent}_{var}",
#                     mode="w",
#                     engine="h5netcdf",
#                 )
#             # restore index to keep working - the user will never know
#             self._set_xarray_data_index(var)

#         return {k: self.__dict__[k] for k in jvars}

#     def save(self, savename):
#         """Save the state of elasticsim to disk
#         Two files are output, a {simname}.esim file which has comments at the start
#         of the file with lines starting with '#'. The parameters of the class
#         are saved then in a JSON string over multiple lines.
#         Pandas DataFrame objects are saved to a separate file {simname.hdf5}
#         Data can be loaded back in to Python by creating an elasticsim class object
#         and using the elasticsim.load method.
#         Arguments:
#             savename (str): The path and prefix to use for the saved files.
#         """
#         # jp.set_encoder_options('json', sort_keys=True, indent=4)
#         # create the header data

#         date = datetime.datetime.now()
#         datestr = f"{date.year:4d}-{date.month:2d}-{date.day:2d}"
#         timestr = f"{date.hour}:{date.minute}:{date.second}"

#         dict_rep = self._recursive_save("main", savename)

#         # save json to disk
#         with open(f"{savename}.json", "w") as fout:
#             fout.writelines(
#                 [
#                     self._save_header,
#                     "\n",
#                     f"#  Create Date: {datestr}",
#                     "\n" f"#  Save Time:   {timestr}",
#                     "\n",
#                 ]
#             )
#             freeze = jp.encode(dict_rep)
#             fout.write(freeze)

#     def _set_xarray_data_index(self, var):
#         """Helper function for saving and loading xarray data to netcdf
#         I like to use multi-level indexing but netcdf doesn't support this. The
#         indexes must be reduced to coordinates before export and then this code
#         reinstates them afterwards. It also reinstates the MLI when loading from
#         disk. All this requires an addition json file to be creating which knows
#         what the MLI was before save and exit.
#         """
#         self.__dict__[var] = self.__dict__[var].set_index(**self._xrdsvars[var])

#     def _recursive_load(
#         self,
#         parent,
#         loadname,
#         thawed_json,
#         ignore_hdf5=False,
#         ignore_nc=False,
#         load_nc=False,
#     ):
#         """Recursively load BaseDataModels if variables of super classes.
#         """
#         for key in thawed_json.keys():
#             # print(key)
#             self.__dict__[key] = thawed_json[key]

#         # read in dataframes
#         if not ignore_hdf5:
#             for var in self._dfvars:
#                 self.__dict__[var] = pd.read_hdf(f"{loadname}.hdf5", f"{parent}_{var}")
#         # read in xarrays
#         if not ignore_nc:
#             for var in self._xrdsvars:
#                 if load_nc:
#                     self.__dict__[var] = xr.load_dataset(
#                         f"{loadname}.nc", group=f"{parent}_{var}", engine="h5netcdf",
#                     )
#                 else:
#                     self.__dict__[var] = xr.open_dataset(
#                         f"{loadname}.nc", group=f"{parent}_{var}", engine="h5netcdf",
#                     )
#                 self._set_xarray_data_index(var)
#             for var in self._xrdavars:
#                 self.__dict__[var] = xr.open_dataarray(
#                     f"{loadname}.nc", group=f"{parent}_{var}"
#                 )
#         # read in BaseDataModel
#         for var, vald in self._bdmvars.items():
#             if var in self._bdmcol:  # bdm were cointained in dict before save
#                 var_dict = dict()
#                 for key, kval in vald.items():
#                     try:
#                         blank = import_object_by_definition(kval["_myclass"])()
#                         blank._recursive_load(
#                             key, loadname, kval, ignore_hdf5, ignore_nc, load_nc
#                         )
#                         var_dict[key] = blank
#                     except OSError:
#                         print(f"couldn't find {key}:{kval}")
#                 self.__dict__[var] = var_dict
#             else:  # plain bdm variable
#                 blank = import_object_by_definition(vald["_myclass"])()
#                 blank._recursive_load(
#                     var, loadname, vald, ignore_hdf5, ignore_nc, load_nc
#                 )
#                 self.__dict__[var] = blank

#     def load(self, loadname, ignore_hdf5=False, ignore_nc=False, load_nc=False):
#         """Load the sate of elasticsim from disk.
#         Input is an elasticsim file created with elasticsim.save called
#         {simname}.esim file which has comments at the start
#         of the file with lines starting with '#'. The file contains a json
#         formatted string which can be eddited or added to as required using a
#         standard text editor.
#         If the file contains values in _dfvars variable the program will look
#         for a {simname.hdf5} file containing Pandas DataFrame objects with
#         names equal to the values in _dfvars.
#         Arguments:
#             simname (str): The path and prefix to the input file.
#         """
#         loadname = str(loadname)
#         fin = open(loadname + ".json", "r")
#         line = ""
#         for line in fin:
#             if line[0] == "#":
#                 pass  # skip comments
#             else:
#                 break
#         # read in json minus formatting
#         json = line.strip() + "".join([l.rstrip().lstrip() for l in fin])
#         thawed = jp.decode(json)
#         self._recursive_load("main", loadname, thawed, ignore_hdf5, ignore_nc, load_nc)

#     def get_summary(self):
#         """Return a dictionary containing a summary of the data properties.
#         Returns:
#             dict: Summary of properties.
#         """
#         return {"type": self._myclass.split(".")[-1]}

#     def __copy__(self):
#         another_me = self.__class__()
#         for atr in self.__dict__:
#             another_me.__dict__[atr] = copy.copy(self.__dict__[atr])
#         return another_me

#     def copy(self):
#         return self.__copy__()
