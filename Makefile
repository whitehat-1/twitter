# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

# Build all services in production
build:
	docker-compose build

# Build all services in production
up:
	docker-compose up

# Delete all services in production
down:
	docker-compose down


# Run all services in development environment
prod-up:
	docker-compose -f docker-compose.prod.yml up

# Kill all services in development environment
prod-down:
	docker-compose -f docker-compose.prod.yml down

# Build all services in development environment
prod-build:
	docker-compose -f docker-compose.prod.yml build
#library for code formatting and linting
black:
	docker-compose run twitter sh -c 'python -m black --line-length 79 .'

flake8:
	docker-compose run twitter sh -c 'flake8'
#reference the aerich github repo (AERICH IS TO TORTOISE ORM)
init-db:
##Success create app migrate location migrations/models
##Success generate schema for app "models"
	docker-compose run twitter sh -c 'aerich init -t library.database.database.TORTOISE_ORM'
	docker-compose run twitter sh -c 'aerich init-db'

db-migrate:
	docker-compose run twitter sh -c 'aerich migrate'


db-upgrade:
	docker-compose run twitter sh -c 'aerich upgrade'

test:
	docker-compose run twitter sh -c 'python -m pytest -v -s -p no:warnings'