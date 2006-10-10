DIRS=$(patsubst %.po,../lang/%,$(wildcard *.po))
SUBDIRS=$(patsubst %.po,../lang/%/LC_MESSAGES,$(wildcard *.po))
LANGUAGES=$(patsubst %.po,%.mo,$(wildcard *.po))

main:	msgfmt	

msgfmt:	dirs $(LANGUAGES)

dirs:
	install -d ../lang
	install -d $(DIRS)
	install -d $(SUBDIRS)

%.mo:	%.po	dirs
	msgfmt -o $@ $<
	install -m 644 $@ $(patsubst %.mo,../lang/%/LC_MESSAGES/destar.mo,$@)

%.po:	../destar ../*.py ../*.ptl
	xgettext --language=python -j -d $(@:.po=) -kM_ ../destar ../*.py ../*.ptl

clean:
	rm -rf *.mo
	rm -rf ../lang
