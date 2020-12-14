all: docker-push

.PHONY: docker-build
docker-build:
	docker build -t cbarraco/google-assistant-over-rest:latest .

.PHONY: docker-push
docker-push: docker-build
	docker push cbarraco/google-assistant-over-rest:latest