.PHONY: check-ver

all: init test

init:
	pip install tox coverage

clean:
	pyclean .
	rm -rf __pycache__ .tox dist django_parsley.egg-info

test:
	coverage erase
	tox
	coverage html

fast_test:
	coverage run setup.py test
	coverage report
	coverage html

release: check-ver
	@echo ${VER}
	sed -i "s/^VERSION = .*/VERSION = '${VER}'/g" setup.py
	git add setup.py
	git commit -m "version bump"
	git tag v${VER}
	git push --tags
	python setup.py sdist upload

check-ver:
ifndef VER
	$(error VER is undefined)
endif
