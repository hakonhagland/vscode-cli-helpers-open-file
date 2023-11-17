Templates
=========

The template files are located in subdirectory
``vscode-cli-helper-open-script/templates`` inside directory ``user_config_dir`` as defined
by the `platformdirs <https://pypi.org/project/platformdirs/>`_ package.

.. note::
    You can open a template file in the default editor by running sub command ``edit-template``
    see the :doc:`usage` section for more information.

.. note::
    See the default template files in the
    `vscode_cli_helpers/open_file/data/templates/ <https://github.com/hakonhagland/vscode_cli_helpers.open_file/blob/main/src/vscode_cli_helpers/open_file/data/templates>`_
    directory in the source code repository. The default template for a given language is copied
    to the template directory the first time you run the script with a given template and the template
    file is missing.
