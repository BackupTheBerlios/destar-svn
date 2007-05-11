Authors
------

Main development made initially by Holger Schurig, holgerschurig using 
the domain gmx point de
schurig on #asterisk, #asterisk-dev and #destar at irc.freenode.net

See http://developer.berlios.de/projects/destar/ to view other project
members and contributors.


Copyright
---------

The code is copyrighted by GPL, see GPL-2.txt and COPYRIGHT.txt for hints on
how to use this code in a commercial environment.


Rationale
---------

We all know that the Asterisk PBX is highly configurable. However,
configuring Asterisk can be a daunting thing, because you have to dig
deeply into the internals.

This is, because Asterisk is configurable at a very low-level. Quite
powerful, but low-level.

This web application eases this by switching the focus.

We have SIP Phones, IAX Phones, CAPI Lines and so on. You create this
objects and edit them. And DeStar will create your sip.conf, iax.conf,
dialplan in extensions.conf, whatever.


Organization
------------

We have a backend and a frontend. See BACKEND.txt and (wow, you guessed it!)
FRONTEND.txt for more info.

First the backend. It provides the various configlets that can hold info. And
it contains the code that takes all of this configlets and produces the
various Asterisk *.conf config files.
 
Now on to the frontend. This provides a web interface. It uses Quixote and
therefore it can run under Apache with CGI, FCGI, mod_python or whatever.
See the Quixote documentation for more info. For small load environments 
and development, we use it under a standalone webserver named Medusa. 
The executable python script 'destar' uses this. Just start it and point 
your web-browser to http://127.0.0.1:8080. For more info, please refer 
to INSTALL.txt.



Webpages, Source Code & Other Resources
----------------------

Project Pages:

* http://destar.berlios.de
* http://developer.berlios.de/projects/destar/


Users mailing list:

* http://lists.berlios.de/mailman/listinfo/destar-user
* destar-user@lists.berlios.de 


Project Wiki:

* http://openfacts.berlios.de/index-en.phtml?title=DeStar


IRC channel:

* #destar at irc.freenode.net


Developers mailing list:

* http://lists.berlios.de/mailman/listinfo/destar-dev
* destar-dev@lists.berlios.de


Web access to Subversion repository:

* http://svn.berlios.de/viewcvs/destar/trunk/


Source code for read-only access:

* svn checkout svn://svn.berlios.de/destar/trunk
