#!/bin/bash
echo y | pip uninstall marslogistic
BASEDIR=$(dirname "$0")
echo $BASEDIR
pip install $BASEDIR
clear
echo Done updating marslogistic
