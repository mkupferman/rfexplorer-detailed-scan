all: build

clean:
	rm -rf ./dist/ ./build/ ./*.egg-info ./__pycache__/ ./*/__pycache__/ ./venv/

venv:
	python3 -m venv venv

validate:
	source venv/bin/activate; \
	python3 -m pip install --upgrade '.[validate]'

build: clean venv validate
	source venv/bin/activate; \
	python3 -m pip install --upgrade pip; \
	python3 -m pip install --upgrade build; \
	python3 -m build; \
	mypy . --strict --exclude=build/ --exclude=venv/

develop: venv validate
	source venv/bin/activate; \
	python3 -m pip install --upgrade pip; \
	python3 -m pip install --editable '.[dev]'

install:
	python3 -m pip install .
