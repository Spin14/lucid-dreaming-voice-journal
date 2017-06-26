.PHONY: test-client test-server test

test-client:
	cd client; env/bin/pytest; cd ..
	
test-server:
	cd server; env/bin/pytest; cd ..

test:
	make test-server
	make test-client
