PREFIX := /usr

install:
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m755 blugon $(DESTDIR)$(PREFIX)/bin/
	install -d $(DESTDIR)$(PREFIX)/share/blugon/
	install -m644 configs/* $(DESTDIR)$(PREFIX)/share/blugon/
