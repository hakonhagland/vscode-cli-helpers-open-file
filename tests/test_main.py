import logging
import os
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner
from pytest_mock.plugin import MockerFixture

import vscode_cli_helpers.open_file.script as script


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
        assert result.stdout.startswith("Usage: main [OPTIONS] [PATH]")

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
        mocker.patch("subprocess.Popen", return_value=None)
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            cli_runner_cwd = os.getcwd()
            args = []
            if workspace:
                Path("a.code-workspace").touch()
            if add_ext:
                Path("t.py").touch()
                args = ["t.py"]
            if line_no:
                args = ["t.py:10"]
            runner.invoke(script.main, args)
        gen_file = Path(cli_runner_cwd) / "t.py"
        assert gen_file.exists()
        assert caplog.records[-1].msg.startswith("""Running: ['code', '-g'""")
