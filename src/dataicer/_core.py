"""
"""

# pylint: disable=protected-access
from typing import Union, Any

import datetime
from pathlib import Path
import jsonpickle as jp

from ._pip import get_pip_freeze
from ._utils import PathType

jp.set_encoder_options("json", sort_keys=True, indent=4)


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


def list_handlers() -> dict:
    """List all the known jsonpickle handlers"""
    base = jp.handlers.registry._base_handlers
    extra = jp.handlers.registry._handlers
    return {"base": base, "extra": extra}
