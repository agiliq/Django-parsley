all: init test

init:
	pip install tox coverage

test:
	coverage erase
	tox
	coverage html

fast_test:
	coverage run setup.py test
	coverage report
	coverage html
