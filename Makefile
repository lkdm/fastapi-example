.PHONY: run, build

run:
	uv run fastapi dev

up:
	docker build -t fastapi-app .

build:
	docker build -t fastapi-app .
