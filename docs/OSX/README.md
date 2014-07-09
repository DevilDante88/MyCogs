Compiling MyCogs for OSX
==========================

To achieve the compilation of MyCogs App for OSX, you should follow this guide step-by-step

Prerequisites
-------------------------------------

* [PyInstaller 2.1](www.pyinstaller.org)
* Python 2.7
* OSX system

Pre-compiling
-------------------------------------

These steps are required to make your system ready to build MyCogs app

Download and install buildozer and some dependencies

	xcode-select --install
	sudo pip install lxml
	apt-get install python-buildozer
	
	
Copy and paste mycogs.spec file 
Open mycogs.spec with a text editor and edit the 3 paths to fit your installation path.
	
Compiling
-------------------------------------

Copy the file mycogs.spec (from this folder repository) inside the project folder. Then:

	cd PyInstaller-2.1
	kivy pyinstaller.py MyCogs/mycogs.spec
	pushd mycogs/dist
	mv mycogs mycogs.app
	hdiutil create ./MyCogs.dmg -srcfolder mycogs.app -ov
	popd



