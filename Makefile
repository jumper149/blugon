PREFIX := /usr

install:
	install -Dm755 blugon $(PREFIX)/bin/
	install -Dm644 configs/ $(PREFIX)/share/blugon/
