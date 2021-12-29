import pytest
import numpy as np

from dataicer import DirectoryHandler


@pytest.fixture(scope="module", params=[1, 2, 3], ids=["1d", "2d", "3d"])
def numpy_data(request):
    return {"np_data": np.zeros((5,) * request.param)}


@pytest.fixture(scope="function")
def directory_handler(tmpdir):
    tmpdir.remove()
    handler = DirectoryHandler(tmpdir, mode="w")
    return handler


@pytest.fixture()
def test_class():
    class TestClass:
        def __init__(
            self,
        ):
            self.a = 1
            self.b = 2.0
            self.c = 1 + 4j
            self.d = (1, 2, 3)
            self.e = [1, 2, 3]
            self.f = {"a": 1, "b": 2}

        def __eq__(self, other):

            for key, val in self.__dict__.items():
                other_val = getattr(other, key)
                if other_val is None:
                    return False

                if other_val != val:
                    return False

            return True

    return TestClass
