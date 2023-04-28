VERSION := $(shell git rev-parse --short HEAD)
UPDATED_DATE := $(shell git log -1 --format=%cd --date=format:%Y%m%d)
UPDATED_TIME := $(shell git log -1 --format=%cd --date=format:%H%M)

DOCKER = IMAGE_TAG=$(VERSION)-$(UPDATED_DATE)-$(UPDATED_TIME) docker-compose

.PHONY: build push pull down run

build:
	$(DOCKER) build

push:
	$(DOCKER) push

pull:
	$(DOCKER) pull

down:
	$(DOCKER) down --remove-orphans

run:
	$(DOCKER) up --force-recreate -d
