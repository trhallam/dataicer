from _pytest.nodes import File
import pytest
import pathlib

from dataicer._dir_archive import FileHandler, DirectoryHandler


@pytest.mark.parametrize("mode", ("w", "a"))
def test_FileHandler_writeable(tmpdir, mode):
    fname = "FileHandlerTest.txt"
    with FileHandler(tmpdir, fname, mode=mode) as fh:
        fh.write("test text")

    with open(tmpdir / fname, "r") as fr:
        assert fr.readlines() == ["test text"]


def test_FileHandler_readable(tmpdir):
    fname = "FileHandlerTest.txt"
    fpath = pathlib.Path(tmpdir) / fname
    with open(fpath, "w") as fw:
        fw.write("test text")
    with FileHandler(tmpdir, fname, mode="r") as fh:
        assert fh.readlines() == ["test text"]


def test_DirectoryHandler_has_archive_type(directory_handler):
    assert directory_handler._archive_type == "directory"


@pytest.fixture(scope="function")
def mock_directory_handler(tmpdir):
    dirname = "mock_directory_handler"
    mockdir = pathlib.Path(tmpdir) / dirname
    mockdir.mkdir(exist_ok=True)

    for test_file in ["A", "B", "C"]:
        (mockdir / f"{test_file}.json").touch()

    return mockdir


@pytest.mark.parametrize("mode", ("w", "a"))
def test_DirectoryHandler_init_fresh_writeable(tmpdir, mode):
    tmpdir_unique = pathlib.Path(tmpdir) / f"mock_directory_handler_mode_{mode}"
    dh = DirectoryHandler(tmpdir_unique, mode)


@pytest.mark.parametrize("mode", ("w", "a"))
def test_DirectoryHandler_init_exists_writeable(mock_directory_handler, mode):
    dh = DirectoryHandler(mock_directory_handler, mode)


@pytest.mark.parametrize("mode", ("r"))
def test_DirectoryHandler_init_fresh_readable(mock_directory_handler, mode):
    dh = DirectoryHandler(mock_directory_handler, mode)


@pytest.mark.parametrize("mode", ("r"))
def test_DirectoryHandler_init_fresh__not_readable(tmpdir, mode):
    with pytest.raises(FileNotFoundError):
        dh = DirectoryHandler(tmpdir / "this_dir_does_not_exist", mode)


def test_DirectoryHandler_open_exists(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    with dh.open_file("A.json") as f:
        x = f.read()
    assert x == ""


def test_DirectoryHandler_open_new(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    with dh.open_file("D.json", "w") as f:
        f.write("test text")
    with dh.open_file("D.json", "r") as f:
        assert f.read() == "test text"


def test_DirectoryHandler_save_obj(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)

    dh.save(tc="test text")
    assert (mock_directory_handler / "tc.json").exists()

    with dh.open_file("tc.json", "r") as f:
        assert f.read() == "test text"


def test_DirectoryHandler_keys(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    for v in ["A", "B", "C"]:
        assert v in dh.keys()


def test_DirectoryHandler_getitem(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    for v in ["A", "B", "C"]:
        assert "" == dh[v]


def test_DirectoryHandler_iter_json(mock_directory_handler):
    dh = DirectoryHandler(mock_directory_handler)
    for key, contents in dh.iter_json():
        assert key in ["A", "B", "C"]
        assert contents == ""

    # with dh.open_file("tc.json")
