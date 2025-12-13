#!/bin/bash
# make_desktop.sh - Crea el archivo .desktop automáticamente

echo "🖥️  Creando acceso directo de Moonlight..."

# Obtener ruta actual
CURRENT_DIR=$(pwd)
SCRIPT_PATH="$CURRENT_DIR/moonlight.py"

# Verificar que existe
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: No encuentro moonlight.py"
    exit 1
fi

# Crear el archivo .desktop
cat > moonlight.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Moonlight Monitor
Comment=Monitor de sistema ligero para gaming
Exec=python3 "$SCRIPT_PATH"
Icon=utilities-system-monitor
Terminal=false
Categories=Utility;System;
Keywords=monitor;system;gaming
StartupNotify=false
EOF

# Dar permisos
chmod +x moonlight.desktop

echo "✅ Archivo .desktop creado:"
echo "   📍 Ubicación: $CURRENT_DIR/moonlight.desktop"
echo ""
echo "📋 Para instalarlo en tu menú:"
echo "   cp moonlight.desktop ~/.local/share/applications/"
echo ""
echo "🖱️  O simplemente haz doble clic en moonlight.desktop"