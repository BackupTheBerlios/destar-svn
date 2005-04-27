DATE=$(shell date +'%Y%m%d-%H%M')
DESTDIR=
PYDIR=$(DESTDIR)/usr/share/destar/python
PAGES_DIR=$(DESTDIR)/usr/share/destar/static
SBINDIR=$(DESTDIR)/usr/sbin
MANDIR=$(DESTDIR)/usr/share/man/man8


clean:
	find -name "*.pyc" -o \
	     -name "*.ptlc" -o \
	     -name "*.ptlo" -o \
	     -name "*.au" | xargs rm -f || true


release:
	svn export . destar-$(DATE) 
	tar cjf destar-$(DATE).tar.bz2 destar-$(DATE)
	scp destar-$(DATE).tar.bz2 holgerschurig@shell.berlios.de:/home/groups/ftp/pub/destar/
	rm -rf destar-$(DATE) destar-$(DATE).tar.bz2

gettext:
	pygettext.py -d destar *.py *.ptl

msgfmt:
	msgfmt.py destar.po


install:
	install -d $(PYDIR)
	cp -a *.py *.ptl misc medusa $(PYDIR)
	install -m 755 destar $(PYDIR)/destar.py
	install -d $(PAGES_DIR)
	cp -a static/* $(PAGES_DIR)
	install -d $(SBINDIR)
	install -m 755 misc/destar.sh $(SBINDIR)/destar
	install -d $(MANDIR)
	gzip -9 <misc/destar.8 >$(MANDIR)/destar.8.gz
	chmod 0644 $(MANDIR)/destar.8.gz
