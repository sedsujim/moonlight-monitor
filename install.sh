#!/usr/bin/env bash

set -e

APP_NAME="moonlight-monitor"
APP_BIN="moonlight"
APP_DIR="/opt/${APP_NAME}"
BIN_DIR="/usr/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/256x256/apps"

if [[ "$EUID" -ne 0 ]]; then
  echo "This installer must be run as root." >&2
  exit 1
fi

echo "Installing ${APP_NAME}..."

# Create application directory
mkdir -p "${APP_DIR}"

# Install application files
cp -f opt/${APP_NAME}/moonlight.py "${APP_DIR}/moonlight.py"
chmod +x "${APP_DIR}/moonlight.py"

# Install launcher binary
cp -f usr/bin/${APP_BIN} "${BIN_DIR}/${APP_BIN}"
chmod +x "${BIN_DIR}/${APP_BIN}"

# Install desktop entry
mkdir -p "${DESKTOP_DIR}"
cp -f usr/share/applications/${APP_BIN}.desktop "${DESKTOP_DIR}/${APP_BIN}.desktop"

# Install icon
mkdir -p "${ICON_DIR}"
cp -f usr/share/icons/hicolor/256x256/apps/logo.png "${ICON_DIR}/logo.png"

# Update desktop database if available
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "${DESKTOP_DIR}" || true
fi

# Update icon cache if available
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f /usr/share/icons/hicolor || true
fi

echo "${APP_NAME} installed successfully."
echo "You can launch it from the application menu or by running '${APP_BIN}' in a terminal."
