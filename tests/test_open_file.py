import logging
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner
from pytest_mock.plugin import MockerFixture

import vscode_cli_helpers.open_file.script as script
from vscode_cli_helpers.open_file.exceptions import ConfigException


class TestMain:
    @pytest.mark.parametrize("language", ["C", "C++"])
    def test_not_script(
        self,
        language: str,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        data_dir_path: Path,
        tmp_path: Path,
    ) -> None:
        caplog.set_level(logging.INFO)
        mocker.patch("platform.system", return_value="Linux")
        data_dir = data_dir_path
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=data_dir,
        )
        mocker.patch("subprocess.Popen", return_value=None)
        runner = CliRunner()
        args = ["-v", "open"]
        if language == "C":
            args.extend(["--template=C", "hello.c"])
        else:
            args.extend(["--template=C++", "hello.cpp"])
        with runner.isolated_filesystem(temp_dir=tmp_path):
            runner.invoke(script.main, args)
        if language == "C":
            assert caplog.records[-1].msg.startswith(
                """Running: ['code', '-g', 'hello.c'"""
            )
        else:
            assert caplog.records[-1].msg.startswith(
                """Running: ['code', '-g', 'hello.cpp'"""
            )

    @pytest.mark.parametrize("language", ["Shell", "foobar"])
    def test_extension(
        self,
        language: str,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        data_dir_path: Path,
        tmp_path: Path,
    ) -> None:
        caplog.set_level(logging.INFO)
        mocker.patch("platform.system", return_value="Linux")
        data_dir = data_dir_path
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=data_dir,
        )
        mocker.patch("subprocess.Popen", return_value=None)
        runner = CliRunner()
        args = ["-v", "open", f"--template={language}", "foo"]
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(script.main, args)
        if language == "Shell":
            assert caplog.records[-1].msg.startswith(
                """Running: ['code', '-g', 'foo.sh'"""
            )
        else:
            assert isinstance(result.exception, ConfigException)
            assert str(result.exception) == (
                "Config exception: Could not find file extension "
                "for language: foobar"
            )

    @pytest.mark.parametrize("platform", ["Linux", "Windows"])
    def test_chmod(
        self,
        platform: str,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        data_dir_path: Path,
        tmp_path: Path,
    ) -> None:
        caplog.set_level(logging.INFO)
        mocker.patch("platform.system", return_value=platform)
        if platform == "Windows":
            mocker.patch("shutil.which", return_value="code")
        data_dir = data_dir_path
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=data_dir,
        )
        mocker.patch("subprocess.Popen", return_value=None)
        runner = CliRunner()
        args = ["-v", "open", "foo"]
        with runner.isolated_filesystem(temp_dir=tmp_path):
            runner.invoke(script.main, args)
        assert caplog.records[-1].msg.startswith("""Running: ['code', '-g', 'foo.py'""")
