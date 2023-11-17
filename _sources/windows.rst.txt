Windows
=======

How to make a script executable
-------------------------------

In Windows CMD or PowerShell you usually have to run the Python script like this: ::

  > python myscript.py

To avoid having to type ```python`` in front of the script, you can try:

* Make a Batch file wrapper for the python script, or
* Create a PowerShell function wrapping the python command, e.g. ::

    function py { python $args }

  Then you can run the script like this: ::

    > py myscript.py
