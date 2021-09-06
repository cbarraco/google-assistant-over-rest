all: docker-build-and-push-multiarch

.PHONY: docker-build-and-push-multiarch
	docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t cbarraco/google-assistant-over-rest:latest --push .
