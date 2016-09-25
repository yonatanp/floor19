#!/usr/bin/env bash
cd `dirname $0`

DATAHACK_PARAMS=$HOME/params DATAHACK_MAXPERSEED=30 DATAHACK_NUMWORDS=400 python app.py
