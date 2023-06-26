#!/bin/bash

pytest tests --cov=tizero --cov-report=xml -m unittest --cov-report=term-missing --durations=0 -v --color=yes
