all: push

.PHONY: build
build:
	docker build -t cbarraco/google-assistant-over-rest:latest .

.PHONY: push
push:
	docker buildx create --node mybuilder
	docker buildx use mybuilder
	docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t cbarraco/google-assistant-over-rest:latest --push .
	docker buildx rm mybuilder
