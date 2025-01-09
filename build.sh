#!/bin/sh

# Check for `python` command, else check for `python3`, else fail
if command -v python &> /dev/null; then
    pythonglobal=python
elif command -v python3 &> /dev/null; then
    pythonglobal=python3
else
    echo "ERROR: Python not found"
    exit 1
fi

# venv not created
if [ ! -d ./venv ]; then
    $pythonglobal -m venv venv

    if [ ! -d ./venv ]; then
        echo "ERROR: Unable to create python virtualenv"
        exit 1
    fi
fi

if [ -f ./venv/bin/python ]; then
    pyexec=./venv/bin/python
    activateexec=./venv/bin/activate
elif [ -f ./venv/Scripts/python ]; then
    pyexec=./venv/Scripts/python
    activateexec=./venv/Scripts/activate
else
    echo "ERROR: Unable to find python exec in virtualenv"
    exit 1
fi

$pyexec -m pip install .

echo
if [ -f $activateexec ]; then
    echo "Installed. Activate environment with: source $activateexec"
else
    echo "ERROR: Unable to find virtualenv activate script"
    exit 1
fi
