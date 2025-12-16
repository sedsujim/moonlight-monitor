#!/usr/bin/env bash

set -e

APP_NAME="moonlight-monitor"
BIN_NAME="moonlight"
INSTALL_DIR="/opt/moonlight-monitor"
BIN_DIR="/usr/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/256x256/apps"

echo "🌙 Installing Moonlight Monitor..."

if [[ $EUID -ne 0 ]]; then
    echo "Please run as root (sudo ./install.sh)"
    exit 1
fi

echo "→ Checking dependencies..."

if ! command -v python3 >/dev/null; then
    echo "Python3 is required"
    exit 1
fi

if ! python3 -c "import PySide6" >/dev/null 2>&1; then
    echo "PySide6 is not installed"
    echo "Arch: sudo pacman -S pyside6"
    echo "Debian/Ubuntu: sudo apt install python3-pyside6"
    exit 1
fi

if ! python3 -c "import psutil" >/dev/null 2>&1; then
    echo "psutil is not installed"
    echo "Arch: sudo pacman -S python-psutil"
    echo "Debian/Ubuntu: sudo apt install python3-psutil"
    exit 1
fi

echo "→ Installing files..."

mkdir -p "$INSTALL_DIR"
cp moonlight.py "$INSTALL_DIR/"

cat > "$BIN_DIR/$BIN_NAME" << EOF
#!/usr/bin/env bash
python3 $INSTALL_DIR/moonlight.py
EOF

chmod +x "$BIN_DIR/$BIN_NAME"

if [[ -f moonlight.desktop ]]; then
    cp moonlight.desktop "$DESKTOP_DIR/"
fi

if [[ -f icon.png ]]; then
    mkdir -p "$ICON_DIR"
    cp icon.png "$ICON_DIR/moonlight.png"
fi

echo "→ Updating desktop database..."
if command -v update-desktop-database >/dev/null; then
    update-desktop-database "$DESKTOP_DIR" || true
fi

echo
echo "✅ Moonlight Monitor installed successfully"
echo
echo "• Run from terminal: moonlight"
echo "• Or search 'Moonlight Monitor' in your app launcher"
echo
echo "🌙 Enjoy."
