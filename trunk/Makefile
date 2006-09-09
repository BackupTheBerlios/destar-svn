DATE=$(shell date +'%Y%m%d-%H%M')
DESTDIR=
PYDIR=$(DESTDIR)/usr/share/destar/python
PAGES_DIR=$(DESTDIR)/usr/share/destar/static
SBINDIR=$(DESTDIR)/usr/sbin
LOCALEDIR=$(DESTDIR)/usr/share/locale
MANDIR=$(DESTDIR)/usr/share/man/man8

# To use with asternic.org op_panel tarball:
#PANEL_HTML_DIR=/usr/local/op_panel/html

# To use with op-panel .deb package:
PANEL_HTML_DIR=/usr/share/op-panel/flash

# set SYS_MEDUSA to 1 to use system copy of medusa
SYS_MEDUSA=0

clean:
	(find -name "*.pyc" ; \
	 find -name "*.ptlc" ; \
	 find -name "*.ptlo" ; \
	 find -name "*.au" ; \
	 find -name "*.mo" ) | xargs rm -f || true

clean-languages:
	cd po && $(MAKE) clean

clean-panel:
	rm -f $(PAGES_DIR)/panel

release:
	svn export svn+ssh://svn.berlios.de/svnroot/repos/destar/trunk destar-0.2.0
	tar cjf destar-0.2.tar.bz2 destar-0.2.0
	tar czf destar-0.2.tar.gz destar-0.2.0
	#scp destar-$(DATE).tar.bz2 shell.berlios.de:/home/groups/ftp/pub/destar/
	#rm -rf destar-$(DATE) destar-$(DATE).tar.bz2


install-panel:
	ln -s $(PANEL_HTML_DIR) $(PAGES_DIR)/panel

languages:
	cd po && $(MAKE)

install:
	install -d $(PYDIR)
	#cp -a *.py *.ptl misc medusa $(PYDIR)
	install -m 644 *.py *.ptl $(PYDIR)/
	install -m 755 Server.py $(PYDIR)/
	install -m 755 tests.py $(PYDIR)/
	install -m 755 docs.py $(PYDIR)/
	install -d $(LOCALEDIR)
	cp -fRp lang/* $(LOCALEDIR)
	install -d $(PYDIR)/misc
	install -m 644 misc/*.py $(PYDIR)/misc/
ifneq ($(SYS_MEDUSA),1)
	install -d $(PYDIR)/medusa
	install -m 644 medusa/*.py $(PYDIR)/medusa/
	install -m 755 medusa/http_server.py $(PYDIR)/medusa/
endif
	install -m 755 destar $(PYDIR)/destar.py
	install -d $(PAGES_DIR)
	cp -fRp static/* $(PAGES_DIR)
	install -d $(SBINDIR)
	install -m 755 misc/destar.sh $(SBINDIR)/destar
	install -d $(MANDIR)
	gzip -9 <misc/destar.8 >$(MANDIR)/destar.8.gz
	chmod 0644 $(MANDIR)/destar.8.gz

test:
	./tests.py

