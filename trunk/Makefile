DATE=$(shell date +'%Y%m%d-%H%M')


clean:
	find -name "*.pyc" -o \
	     -name "*.ptlc" -o \
	     -name "*.ptlo" -o \
	     -name "*.au" | xargs rm


release:
	svn export . destar-$(DATE) 
	tar cjf destar-$(DATE).tar.bz2 destar-$(DATE)
	scp destar-$(DATE).tar.bz2 holgerschurig@shell.berlios.de:/home/groups/ftp/pub/destar/
	rm -rf destar-$(DATE) destar-$(DATE).tar.bz2

gettext:
	pygettext.py -d destar *.py *.ptl

msgfmt:
	msgfmt.py destar.po
