import re

from vscode_cli_helpers.open_file.exceptions import ConfigException, OpenFileException


def test_config_exception() -> None:
    try:
        raise ConfigException("Testing")
    except ConfigException as exc:
        msg = str(exc)
        assert re.search(r"Testing", msg)


def test_open_file_exception() -> None:
    try:
        raise OpenFileException("Testing")
    except OpenFileException as exc:
        msg = str(exc)
        assert re.search(r"Testing", msg)
