Windows
=======

How to make a script executable
-------------------------------

In Windows CMD or PowerShell you usually have to run the Python script like this: ::

  > python myscript.py

To avoid having to type ``python`` in front of the script, you can try the following
approaches :

* Make a Batch file wrapper for the python script, or
* Create a PowerShell function wrapping the python command, e.g. ::

    function py { python $args }

  Then you can run the script like this: ::

    > py myscript.py

  Or,
* On Windows, the standard Python installer already associates the ``.py`` extension
  with a file type (``Python.File``) and gives that file type an open command that
  runs the interpreter, e.g. ``D:\Program Files\Python\python.exe "%1" %*``. This is
  enough to make scripts executable from the command prompt as ``foo.py``.

  A drawback of this approach is that, if you are using multiple Python installations
  concurrently, you may need to re-associate ``.py`` files with the correct interpreter.
  Also, the CMD or PowerShell will open a new console window for each script run. This
  can be inconvenient since the new console window will disappear when the script
  finishes executing.

  If you'd rather be able to execute the script by simple typing ``foo`` with no extension
  you need to add ``.py`` to the ``PATHEXT`` environment variable.

  See the `Python Windows FAQ <https://docs.python.org/3/faq/windows.html>`_ for more information.
