import pytest

from collections import OrderedDict
from tarfile import TarInfo
from zipfile import ZipInfo

from dataicer._utils import get_full_class_definition, import_object_by_definition


@pytest.mark.parametrize(
    "kls,result",
    [
        (OrderedDict(), "collections.OrderedDict"),
        (TarInfo(), "tarfile.TarInfo"),
        (ZipInfo(), "zipfile.ZipInfo"),
    ],
)
def test_get_full_class_definition(kls, result):
    assert get_full_class_definition(kls) == result
