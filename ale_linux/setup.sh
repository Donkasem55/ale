#!/usr/bin/sh
set -euo pipefail # abort if there is an issue with installation

cd "$(dirname "$0")"

BIN_NAME="ale"
BIN_DEST="/usr/local/bin/${BIN_NAME}"

# Logging functions for simplicity
log() { echo "[setup] $*"; }
abort_install() { echo "[setup] \033[31m ERROR: $* \033[37m" >&2; exit 1; }

# Check if required tools are present
command -v python3 >/dev/null 2>&1 || abort_install "python3 not found"
command -v pip >/dev/null 2>&1 || abort_install "pip not found"
[ -f ./"$BIN_NAME" ] || abort_install "expected binary '${BIN_NAME}' not found at ${BIN_SRC}"

# Once confirmed that pip is present, install the neccesary packages
log "Installing Python dependencies..."
pip install --break-system-packages psutil termcolor readchar

log "Please enter your root password in order to install the binary to ${BIN_DEST}"
sudo cp "./$BIN_NAME" "$BIN_DEST"
sudo chmod +x "$BIN_DEST"

log "Setup complete. Use command '${BIN_NAME}' to execute the program!"
