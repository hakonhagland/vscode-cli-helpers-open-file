Filename Extension
==================

The script will add a filename extension if it is missing. First, if the filename
represent an existing file the script will assume that the user wants to open that
file and an extension is not added.

However, if the filename does not represent an existing file the script will
consider two things to determine the extension to add. First, it determines the desired
extension from the template name. For example, if the script is run like this
``vscode-cli-helpers-open-file open --template=Python foo`` it will know that
the desired extension will be ``.py`` by looking at ``Python`` option in the
``[FileExtensions]`` section of the config file. If the template name is not given
explicitly on the command line the default template name under the ``[Default]``
section will be used instead.

Second, to determine how to create a new filename with correct extension,
the filename is split into parts by the dot character and each part is
considered separately.
The specific rules used are best
illustrated by the following examples for the template ``C++``

.. list-table:: Examples given **known** template name ``C++``
   :widths: 10 10 10 11
   :header-rows: 1

   * - Filename
     - Extension
     - New Filename
     - Comment
   * - ``hello``
     - ``.cpp``
     - ``hello.cpp``
     -
   * - ``hello.cpp``
     - ``.cpp``
     - ``hello.cpp``
     -
   * - ``.cpp``
     - ``.cpp``
     - ``.cpp.cpp``
     -
   * - ``.hello``
     - ``.cpp``
     - ``.hello.cpp``
     - not ``.hello``
   * - ``a.hello``
     - ``.cpp``
     - ``a.hello.cpp``
     - not ``a.hello``
   * - ``hello.``
     - ``.cpp``
     - ``hello.cpp``
     - not ``hello..cpp``
