DEST=files
DATE=$(shell date +'%Y%m%d-%H%M')


clean:
	find -name "*.pyc" -o \
	     -name "*.ptlc" -o \
	     -name "*.ptlo" -o \
	     -name "*.au" | xargs rm


tar:
	mkdir -p $(DEST)
	rm -rf destar-$(DATE)
	svn export . destar-$(DATE) 
	tar cjf $(DEST)/destar-$(DATE).tar.bz2 destar-$(DATE)
	rm -rf destar-$(DATE)
