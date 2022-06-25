#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
echo "Executing iziQR_bot in '$BASEDIR'"
PORT=$1

source $BASEDIR/venv/bin/activate
export TELEGRAM_TOKEN=5571098152:AAEzy_jBA72QYhsZpThRR-pnDRNuS4rkUW4
export CHAT_ID=988347219

python $BASEDIR/iziQR_bot.py $PORT
