DATE=$(shell date +'%Y%m%d-%H%M')
DESTDIR=
PYDIR=$(DESTDIR)/usr/share/destar/python
PAGES_DIR=$(DESTDIR)/usr/share/destar/static
SBINDIR=$(DESTDIR)/usr/sbin
MANDIR=$(DESTDIR)/usr/share/man/man8

# set SYS_MEDUSA to 1 to use system copy of medusa
SYS_MEDUSA=0

clean:
	find -name "*.pyc" -o \
	     -name "*.ptlc" -o \
	     -name "*.ptlo" -o \
	     -name "*.au" | xargs rm -f || true


release:
	svn export svn+ssh://svn.berlios.de/svnroot/repos/destar/trunk destar-$(DATE) 
	tar cjf destar-$(DATE).tar.bz2 destar-$(DATE)
	scp destar-$(DATE).tar.bz2 shell.berlios.de:/home/groups/ftp/pub/destar/
	rm -rf destar-$(DATE) destar-$(DATE).tar.bz2

gettext:
	pygettext.py -d destar *.py *.ptl

msgfmt:
	msgfmt.py destar.po


install:
	install -d $(PYDIR)
	#cp -a *.py *.ptl misc medusa $(PYDIR)
	install -m 644 *.py *.ptl $(PYDIR)/
	install -d $(PYDIR)/misc
	install -m 644 misc/*.py $(PYDIR)/misc/
ifneq ($(SYS_MEDUSA),1)
	install -d $(PYDIR)/medusa
	install medusa/*.py $(PYDIR)/medusa/
endif
	install -m 755 destar $(PYDIR)/destar.py
	install -d $(PAGES_DIR)
	cp -a static/* $(PAGES_DIR)
	install -d $(SBINDIR)
	install -m 755 misc/destar.sh $(SBINDIR)/destar
	install -d $(MANDIR)
	gzip -9 <misc/destar.8 >$(MANDIR)/destar.8.gz
	chmod 0644 $(MANDIR)/destar.8.gz
