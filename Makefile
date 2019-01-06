PREFIX := /usr

install:
	mkdir -p $(DESTDIR)$(PREFIX)/bin/
	install -Dm755 blugon $(DESTDIR)$(PREFIX)/bin/
	mkdir -p $(DESTDIR)$(PREFIX)/share/blugon/
	install -Dm644 configs/ $(DESTDIR)$(PREFIX)/share/blugon/
