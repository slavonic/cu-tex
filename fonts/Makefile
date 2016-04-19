ZIP1 = PonomarUnicode-1.2.zip
ZIP1_SRC = PonomarUnicode-specific-info.tex

ZIP2 = monomachus-1.0-prerelease.otf.zip

ZIP3 = PomorskyUnicode-0.75.zip
ZIP3_SRC = PomorskyUnicode.tex

ZIP4 = FedorovskUnicode-3.0.zip
ZIP4_SRC = FedorovskUnicode-specific-info.tex

ZIP5 = MenaionUnicode-2.0.zip
ZIP5_SRC = MenaionUnicode-specific-info.tex

ALL_SRC = $(ZIP1) $(ZIP1_SRC) \
	$(ZIP2) \
	$(ZIP3) $(ZIP3_SRC) \
	$(ZIP4) $(ZIP4_SRC) \
	$(ZIP5) $(ZIP5_SRC) \
	

all: fonts-churchslavonic.zip

fonts-churchslavonic.zip: $(ALL_SRC)
	rm -f $@
	./zip_copy.py README.ctan $@:README
	./zip_copy.py ../LICENSE $@:
	./zip_copy.py $(ZIP1): $@:ponomar/
	./zip_copy.py $(ZIP1_SRC) $@:ponomar/
	./zip_copy.py $(ZIP2): $@:monomachus/
	./zip_copy.py $(ZIP3): $@:pomorsky/
	./zip_copy.py $(ZIP3_SRC) $@:pomorsky/
	./zip_copy.py $(ZIP4): $@:fedorovsk/
	./zip_copy.py $(ZIP4_SRC) $@:fedorovsk/
	./zip_copy.py $(ZIP5): $@:menaion/
	./zip_copy.py $(ZIP5_SRC) $@:menaion/

$(ZIP1):
	wget http://www.ponomar.net/files/$@

$(ZIP1_SRC):
	wget https://raw.githubusercontent.com/typiconman/fonts-cu/master/Ponomar/$@ 

$(ZIP2):
	wget https://github.com/akryukov/monomachus/releases/download/v1.0-prerelease/$@

$(ZIP3):
	wget http://www.ponomar.net/files/$@

$(ZIP3_SRC):
	wget https://raw.githubusercontent.com/typiconman/fonts-cu/master/Pomorsky/$@ 

$(ZIP4):
	wget http://www.ponomar.net/files/$@

$(ZIP4_SRC):
	wget https://raw.githubusercontent.com/typiconman/fonts-cu/master/Fedorovsk/$@ 

$(ZIP5):
	wget http://www.ponomar.net/files/$@

$(ZIP5_SRC):
	wget https://raw.githubusercontent.com/typiconman/fonts-cu/master/Menaion/$@ 

clean:
	rm -f $(ALL_SRC)
	rm -f fonts-churchslavonic.zip
