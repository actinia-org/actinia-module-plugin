#!/usr/bin/env sh

# start redis server
redis-server &
sleep 1
redis-cli ping

# # start webhook server
# webhook-server --host "0.0.0.0" --port "5005" &
# sleep 10

# run tests
echo $ACTINIA_CUSTOM_TEST_CFG
echo $DEFAULT_CONFIG_PATH

if [ "$1" = "dev" ]
then
  echo "Executing only 'dev' tests ..."
  pytest -m 'dev'
else
  pytest
fi

TEST_RES=$?

# stop redis server
redis-cli shutdown

return $TEST_RES
