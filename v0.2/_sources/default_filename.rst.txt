Default Filename
================

If no filename is given to ``vscode-cli-helpers-open-file open``
(see :doc:`usage`), a default filename will be used. The default filename is
given by option ``Filename`` in section ``[Defaults]`` of the configuration file.
See :doc:`configuration` for more information about the configuration file.

A default name for each language can also be specified in the section ``[DefaultFilenames]``
in the configuration file. The key is the language name, and the value is the default filename.
See the
`default config file <https://github.com/hakonhagland/vscode_cli_helpers.open_file/blob/main/src/vscode_cli_helpers/open_file/data/default_config.ini>`_
for the initial default values.
