#! /usr/bin/env python3

import logging
import platform
import subprocess
from pathlib import Path
from typing import Optional

import click
import colorama
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

from vscode_cli_helpers.open_file.config import Config
from vscode_cli_helpers.open_file.exceptions import ConfigException
from vscode_cli_helpers.open_file.open_file import OpenFile

# To be used with make_rst_to_ansi_formatter()
doc_url = "https://hakonhagland.github.io/vscode-cli-helpers-open-file/main/"
# CLI colors for make_rst_to_ansi_formatter()
cli_colors = {
    "heading": {"fg": colorama.Fore.GREEN, "style": colorama.Style.BRIGHT},
    "url": {"fg": colorama.Fore.CYAN, "style": colorama.Style.BRIGHT},
    "code": {"fg": colorama.Fore.BLUE, "style": colorama.Style.BRIGHT},
}
click_command_cls = make_rst_to_ansi_formatter(doc_url, colors=cli_colors)


def edit_config_file(config: Config) -> None:
    """Edit the config file."""
    config_path = config.get_config_file()
    edit_file(config, config_path)


def edit_file(config: Config, file: Path) -> None:
    """Edit the config file."""
    cfg = config.config["Editor"]
    if platform.system() == "Linux":
        editor = cfg["Linux"]
        cmd = editor
        args = [str(file)]
    elif platform.system() == "Darwin":
        cmd = "open"
        editor = cfg["MacOS"]
        args = ["-a", editor, str(file)]
    elif platform.system() == "Windows":
        editor = cfg["Windows"]
        cmd = editor
        args = [str(file)]
    else:
        raise ConfigException(f"Unknown platform: {platform.system()}")
    logging.info(f"Running: {cmd} {args}")
    subprocess.Popen([cmd, *args], start_new_session=True)


def edit_template_file(config: Config, template: Optional[str], version: int) -> None:
    """Edit the template file."""
    path = config.get_template_path(template, version)
    edit_file(config, path)


@click.group(cls=make_rst_to_ansi_formatter(doc_url, group=True))
@click.option("--verbose", "-v", is_flag=True, help="Show verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """``vscode-cli-helpers-open-file`` is a command line tool for opening new
    or existing files in VS Code and navigating to a specific line.
    """
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose
    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


@main.command(cls=click_command_cls)  # type: ignore
@click.option(
    "--print-path", is_flag=True, help="Only print the path of the config file"
)
def edit_config(print_path: bool) -> None:
    """``vscode-cli-helpers-open-file edit-config`` lets you edit the config file. You can
    specify the editor to use for editing the config file in the config file itself. If the
    config file does not exist (the first time you edit it), it will be created with default
    values. See
    `default_config.ini <https://github.com/hakonhagland/vscode_cli_helpers.open_file/tree/main/src/vscode_cli_helpers/open_file/data/default_config.ini>`_
    for the default values. For more information about the config file, see the documentation section
    :doc:`/configuration`.
    """  # noqa: B950
    config = Config()
    if print_path:
        path = config.get_config_file()
        print(f"{str(path)}")
    else:
        edit_config_file(config)


@main.command(cls=click_command_cls)  # type: ignore
@click.argument("template", type=str, required=False)
@click.option(
    "--print-path", is_flag=True, help="Only print the path of the template file"
)
@click.option(
    "--version",
    type=click.IntRange(1, None),
    default=1,
    help="Template version number (must be a positive integer)",
)
def edit_template(template: str, print_path: bool, version: int) -> None:
    """``vscode-cli-helpers-open-file edit-template`` lets you edit a template file. See the
    `default_config.ini <https://github.com/hakonhagland/vscode_cli_helpers.open_file/tree/main/src/vscode_cli_helpers/open_file/data/default_config.ini>`_
    for the TEMPLATE names that are recognized by default. For example, ``Python`` is recognized
    by default, and is associated with the file extension ``.py``. For example, ::

      $ vscode-cli-helpers-open-file edit-template Python

    will open the template file ``Python.txt`` in the default editor. If the template file does not
    exist, it will be created empty. In some cases, you may want to have multiple versions of
    a template for a given language. For example, for Python you may want one version for creating
    a script, and one version for creating a module. In that case, you can specify the version number with the ``--version`` option.
    For example, ::

        $ vscode-cli-helpers-open-file edit-template Python --version 2

    will open the template file ``Python__2.txt`` in the default editor. If you specify a version using the ``--version`` option, the value should be an integer > 1. To use the default template
    (version 1), omit the ``--version`` option. The version number is appended to the template name with two underscores. When opening a file with the ``open`` command, you can specify the template to use with the ``--template`` option, and optionally the version with the ``--version`` option.

    For more information about the template file, see the documentation section :doc:`/template`.
    """  # noqa: B950
    config = Config()
    if print_path:
        print(f"{config.get_template_path(template, version)}")
    else:
        edit_template_file(config, template, version)


@main.command(cls=click_command_cls)  # type: ignore
@click.argument("path", type=str, required=False)
@click.option("--template", type=str, help="specify the template to use")
@click.option(
    "--executable/--no-executable", default=False, help="Make the file executable"
)
@click.option(
    "--version",
    default=1,
    type=click.IntRange(1, None),
    help="Template version number (must be a positive integer)",
)
def open(
    path: Optional[str], template: Optional[str], executable: bool, version: int
) -> None:
    """``vscode-cli-helpers-open-file open`` lets you open a new
    or existing file in VS Code and navigating to a specific line number.
    You almost certainly want to consider creating terminal aliases for this command with
    the file types you use most often, see
    :doc:`Creating an alias <alias>` for more information.

    If the ``--template`` option is not used, the file extension of ``PATH`` will be used
    to determine the template to use. If the :doc:`file extension <file_extension>` is not
    recognized, a default template will be used. For more information about specifying the
    default template, see :doc:`/template`. Optionally, you can specify a template version
    with the ``--version`` option. See the documentation for the ``edit-template`` command
    for more information about template versions.

    If the file exists, it will be opened in VS Code at line 1 or at a specified line number.
    If the file does not exist, it will be created and the template will be written to the
    file before opening it in VS Code. If the :doc:`template file type <configuration>` is
    "script" it will also be made executable.

    If no filename is given for PATH, a default filename will be used. For more information
    about specifying the default filename, see :doc:`/default_filename`.

    EXAMPLES ::

      $ vscode-cli-helpers-open-file open a.py

    If ``a.py`` exists, opens it in VS Code and navigates to line 1. If ``a.py`` does not exist,
    determines the file type from the extension of ``a.py`` (``.py``). Then creates a
    file ``a.py`` and writes a template for the file type ``.py`` to the file. If the
    ``--executable`` option is given, the file will also be made executable. Then opens the file
    in VS Code and navigates to line 1. ::

      $ vscode-cli-helpers-open-file open a

    If ``a`` exists, opens it in VS Code and navigates to line 1. If ``a`` does not exist,
    the file type will be determined from the default template (since ``--template`` option
    is not given). For example, if the default template is "Python", ``a.py`` will be
    created and made executable. Then the template will be written to the file
    before opening it in VSCode. ::

      $ vscode-cli-helpers-open-file open a:10
      $ vscode-cli-helpers-open-file a.py:10

    Sames as above but also navigates to line 10

    For more information about editing the template file, see :doc:`/template`.
    For information about specifying the file type of the templates, see :doc:`/configuration`.

    """
    OpenFile(path, template, executable, version).open()


if __name__ == "__main__":  # pragma: no cover
    main()
