import pytest

from dataicer._pip import get_pip_freeze

def test_get_pip_freeze():
    frozen_pip_list = get_pip_freeze()
    assert isinstance(frozen_pip_list, list)
