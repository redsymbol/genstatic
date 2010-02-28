#!/bin/bash
GSROOT=$(dirname $(realpath $0))/..
export PYTHONPATH=$GSROOT/lib:$HOME/src/Django-1.2
$GSROOT/bin/genstatic $*