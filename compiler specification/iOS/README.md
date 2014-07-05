Compiling MyCogs for iOS
======

To achieve the com

#. Prerequisites

* Apple computer
* Apple Developer ID


#. Pre-compiling

These steps are required to make your system ready to build MyCogs app

- if you haven't already installed, download and install XCode from AppStore
- install [BREW](http://brew.sh) and verify the correct installation by typing 'brew doctor' on your terminal
    
    ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
    brew doctor
    
- install those dependencies, open a terminal and type

    brew install autoconf automake libtool pkg-config mercurial
    brew link libtool
    brew link mercurial
    sudo easy_install pip
    sudo pip install cython
    
- now we need to download [kivy-ios](https://github.com/kivy/kivy-ios) from the terminal, typing:

    git clone git://github.com/kivy/kivy-ios
    
  once downloaded, we have to modify 3 files to include in our building both openssl and and lxml wich are needed in MyCogs app. 

    




