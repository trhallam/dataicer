import pytest

from dataicer._errors import (
    UnknownTypeError,
    ImportModuleError,
)

def test_unknown_type():
    with pytest.raises(UnknownTypeError):
        raise UnknownTypeError(int)

def test_import_module():
    with pytest.raises(ImportModuleError):
        raise ImportModuleError
