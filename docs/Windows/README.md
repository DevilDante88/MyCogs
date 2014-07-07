Compiling MyCogs for OSX
==========================

To achieve the compilation of MyCogs App for OSX, you should follow this guide step-by-step

Prerequisites
-------------------------------------

* [PyInstaller 2.1](www.pyinstaller.com)
* Python 2.7
* OSX system

Pre-compiling
-------------------------------------

These steps are required to make your system ready to build MyCogs app

Download and install buildozer and some dependencies

	apt-get install python-buildozer
	
	
Copy and paste mycogs.spec file 
Open mycogs.spec with a text editor and edit the 3 paths to fit your installation path.
	
Compiling
-------------------------------------

Copy the file buildozer.spec (from this repository folder) inside the project folder

	cd /path/to/MyCogs/folder
	buildozer -v android debug
	
this process will take about 10 minutes depending on your internet connection.
If all works good, the terminal output should say you that the file MyCogs-1.2.0.debug.apk
has been created.




