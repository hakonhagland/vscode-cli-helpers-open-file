Configuration
=============

The configuration file is named ``config.ini`` and is located in sub directory
``vscode-cli-helpers-open-script`` inside directory ``user_config_dir`` as defined
by the `platformdirs <https://pypi.org/project/platformdirs/>`_ package.

.. note::
    You can open the config file in the default editor by running sub command ``edit-config``
    see :doc:`usage` for more information.

The syntax for the config file is described in the documentation for the
`configparser <https://docs.python.org/3/library/configparser.html>`_ module
in the Python standard library.

* Refer to :doc:`/usage`: When using the ``open`` sub command, if the ``--template``
  option is not used, the file extension of the filename will be used to determine the template.
  For example, if you try to open ``test.py`` and if the extension ``.py`` has been declared like
  this in the config file ::

        [FileExtensions]
        py = Python

   the ``Python.txt`` template will be used.  the Python the :doc:`file extension <file_extension>` is not
    recognized, a default template will be used. For more information about specifying the
    default template, see :doc:`/usage`.
To specify a default template to use for creating new files, use the ``Template`` option in the
  ``[Defaults]`` section. Example ::

        [Defaults]
        Template = Python   # default template is Python

  the template name is case-sensitive and must match one of the names in the ``[FileExtensions]``
  section. See the
  `default config file <https://github.com/hakonhagland/vscode_cli_helpers.open_file/blob/main/src/vscode_cli_helpers/open_file/data/default_config.ini>`_
  for a list of file extensions that are recognized by default.

* You can mark a template as a "script" to make the file executable. To do this, add the
  language to the ``Languages`` option under the ``[ScriptFiles]`` section. Example ::

        [ScriptFiles]
        Languages = Bash, Python, Perl, Ruby, Tcl

  Files created from templates "Bash", "Python", "Perl", "Ruby", and "Tcl" will now be made
  executable.

  .. note::
    It is not possible to make the python script directly executable on Windows, see
    section :doc:`windows` for more information of how to work around this.

  The ``Languages`` option is case-sensitive and must match one of the names in the
  ``[FileExtensions]`` section.

* To specify the editor to use for opening files, use the OS name option in the
  ``[Editor]`` section. Example ::

        [Editor]
        Windows = code     # use code for opening files on Windows
        Linux = code       # use code for opening files on Linux
        Darwin = code      # use code for opening files on macOS

.. note::
    See the default config file
    `default_config.ini <https://github.com/hakonhagland/vscode_cli_helpers.open_file/blob/main/src/vscode_cli_helpers/open_file/data/default_config.ini>`_
    for the current values of the default editor. The values you specify in configuration file
    will override the default values.

* See the :doc:`template` section for more information about how to modify the templates for each language.
