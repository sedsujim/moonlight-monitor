#!/bin/bash
# install.sh - Instala Moonlight como aplicación

echo "🌙 Instalando Moonlight Monitor..."
echo "=================================="

# Verificar si estamos en la carpeta correcta
if [ ! -f "moonlight.py" ]; then
    echo "❌ Error: No encuentro moonlight.py"
    echo "Ejecuta este script desde la carpeta de Moonlight"
    exit 1
fi

# Obtener ruta absoluta
SCRIPT_PATH="$(pwd)/moonlight.py"
echo "📁 Ruta del script: $SCRIPT_PATH"

# Instalar dependencias
echo "📦 Instalando dependencias..."
sudo pacman -S --noconfirm python python-psutil python-tk

# Para GPU NVIDIA (opcional)
read -p "¿Tienes GPU NVIDIA? [s/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🎮 Instalando soporte para NVIDIA..."
    sudo pacman -S --noconfirm nvidia-utils
fi

# Dar permisos
chmod +x "$SCRIPT_PATH"

# Crear directorio para .desktop
mkdir -p ~/.local/share/applications

# Crear archivo .desktop CON LA RUTA CORRECTA
DESKTOP_FILE="$HOME/.local/share/applications/moonlight.desktop"
echo "📋 Creando acceso directo en: $DESKTOP_FILE"

cat > "$DESKTOP_FILE" << EOF
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

# Hacer el .desktop ejecutable
chmod +x "$DESKTOP_FILE"

echo ""
echo "✅ ¡INSTALACIÓN COMPLETADA!"
echo ""
echo "🎮 Para usar Moonlight:"
echo "   1. Busca 'Moonlight' en tu menú de aplicaciones"
echo "   2. Haz doble clic para abrir"
echo "   3. Usa ESC para cerrar"
echo ""
echo "📊 Moonlight monitorea:"
echo "   - CPU, RAM, GPU, Temperatura"
echo "   - Disco y Red"
echo "   - Procesos activos"
echo "   - Consumo propio de la app"
echo ""
echo "✨ ¡Listo para jugar con monitoreo completo!"