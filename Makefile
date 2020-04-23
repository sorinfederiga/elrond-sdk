clean:
	rm -rf ./dist

build: clean
	python3 setup.py sdist

publish: build
	twine upload dist/*

test:
	python3 -m unittest -v erdpy.tests.test_wallet
	python3 -m unittest -v erdpy.tests.test_contracts

test-all:
	python3 -m unittest discover -s erdpy/tests

arwendebug:
	# When referencing a non-released version, add the commit hash, like this: arwen-wasm-vm/cmd/arwendebug@...
	# When referencing a released version, use the actual version instead: arwen-wasm-vm/cmd/arwendebug v0.3.14
	GO111MODULE=on GOPATH=$(shell pwd)/distribution/go go get github.com/ElrondNetwork/arwen-wasm-vm/cmd/arwendebug@b3fc49a7ccfc290ae6532d2c9b764a2458f0276c
	stat ./distribution/go/bin/arwendebug