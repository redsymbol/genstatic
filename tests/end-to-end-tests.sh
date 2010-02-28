#!/bin/bash

GENSTATIC=../bin/genstatic.sh
OUT=$(mktemp -d)
echo "Test output dir: $OUT"

count=0
failed=0

function runtests() {
    item=$1
    $GENSTATIC ./data/$item $OUT/$item
    diff -Naur $OUT/$item ./data/${item}_out
    ec=$?
    if [ $ec != 0 ]; then
	failed=$(( $failed + 1 ))
    fi
    count=$(( $count+1 ))
}
# e1
runtests e1

echo "Tests run: $count"
echo "Tests failed: $failed"

if [ $failed != 0 ]; then
    echo "FAIL"
    exit 1
fi
echo "Ok"
exit 0