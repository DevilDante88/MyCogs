Compiling MyCogs for Android
==========================

To achieve the compilation of MyCogs App for Android, you should follow this guide step-by-step

Prerequisites
-------------------------------------

* Linux OS
* Python 2.7
* an Android device (preferable a tablet) or a running Android emulator


Pre-compiling
-------------------------------------

These steps are required to make your system ready to build MyCogs app

Download and install buildozer and some dependencies

	sudo pip install --upgrade cython
	sudo dpkg --add-architecture i386
	sudo apt-get update
	sudo apt-get install build-essential ccache git ia32-libs libncurses5:i386 libstdc++6:i386 python2.7 python2.7-dev openjdk-7-jdk unzip zlib1g-dev zlib1g:i386
	apt-get install python-buildozer
	
Compiling
-------------------------------------

Copy the file buildozer.spec (from this repository folder) inside the project folder

	cd /path/to/MyCogs/folder
	buildozer -v android debug
	
this process will take about 10 minutes depending on your internet connection.
If all works good, the terminal output should say you that the file MyCogs-1.2.0.debug.apk
has been created.

Install & Run
-------------------------------------

Make sure your device is connected or your emulator is running (Android version suggested 4.4)

	adb install -r /path/to/MyCogs/apk
	
After just few seconds your app should be installed on the device.
Open the device menu and start your app

If you want to debug your app, just open a new terminal and launch

	adb logcat




