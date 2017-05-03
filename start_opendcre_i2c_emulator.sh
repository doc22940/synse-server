#!/bin/bash

# first, determine if we are in debug mode, in which case we prop debug log config over prod log config
if [[ $VAPOR_DEBUG && ${VAPOR_DEBUG} = "true" ]]
then
    mv -f /opendcre/configs/logging_bootstrap_debug.json /opendcre/logging_bootstrap.json
    mv -f /opendcre/configs/logging_opendcre_debug.json /opendcre/logging_opendcre.json
    mv -f /opendcre/configs/logging_emulator_debug.json /opendcre/logging_emulator.json
fi

# before we start up the flask endpoint, we want to bootstrap the container
#python ./opendcre_southbound/bootstrap/bootstrap.py 2>&1

# this is to disable double-bootstrapping through start_opendcre.sh
export NO_BOOTSTRAP=true


cp ./configs/opendcre_config_i2c_emulator.json ./default/default.json

# test flag to let us bypass the default prop-in of rs485 config for bind-mount from test yml
if [ ! $VAPOR_TEST ]
    then
        cp ./configs/i2c_emulator_config.json ./i2c_config.json
fi

socat PTY,link=/dev/ttyVapor005,mode=666 PTY,link=/dev/ttyVapor006,mode=666 &
if [ $# -eq 1 ]
    then
        python -u ./opendcre_southbound/emulator/i2c/i2c_emulator.py $1 &

    else
        python -u ./opendcre_southbound/emulator/i2c/i2c_emulator.py ./opendcre_southbound/emulator/i2c/data/example.json &
fi
./start_opendcre.sh