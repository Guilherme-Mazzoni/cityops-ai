.PHONY: setup start stop

setup:
	@echo "Setting up CityOps AI environment..."

start:
	docker-compose up -d

stop:
	docker-compose down
