import pytest

# import numpy as np

from dataicer import list_handlers

# from dataicer.plugins import numpy as dinp
# from dataicer.plugins import pandas as dipd
# from dataicer.plugins import xarray as dixr


def test_list_handlers():
    handlers = list_handlers()
    assert isinstance(handlers, dict)
    assert "base" in handlers
    assert isinstance(handlers["base"], dict)
    assert "extra" in handlers
    assert isinstance(handlers["extra"], dict)


# # @pytest.mark.parametrize(
# #     "comp", ["gz", "bz2", "xz"]
# # )
# # def test_ice_tar(tmpdir, comp):
# #     filename = pathlib.Path(tmpdir / "fakepath")
# #     ice(tmpdir/"fakepath", compression=comp, a=2)

# #     assert filename.with_suffix(".tar.{}".format(comp)).exists()

# # @pytest.mark.parametrize(
# #     "comp", ["zip"]
# # )
# # def test_ice_zip(tmpdir, comp):
# #     filename = pathlib.Path(tmpdir / "fakepath")
# #     ice(tmpdir/"fakepath", compression=comp, a=2)

# #     assert filename.with_suffix(".{}".format(comp)).exists()
