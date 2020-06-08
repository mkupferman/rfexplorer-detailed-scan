all: build

build:
	bash build.sh

clean:
	rm -rf ./*.egg-info ./__pycache__/ ./*/__pycache__/ ./venv/
