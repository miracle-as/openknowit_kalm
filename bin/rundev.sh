#!/usr/bin/env bash

git pull
git checkout staging
pip install .

kalm service


