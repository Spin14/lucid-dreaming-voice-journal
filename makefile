.PHONY: test-client test-server test

test-client:
	cd client; client-venv/bin/pytest; cd ..
	
test-server:
	cd server; server-venv/bin/pytest; cd ..

test:
	make test-server
	make test-client
