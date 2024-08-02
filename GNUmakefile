default: sanity

TEST_MODULE ?= "sonarr_tag"

# Run sanity test
.PHONY: sanity
sanity:
	ansible-test sanity --exclude .github/

# Run integration test
.PHONY: integration
integration:
	ansible-test integration ${TEST_MODULE} -vvv

# Generate doc
.PHONY: doc
doc:
	antsibull-docs sphinx-init --use-current --dest-dir dest devopsarr.sonarr
	cd dest && ./build.sh