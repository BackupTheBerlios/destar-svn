#!/bin/sh

SOURCE=manual
LANG=en
OUTPUT=../../build-area/$(LANG)
DSLPDF=/usr/share/sgml/docbook/stylesheet/dsssl/ldp/ldp.dsl
DSLHTML=../destar.dsl\#html
#DSLPDF=../destar.dsl\#pdf
DB_IMAGES=/usr/share/sgml/docbook/stylesheet/dsssl/modular/images
all: html rtf pdf ps clean

#TODO: automate spell checking
#spell: 
#	echo "Cheking spell..."
#	aspell -l en -c introduction.xml

html: $(SOURCE).xml
	echo "Generating HTML OUTPUT..."
	mkdir -p $(OUTPUT)/html
	db2html $(SOURCE).xml -o $(OUTPUT)/html --dsl $(DSLHTML)
	db2html -u $(SOURCE).xml -o $(OUTPUT)/html --dsl $(DSLHTML)
	rm -rf $(SOURCE).junk $(OUTPUT)/html/images
	mkdir -p $(OUTPUT)/html/images
	mkdir -p $(OUTPUT)/images
	cp -rp images/*.png $(OUTPUT)/html/images 
	cp -rp $(DB_IMAGES)/*.gif $(OUTPUT)/images 
	cp ../html.css $(OUTPUT)/html/
	rm -rf $(SOURCE)

rtf: $(SOURCE).xml
	echo "Generating RTF OUTPUT..."
	mkdir -p $(OUTPUT)/rtf
	db2rtf $(SOURCE).xml -o $(OUTPUT)/rtf
	rm -rf $(SOURCE).junk 

pdf: $(SOURCE).xml
	echo "Generating PDF OUTPUT..."
	mkdir -p $(OUTPUT)/pdf
	#docbook2pdf $(SOURCE).xml -d $(DSLPDF) -o $(OUTPUT)/pdf
	docbook2pdf $(SOURCE).xml -o $(OUTPUT)/pdf
	rm -rf $(SOURCE).junk 

ps: $(SOURCE).xml
	echo "Generating PS OUTPUT..."
	mkdir -p $(OUTPUT)/ps
	#docbook2pdf $(SOURCE).xml -d $(DSLPDF) -o $(OUTPUT)/ps
	docbook2pdf $(SOURCE).xml -o $(OUTPUT)/ps
	rm -rf $(SOURCE).junk 
	
clean:
	rm -rf $(OUTPUT)
	rm -rf $(SOURCE) $(SOURCE).junk
	rm -f *~

release: html
	scp -r $(OUTPUT)/html/ shell.berlios.de:/home/groups/destar/htdocs/manual/

