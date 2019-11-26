#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo $DIR
cd $DIR

source $DIR/venv/bin/activate
source $DIR/.ENV


./bot.py --noauth_local_webserver
