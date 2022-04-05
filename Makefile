name?=backend

build: # Build image [name]
	docker-compose build $(name)

test: # Run tests in tests folder
	coverage run -m pytest tests
	coverage report -m --skip-covered --ignore-errors
