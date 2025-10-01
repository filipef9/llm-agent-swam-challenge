#!/bin/sh

echo -e "\nRemoving existent virtual environment."
rm -Rf .venv

echo -e "\nCreating new virtual environment."
python3 -m venv .venv &&\

echo -e "\nActivating virtual environment." &&\
source .venv/bin/activate &&\

echo -e "\nInstalling dependencies." &&\
pip install --no-cache-dir -r requirements.txt

