MyCogs
======

MyCogs, a multi-platform Information Retrieval application with the aim of extracting and generating knowledge from an email account (at the moment only from a gmail one). Realized in Python with the help of many different libraries as [Kivy](http://kivy.org), [NLTK](http://www.nltk.org), [wikipedia API for python](https://pypi.python.org/pypi/wikipedia/) and [ConceptNet5](http://conceptnet5.media.mit.edu) (some of them has been lightly modified to be able to run on all systems).

The workflow of this application is divided in 4 main steps:

1) Parse all mails or only those not already read (because MyCogs uses a sqlite3 DB to keep also track of emails IDs), 
and generate a list of senders extracting the real sender if it is a forwarded one.

2) The user has the ability to choose the sender from the generated list. After that, the program will extract the text from those mails and pulls out all the noun phrases. 
For each of these, MyCogs will look for one or more possible meanings on Wikipedia and at the same time will pull out some possible categories (like “animal” for “dog”)  from the KB [ConceptNet5](http://conceptnet5.media.mit.edu).

3) The last part allows the user to view the results, dividing the results obtained in 3 different tables: 

	“Approved” (when the program obtain one single result), 
	"Unapproved” (when no result is obtained),
	“Ambiguous” (when the program retrieved more results for that noun-phrase).

4) The desired results do not always correspond to those obtained and each user can have a "default meaning" for a particular noun phrase different between them. For this reason, each user can modify the data via the GUI and the program will learn from these changes for successive researches.

Prerequisites
-------------------------------------

* Python 2.7
* Cython


Source code installation
-------------------------------------

Just copy MyCogs folder and add it to yuor favorite Python IDE.

Support
-------

If you need assistance, you can ask for help directly to me:

* Email      : matteo.renzi.88@gmail.com

TODO list
----------

* generate a queryable category structure
* create a "search" screen
* implement a parallel computing for the textprocessing and information retrieval thread
* retrieve image from wikipedia (if possible)
* implement a multi-language noun phrase extraction (only english in supported at the moment)
* refer the category to the single meaning found in wikipedia and not from the original extracted NP

Known Bugs
------------

The application in still in development
* Wikipedia HTTP Error -- insert an error management
* check that all text is utf-8 encoded

Compilation Bugs
-----------------

* Compilation for OSX works good, but if you compile the application using OSX 10.9 the app will work only on OSX 10.9 systems (if you want to know more: https://github.com/kivy/kivy/wiki/Building-Portable-Package#mavericks--109-doesnt-work-at-the-moment)




