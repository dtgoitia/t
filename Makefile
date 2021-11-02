VERSION:=$(shell cat VERSION)
IMAGE_TAG:=$(shell cat IMAGE_NAME):$(VERSION)

clean_logs:
	rm -rf logs

clean:
	python -m src.clean_all_parquet_files

requirements:
	rm -f requirements.txt
	pip-compile requirements.in \
		--output-file requirements.txt \
		--no-header \
		--no-emit-index-url \
		--verbose

dev-requirements:
	rm -f dev-requirements.txt
	pip-compile requirements.in dev-requirements.in \
		--output-file dev-requirements.txt \
		--no-header \
		--no-emit-index-url \
		--verbose

install:
	pip install -r requirements.txt
	./scripts/patch-togglpy.py

install-container: build
	./scripts/install-container-wrapper.py

uninstall-container: delete-all-images
	./scripts/uninstall-container-wrapper.py

dev-install:
	pip install -r dev-requirements.txt
	./scripts/patch-togglpy.py

lint:
	flake8
	black --check --diff .
	isort --check --diff .
	python -m mypy --config-file setup.cfg --pretty .

format:
	isort .
	black .

test:
	pytest tests -vv

build:
	podman build \
		--file=./Containerfile \
		--tag $(IMAGE_TAG) \
		.

delete-current-image:
	podman rmi $(IMAGE_TAG) -f

delete-all-images:
	images_to_delete=$(shell python ./scripts/find-podman-images.py); \
	podman rmi $$images_to_delete -f

rebuild: delete-current-image build

run:
	podman run \
		--interactive --tty \
		--rm \
		--mount type=bind,source=$(HOME)/.config/t,target=/config \
		$(IMAGE_TAG)
