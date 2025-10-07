#!/bin/sh
echo -e "\nUpdating pip"
pip install --upgrade pip

echo -e "\nInstalling dependencies."
pip install --no-cache-dir -r requirements.txt