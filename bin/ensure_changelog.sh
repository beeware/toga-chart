#!/usr/bin/env bash
[[ "$TRACE" ]] && set -x
set -eu -o pipefail

ensure_changelog() {
    git diff @{upstream} --name-only | grep changes/ 1> /dev/null
}

if ensure_changelog; then
   exit 0
else
    echo "Please ensure that a changelog exists along with your PR in changes/"
    exit 3
fi
