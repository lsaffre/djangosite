tests:
	cd tests ; make tests
  
html:
	cd docs; make html
  
sdist:
	python setup.py sdist --formats=gztar,zip --dist-dir=docs/dl 
	#~ python setup.py register sdist --formats=gztar,zip upload 
	#~ python setup.py sdist --formats=gztar,zip --dist-dir=docs/dist
  
upload:
	python setup.py sdist --formats=gztar,zip --dist-dir=docs/dl upload 
