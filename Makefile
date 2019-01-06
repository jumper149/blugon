PREFIX := /usr

install:
	install -Dm755 blugon $(DESTDIR)/$(PREFIX)/bin/
	install -Dm644 configs/ $(DESTDIR)/$(PREFIX)/share/blugon/
