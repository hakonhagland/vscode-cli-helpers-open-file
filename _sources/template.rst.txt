Template
========

The configuration file is named ``config.ini`` and is located in sub directory
``vscode-cli-helper-open-script`` inside directory ``user_config_dir`` as defined
by the `platformdirs <https://pypi.org/project/platformdirs/>`_ package.

.. note::
    You can open the config file in the default editor by passing command line argument
    ``--edit-config``.
    See the default config file
    `default_config.ini <https://github.com/hakonhagland/vscode_cli_helpers.open_file/blob/main/src/vscode_cli_helpers/open_file/data/default_config.ini>`_
    for the current values of the default editor. The values you specify in configuration file
    will override the default values.

The syntax is described in the documentation for the
`configparser <https://docs.python.org/3/library/configparser.html>`_ module
in the Python standard library.

The template file is named ``python.txt`` and is located in sub directory
``vscode-cli-helper-open-script/templates`` inside directory ``user_config_dir`` as defined
by the `platformdirs <https://pypi.org/project/platformdirs/>`_ package.

.. note::
    You can open the template file in the default editor by passing command line argument
    ``--edit-template``.
    See the default template file
    `python.txt <https://github.com/hakonhagland/vscode_cli_helpers.open_file/blob/main/src/vscode_cli_helpers/open_file/data/templates/python.txt>`_
    for the current default template. This default template is copied to the template file
    the first time you run the script.
