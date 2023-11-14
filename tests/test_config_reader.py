import logging
import re
from pathlib import Path

# import os
import pytest
from _pytest.logging import LogCaptureFixture
from pytest_mock.plugin import MockerFixture

from vscode_cli_helpers.open_file.config_reader import ConfigReader
from vscode_cli_helpers.open_file.exceptions import ConfigException


class TestMain:
    @pytest.mark.parametrize(
        "is_dir,bad_content", [(False, False), (True, False), (False, True)]
    )
    def test_exceptions(
        self,
        is_dir: bool,
        bad_content: bool,
        caplog: LogCaptureFixture,
        data_dir_path: Path,
        mocker: MockerFixture,
    ) -> None:
        caplog.set_level(logging.INFO)
        cfg = ConfigReader()
        data_dir = data_dir_path
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=data_dir,
        )
        cfg_dir = cfg.get_config_dir()
        lock_file = cfg_dir / "xyz"
        if is_dir:
            lock_file.mkdir(parents=True)
        if bad_content:
            with open(str(lock_file), "w", encoding="utf_8") as fp:
                fp.write("xyz")
        with pytest.raises(ConfigException) as excinfo:
            cfg.check_correct_config_dir(lock_file)
        if not is_dir and not bad_content:
            assert re.search(r"Config dir lock file: missing", str(excinfo))
        elif is_dir and not bad_content:
            assert re.search(r"Config dir lock file: is a directory", str(excinfo))
        elif not is_dir and bad_content:
            assert re.search(r"Config dir lock file: bad content", str(excinfo))

    @pytest.mark.parametrize("exists,is_file", [(True, True), (False, False)])
    def test_exceptions2(
        self,
        is_file: bool,
        exists: bool,
        caplog: LogCaptureFixture,
        data_dir_path: Path,
        mocker: MockerFixture,
    ) -> None:
        caplog.set_level(logging.INFO)
        cfg = ConfigReader()
        data_dir = data_dir_path
        config_dir = data_dir
        if is_file:
            some_file = data_dir / "some_file"
            with open(some_file, "w", encoding="utf_8") as fp:
                fp.write("xyz")
            config_dir = some_file
        if not exists:
            config_dir = data_dir / "some_dir"
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=config_dir,
        )
        if is_file:
            with pytest.raises(ConfigException) as excinfo:
                cfg.get_config_dir()
            assert re.search(r"Config directory .* is file", str(excinfo))
        if not exists:
            cfg.get_config_dir()
            assert True
