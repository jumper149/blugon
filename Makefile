PREFIX := /usr

build:
	gzip --keep blugon.1

install:
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m755 blugon.py $(DESTDIR)$(PREFIX)/bin/blugon
	install -d $(DESTDIR)$(PREFIX)/share/blugon/configs/default/
	install -m644 configs/default/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/default/
	install -d $(DESTDIR)$(PREFIX)/share/blugon/configs/extreme/
	install -m644 configs/extreme/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/extreme/
	install -d $(DESTDIR)$(PREFIX)/share/man/man8/
	install -m644 blugon.1.gz $(DESTDIR)$(PREFIX)/share/man/man1/
