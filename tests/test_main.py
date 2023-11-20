import logging
import os
import platform
import re
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner
from pytest_mock.plugin import MockerFixture

import vscode_cli_helpers.open_file.script as script
from vscode_cli_helpers.open_file.exceptions import ConfigException


class TestMain:
    def test_help_opt(
        self,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        data_dir_path: Path,
    ) -> None:
        caplog.set_level(logging.INFO)
        data_dir = data_dir_path
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=data_dir,
        )
        runner = CliRunner()
        result = runner.invoke(script.main, ["--help"])
        assert result.stdout.startswith("Usage: main [OPTIONS] COMMAND [ARGS]")

    @pytest.mark.parametrize(
        "workspace,add_ext,line_no",
        [(True, False, False), (False, True, False), (False, False, True)],
    )
    def test_empty_arg(
        self,
        workspace: bool,
        add_ext: bool,
        line_no: bool,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        data_dir_path: Path,
        tmp_path: Path,
    ) -> None:
        caplog.set_level(logging.INFO)
        data_dir = data_dir_path
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=data_dir,
        )
        # NOTE: This line must be before we mock subprocess.Popen
        platform_name = platform.system()
        mocker.patch("subprocess.Popen", return_value=None)
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            cli_runner_cwd = os.getcwd()
            args = ["open"]
            if workspace:
                Path("a.code-workspace").touch()
            if add_ext:
                Path("t.py").touch()
                args.append("t.py")
            if line_no:
                args.append("t.py:10")
            runner.invoke(script.main, args)
        gen_file = Path(cli_runner_cwd) / "t.py"
        assert gen_file.exists()
        if platform_name == "Windows":  # pragma: no cover
            assert re.match(
                r"""Running: \['.*?code.cmd', '-g'""",
                caplog.records[-1].msg,
            )
        elif platform_name == "Darwin":  # pragma: no cover
            assert re.match(
                r"""Running: \['.*?/Contents/Resources/app/bin/code', '-g'""",
                caplog.records[-1].msg,
            )
        else:  # pragma: no cover
            assert caplog.records[-1].msg.startswith("""Running: ['code', '-g'""")

    @pytest.mark.parametrize("platform_name", ["Linux", "Windows", "Darwin", "Unknown"])
    def test_platform(
        self,
        platform_name: str,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        data_dir_path: Path,
        tmp_path: Path,
    ) -> None:
        caplog.set_level(logging.INFO)
        data_dir = data_dir_path
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=data_dir,
        )
        mocker.patch("platform.system", return_value=platform_name)
        mocker.patch("subprocess.Popen", return_value=None)
        if platform_name == "Windows":
            mocker.patch("shutil.which", return_value="code.cmd")
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            cli_runner_cwd = os.getcwd()
            args = ["-v", "open", "t.py"]
            runner.invoke(script.main, args)
        gen_file = Path(cli_runner_cwd) / "t.py"
        assert gen_file.exists()
        if platform_name == "Windows":  # pragma: no cover
            assert re.match(
                r"""Running: \['.*?code.cmd', '-g'""",
                caplog.records[-1].msg,
            )
        elif platform_name == "Darwin":
            assert re.match(
                r"""Running: \['.*?/Contents/Resources/app/bin/code', '-g'""",
                caplog.records[-1].msg,
            )
        else:  # pragma: no cover
            assert caplog.records[-1].msg.startswith("""Running: ['code', '-g'""")

    @pytest.mark.parametrize("os_name", ["Linux", "Windows", "Darwin", "Unknown"])
    def test_edit_config_file(
        self,
        os_name: str,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        data_dir_path: Path,
        tmp_path: Path,
    ) -> None:
        caplog.set_level(logging.INFO)
        mocker.patch("platform.system", return_value=os_name)
        data_dir = data_dir_path
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=data_dir,
        )
        mocker.patch("subprocess.Popen", return_value=None)
        runner = CliRunner()
        args = ["edit-config"]
        if os_name != "Unknown":
            with runner.isolated_filesystem(temp_dir=tmp_path):
                runner.invoke(script.main, args)
            if os_name == "Linux":
                assert caplog.records[-1].msg.startswith("""Running: gedit""")
            elif os_name == "Windows":
                assert caplog.records[-1].msg.startswith("""Running: notepad""")
            elif os_name == "Darwin":
                assert caplog.records[-1].msg.startswith(
                    """Running: open ['-a', 'TextEdit'"""
                )
        else:
            result = runner.invoke(script.main, args)
            assert isinstance(result.exception, ConfigException)
            assert (
                str(result.exception) == "Config exception: Unknown platform: Unknown"
            )

    def test_edit_template(
        self,
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
        args = ["-v", "edit-template"]
        with runner.isolated_filesystem(temp_dir=tmp_path):
            runner.invoke(script.main, args)
        assert caplog.records[-1].msg.startswith("""Running: gedit""")
