LANG_DIRS = $(patsubst %.po,../lang/%,$(wildcard *.po))
LANG_SUBD = $(patsubst %.po,../lang/%/LC_MESSAGES,$(wildcard *.po))
MO_FILES  = $(patsubst %.po,%.mo,$(wildcard *.po))

main:	createdirs $(MO_FILES)

createdirs:
	install -d ../lang
	install -d $(LANG_DIRS)
	install -d $(LANG_SUBD)

%.mo:	%.po createdirs
	msgfmt -o $@ $<
	install -m 644 $@ $(patsubst %.mo,../lang/%/LC_MESSAGES/destar.mo,$@)

%.po:	pot destar.pot	
	msgmerge -U $@ destar.pot 

pot:	../destar ../*.py ../*.ptl
	xgettext --language=python -o destar.pot -kM_ ../destar ../*.py ../*.ptl
	
.PHONY: clean

clean:
	rm -rf *.mo
	rm -rf ../lang
