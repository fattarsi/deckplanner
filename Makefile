#!make

PWD = $(shell pwd)

build:
	docker compose build

run:
	docker compose up

clean:
	docker compose rm -f
	rm -f app/deckplanner/migrations/0*.py

deploy:
	docker build -f docker/Dockerfile -t registry.fattarsi.com/deckplanner/backend:latest .
	docker push registry.fattarsi.com/deckplanner/backend:latest
