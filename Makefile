#!make

PWD = $(shell pwd)

build:
	docker compose build

run:
	docker compose up