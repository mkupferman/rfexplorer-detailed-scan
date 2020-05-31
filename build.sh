#!/bin/sh

if which python3 >/dev/null; then
    pyexec=python3
elif which python >/dev/null; then
    vers=$(python --version 2>&1)
    if [[ "${vers}" == "Python 3."* ]]; then
        pyexec=python
    else
        echo "Could not find python >= 3 in PATH"
        exit 1
    fi
else
    echo "Could not find python >= 3 in PATH"
fi

$pyexec -m virtualenv venv
[[ -f ./venv/bin/pip ]] \
    && ./venv/bin/pip install --editable . \
    || ./venv/Scripts/pip install --editable .
