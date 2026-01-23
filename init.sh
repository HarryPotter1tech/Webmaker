#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status
echo "initializing python environment..."
cd /backend
python -m venv web_env
source web_env/bin/activate

echo "python environment initialized."

pip install --upgrade pip
pip install -r requirements.txt
echo "dependencies installed."

echo "initializing backend server..."

uvicorn server:app --host 0.0.0.0 --port 8000 --reload