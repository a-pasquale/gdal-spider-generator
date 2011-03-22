#Facilities Spider Generator

A commandline python utility to extract features from data layers and create new "spider" layers.

##Install

This script depends on the opensource [Geospatial Data Abstraction Library] [gdal] (GDAL).  Install this using [the binary of your choice] [binary].

You also need the python bindings for gdal, [available from pypi] [pypi] or via

     $ pip install GDAL

##Usage

The datasource from which the spiders are to be generated is passed as a parameter from the commandline.

	$ spider.py facilities.sqlite 

Any data format supported by the gdal library should be usable.  The facilities are split by usercode and a new layer is output for each usercode.


[gdal]:http://www.gdal.org
[binary]:http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries
[pypi]:http://pypi.python.org/pypi/GDAL/
