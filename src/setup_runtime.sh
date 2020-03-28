#!/usr/bin/env bash

pythonEnv="pyenv"
requirements="requirements.txt"

if [ ! -d "${pythonEnv}" ]
then
    echo "Create python virtual environment!"
    virtualenv "${pythonEnv}"
    curl https://bootstrap.pypa.io/get-pip.py | "${pythonEnv}/bin/python"
fi

if [ -f "${requirements}" ]
then
    "${pythonEnv}/bin/pip" install -r "${requirements}"
fi
