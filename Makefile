ifndef UID
	UID = $(shell id -u)
endif
export UID

ifndef GID
	GID = $(shell id -g)
endif
export GID

start:
	docker-compose -f docker-compose.dev.yml run --rm python



