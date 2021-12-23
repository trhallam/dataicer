import pytest
import pathlib

from dataicer import ice
from dataicer._core import BASE_OBJECTS

@pytest.mark.parametrize(
    "baseobj", BASE_OBJECTS
)
def test_ice_baseobjects(tmpdir, baseobj):
    test_obj = baseobj(10)
    ice(tmpdir/"fakepath", a=test_obj, archive=False)

# @pytest.mark.parametrize(
#     "comp", ["gz", "bz2", "xz"]
# )
# def test_ice_tar(tmpdir, comp):
#     filename = pathlib.Path(tmpdir / "fakepath")
#     ice(tmpdir/"fakepath", compression=comp, a=2)

#     assert filename.with_suffix(".tar.{}".format(comp)).exists()

# @pytest.mark.parametrize(
#     "comp", ["zip"]
# )
# def test_ice_zip(tmpdir, comp):
#     filename = pathlib.Path(tmpdir / "fakepath")
#     ice(tmpdir/"fakepath", compression=comp, a=2)

#     assert filename.with_suffix(".{}".format(comp)).exists()