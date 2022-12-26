.PHONY: up
up:
	docker compose up -d

.PHONY: test
test:
	docker compose exec web pytest --disable-warnings