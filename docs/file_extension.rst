File Extension
==============

The script will look at the filename to determine its file extension.
The file is split into parts by the dot character. The last part is
considered the file extension. The specific rules used are best
illustrated by the following examples for the template ``C++``:

* ``hello`` → ``hello.cpp``
* ``hello.cpp`` → ``hello.cpp``
* ``.cpp`` → ``.cpp.cpp``
* ``.hello`` → ``.hello.cpp`` (note: not ``.hello``)
* ``a.hello`` → ``a.hello.cpp`` (note: not ``a.hello``)
* ``hello.`` → ``hello.cpp`` (note: not ``hello..cpp``)
