#!/bin/bash

set -e

flake8 envconfig/ --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 envconfig/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
