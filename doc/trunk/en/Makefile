#!/bin/sh

SOURCE=manual
LANG=en
OUTPUT=../../build-area/$(LANG)
DSLPDF=/usr/share/sgml/docbook/stylesheet/dsssl/ldp/ldp.dsl
#DSLHTML=../destar.dsl\#html
#DSLPDF=../destar.dsl\#pdf

all: html rtf pdf ps clean

html: $(SOURCE).xml
	echo "Generating HTML OUTPUT..."
	mkdir -p $(OUTPUT)/html
	#db2html $(SOURCE).xml -o $(OUTPUT)/html --dsl $(DSLHTML)
	db2html $(SOURCE).xml -o $(OUTPUT)/html
	rm -rf $(SOURCE).junk $(OUTPUT)/html/images
	mkdir -p $(OUTPUT)/html/images
	cp -rp images/*.png $(OUTPUT)/html/imagenes 
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