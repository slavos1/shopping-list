HATCH=hatch
PROJECT_NAME=$(shell ${HATCH} project metadata|jq -r '.name')

all: test

test cov help:
	${HATCH} run $@ ${EXTRA}

cli:
	${HATCH} run cli -i shop.db ${EXTRA}

# XXX always run formatter first to wrap long lines
# https://github.com/pypa/hatch/discussions/1205#discussioncomment-8087562
fmt:
	${HATCH} fmt -f
	${HATCH} fmt
	
mypy:
	${HATCH} run types:check

build:
	${HATCH} build

deploy: mypy build reinstall

reinstall:
	-pipx uninstall "${PROJECT_NAME}"
	pipx install dist/*$$(${HATCH} version)*.whl
