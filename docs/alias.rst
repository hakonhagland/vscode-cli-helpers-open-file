Creating an alias
=================

If you are using the ``vscode-cli-helper-new-python-script`` command
line script frequently, you may want to create a short alias for it like ``ny``
to avoid typing the full command each time.

Linux
-----

To create an alias on Linux, add the following line to your ``~/.bashrc``
file (if you are using Bash shell): ::

    alias ǹy='vscode-cli-helper-new-python-script'

macOS
-----

To create an alias on macOS, add the following line to your ``~/.bash_profile`` or
``~/.zshrc`` file: ::

    alias ǹy='vscode-cli-helper-new-python-script'

Windows
-------

To create an alias on Windows (PowerShell), add the following line to your
``%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1``
file: ::

    function vscode-cli-helper-new-python-script-function {
       vscode-cli-helper-new-python-script $args
    }
    SetAlias ny vscode-cli-helper-new-python-script-function
