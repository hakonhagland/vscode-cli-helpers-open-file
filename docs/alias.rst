Creating an alias
=================

If you are using the ``vscode-cli-helpers-open-file open`` command
line script frequently, you almost certainly want to create a short alias for each
file type. For example, to open a new Python file and make the file executable
(i.e. ``chmod +x <file>``) you could create an alias with name ``np`` or ``ny`` (for "new Python") that
includes everything except the file name. This way, you can quickly create a new Python file
by typing ``ny <filename>`` in the terminal window. Here is more information of how you can create
an alias on different operating systems:

Linux
-----

To create an alias on Linux, add the following line to your ``~/.bashrc``
file (if you are using Bash shell): ::

    alias ǹy='vscode-cli-helpers-open-file open --template=Python --executable'

macOS
-----

To create an alias on macOS, add the following line to your ``~/.bash_profile`` or
``~/.zshrc`` file: ::

    alias ǹy='vscode-cli-helpers-open-file open --template=Python --executable'

Windows
-------

To create an alias on Windows (PowerShell), add the following line to your
``%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1``
file: ::

    function ny($args) {
       vscode-cli-helpers-new-open-file open --template=Python --executable $args
    }
