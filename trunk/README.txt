Author
------

Holger Schurig, holgerschurig using the domain gmx point de
schurig on #asterisk, #asterisk-dev and #destar at irc.freenode.net



Warning
-------

If you look for some finished product, then look somewhere else. If you
look for something that can be easily tailerd to your suit (and you don't
fear a simple programming language), then look here.



Copyright
---------

The code is copyrighted by GPL, see GPL-2.txt and COPYRIGHT.txt for hints on
how to use this code in a commerical environment.




Rationale
---------

We all know that the Asterisk PBX is highly configurable. However,
configuring Asterisk can be a daunting thing, because you have to
deeply into the internals.

This is, because Asterisk is configurable at a very low-level. Quite
powerful, but low-level.

This web application eases this by switching the focus.

We have SIP Phones, IAX Phones, CAPI Lines and so on. You create this
objects and edit them. And DeStar will create your sip.conf, iax.conf,
dialplan in extensions.conf, whatever.




Organisation
------------

We have a backend and a frontend. See BACKEND.txt and (wow, you guessed it!)
FRONTEND.txt for more info.

First the backend. It provides the various configlets that can hold info. And
it contains the code that takes all of this configlets and produces the
various Asterisk *.conf config files. You can even run it without the
frontend, 'python backend.py' will do the trick.

Now on to the frontend. This provides a web interface. It uses Quixote and
therefore it can run under Apache with CGI, FCGI, mod_python or whatever.
See the Quixote documentation for more info. For my development I use it
under a standalone webserver named Medusa. The executable python script
'destar' uses this. Just start it and point your web-browser to
http://127.0.0.1:8080. For more info, please refer to INSTALL.txt.





Why
---

Why do I do just another GUI?

* Because I can.
* Because nothing similar exists.




Why not
-------

And why I didn't jump on some existing project:

* I don't know PHP, I know Perl and (preferred) Python

* I don't want to have a GUI that runs on Linux itself, e.g. in Qt or GTK
  and therefore needs file access to /etc/asterisk

* I don't want something that is just an text editor via web, e.g. where I
  can select a config file and inside the config file the section.




Webpages & Source Code
----------------------
* http://developer.berlios.de/projects/destar/
* http://svn.berlios.de/viewcvs/destar/trunk/


Source code for read-only access:

* svn checkout svn://svn.berlios.de/destar

Source code for an DeStar developer:

* export SVN_SSH="ssh -l developername"
* svn checkout svn+ssh://svn.berlios.de/svnroot/repos/destar
