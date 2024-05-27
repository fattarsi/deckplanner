#!make

PWD = $(shell pwd)

build:
	docker compose build

run:
	docker compose up

clean:
	docker compose rm -f
	rm app/deckplanner/migrations/*