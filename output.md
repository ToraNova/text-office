# foo

Hello bar, this file will first be processed by python's string.Template module using `boilergen.py`. It can then be fed to `docxtool.py`.

To process this, use the 'kvsub' module by invoking the following:

```
boilergen.py kvsub samples/kvboil.md --data "heading=foo,name=bar"
```
