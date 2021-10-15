DOCKER_REGISTRY?=quay.io
DOCKER_PROJECT?=jdzon
DOCKER_TAG?=v1

# Setting SHELL to bash allows bash commands to be executed by recipes.
# This is a requirement for 'setup-envtest.sh' in the test target.
# Options are set to exit when a recipe line exits non-zero or a piped command fails.
SHELL = /usr/bin/env bash -o pipefail


.PHONY: build-dependencies
build-dependencies:
	sudo dnf install podman buildah qemu-user-static -y

build-%: build-dependencies
	buildah build --jobs=2 --platform=linux/amd64,linux/arm64 --manifest ${DOCKER_REGISTRY}/$(DOCKER_PROJECT)/$*:$(DOCKER_TAG) poc-demo/edge/$*

.PHONY: build-edge
build-edge: build-random-server build-os-stats

push-%:	build-%*
	podman manifest push --all $(DOCKER_REGISTRY)/$(DOCKER_PROJECT)/$*:$(DOCKER_TAG) docker://$(DOCKER_REGISTRY)/$(DOCKER_PROJECT)/random$*:$(DOCKER_TAG)

.PHONY: push-edge
push-edge: push-random-server push-os-stats