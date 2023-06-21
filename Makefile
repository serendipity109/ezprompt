VERSION := $(shell git rev-parse --short HEAD)
UPDATED_DATE := $(shell git log -1 --format=%cd --date=format:%Y%m%d)
UPDATED_TIME := $(shell git log -1 --format=%cd --date=format:%H%M)

TAG = IMAGE_TAG=$(VERSION)-$(UPDATED_DATE)-$(UPDATED_TIME)

DOCKER = docker-compose

.PHONY: build push pull down run

build:
	$(TAG) $(DOCKER) build

push:
	$(TAG) $(DOCKER) push

pull:
	$(TAG) $(DOCKER) pull

down:
	$(TAG) $(DOCKER) down --remove-orphans

run:
	$(TAG) BUILD_VERSION=internal $(DOCKER) up --force-recreate -d

run_external:
	$(TAG) BUILD_VERSION=external $(DOCKER) up --force-recreate -d
