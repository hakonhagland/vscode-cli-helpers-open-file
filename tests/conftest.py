# import logging
import shutil
from pathlib import Path

# import typing
import pytest

from vscode_cli_helpers.open_file.config_reader import ConfigReader

PytestDataDict = dict[str, str]


@pytest.fixture(scope="session")
def test_file_path() -> Path:
    return Path(__file__).parent / "files"


@pytest.fixture(scope="session")
def test_data() -> PytestDataDict:
    return {
        "config_dir": "config",
        "data_dir": "data",
    }


@pytest.fixture()
def data_dir_path(
    tmp_path: Path, test_file_path: Path, test_data: PytestDataDict
) -> Path:
    data_dir = tmp_path / test_data["data_dir"]
    data_dir.mkdir()
    data_dirlock_fn = test_file_path / test_data["data_dir"] / ConfigReader.dirlock_fn
    shutil.copy(data_dirlock_fn, data_dir)
    return data_dir
