PREFIX := /usr

install:
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m755 blugon $(DESTDIR)$(PREFIX)/bin/
	install -d $(DESTDIR)$(PREFIX)/share/blugon/configs/default/
	install -m644 configs/default/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/default/
	install -d $(DESTDIR)$(PREFIX)/share/blugon/configs/extreme/
	install -m644 configs/extreme/gamma $(DESTDIR)$(PREFIX)/share/blugon/configs/extreme/
