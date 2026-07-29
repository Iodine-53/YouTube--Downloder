#!/data/data/com.termux/files/usr/bin/bash
set -e

echo "=== Updating system packages ==="
pkg update -y && pkg upgrade -y

echo "=== Installing required system packages ==="
pkg install -y python ffmpeg clang make python-dev

echo "=== Creating virtual environment ==="
python -m venv .venv

echo "=== Activating virtual environment ==="
source .venv/bin/activate

echo "=== Upgrading pip ==="
pip install --upgrade pip

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Launching Streamlit app ==="
streamlit run app.py
