# actinia-module-plugin

You can run actinia-module-plugin as actinia-core plugin.

## Installation
For installation or DEV setup, see docker/README.md.

## actinia-core process-chain templating
see actinia-module.md

## DEV notes

### Build

__insprired by [this](https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/)__

to create a shippable wheel, run
```bash
pip3 install --upgrade pip pep517
python3 -m pep517.build .
```

#### Versioning

[(MAJOR.MINOR.PATCH)](https://semver.org/)

#### Logging
in any module, import `from actinia_module_plugin.resources.logging import log` and call logger with `log.info("my info i want to log")`


### Running tests
You can run the tests in the actinia-modules-plugin-test docker. For that you can comment the execution of the test in the docker/actinia-modules-plugin-test/Dockerfile `RUN ./tests_with_kvdb.sh` and run the following commands:
```bash
docker build -f docker/actinia-module-plugin-test/Dockerfile -t actinia-module-plugin-test .

# run docker (here the tests folder can also be mounted for development of further tests)
docker run -it actinia-module-plugin-test -i

cd /src/actinia-module-plugin/

# run all tests
./tests_with_kvdb.sh
```
