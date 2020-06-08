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
    exit 1
fi

# try to set up virtualenv
$pyexec -m virtualenv venv

# venv not created
if [ ! -d ./venv ]; then
    $pyexec -m pip install --user virtualenv
    $pyexec -m virtualenv venv

    if [ ! -d ./venv ]; then
        echo "ERROR: Unable to create python virtualenv"
        exit 1
    fi
fi

if [ -f ./venv/bin/pip ]; then
    pipexec=./venv/bin/pip
    activateexec=./venv/bin/activate
elif [ -f ./venv/Scripts/pip ]; then
    pipexec=./venv/Scripts/pip
    activateexec=./venv/Scripts/activate
else
    echo "ERROR: Unable to find python pip in virtualenv"
    exit 1
fi

$pipexec install --editable .

echo
if [ -f $activateexec ]; then
    echo "Installed. Activate environment with: source $activateexec"
else
    echo "ERROR: Unable to find virtualenv activate script"
    exit 1
fi
