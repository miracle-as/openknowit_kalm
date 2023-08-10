#!/usr/bin/env bash

rm -fr venv/ >/dev/null 2>&1

python3 -m venv venv
source venv/bin/activate

poetry install

