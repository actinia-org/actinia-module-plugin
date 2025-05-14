# Tests

## Running tests locally

When writing new tests it is useful to run selected tests locally and isolated. In this way it is also possible to debug interactively:

1. In the `docker/actinia-module-plugin-test/Dockerfile` comment out `RUN ./tests_with_kvdb.sh` (last line)

1. Then run `docker build`:

```bash
docker build -f docker/actinia-module-plugin-test/Dockerfile -t actinia-module-plugin-test:alpine .
```

3. To run only a few tests you can mark the tests for development with
   `@pytest.mark.dev` and add `import pytest` to the `.py` file/s with the tests you want to run.
   (For best practice examples on the use of pytest-decorators, see actinia-core `tests/unittests/test_version.py`)

1. Start the docker container and mount your `tests` folder:

```bash
docker run --rm -it --entrypoint sh -v `pwd`/tests:/src/actinia-module-plugin/tests actinia-module-plugin-test:alpine
# If you are not developing the tests you can run tests using the following command:
docker run --rm -it --entrypoint sh actinia-module-plugin-test:alpine
```

And then start the kvdb and run tests:
```bash
valkey-server &
sleep 1
valkey-cli ping

# run all tests
pytest

# run only dev tests in debugger mode
pytest --pdb -x -m dev
```
