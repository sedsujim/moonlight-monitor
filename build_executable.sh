#!/bin/bash
# build_executable.sh - Crea un ejecutable de Moonlight

echo "🔨 Construyendo ejecutable de Moonlight..."
echo "==========================================="

# Verificar que estamos en la carpeta correcta
if [ ! -f "moonlight.py" ]; then
    echo "❌ Error: No encuentro moonlight.py"
    echo "Ejecuta este script desde la carpeta de Moonlight"
    exit 1
fi

# Instalar dependencias necesarias
echo "📦 Instalando dependencias..."
sudo pacman -S --noconfirm python-pip python-venv tk

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar PyInstaller y dependencias
echo "📦 Instalando PyInstaller..."
pip install pyinstaller psutil

# Crear el ejecutable
echo "🔨 Compilando ejecutable..."
pyinstaller --onefile \
            --windowed \
            --name "Moonlight" \
            --add-data "moonlight.desktop:." \
            --icon=utilities-system-monitor \
            moonlight.py

# Verificar que se creó
if [ -f "dist/Moonlight" ]; then
    echo ""
    echo "✅ ¡ÉXITO! Ejecutable creado:"
    echo "   📁 dist/Moonlight"
    echo ""
    echo "📋 Para instalar en tu sistema:"
    echo "   sudo cp dist/Moonlight /usr/local/bin/moonlight"
    echo "   sudo cp moonlight.desktop /usr/share/applications/"
    echo ""
    echo "🎮 Para ejecutar: simplemente haz doble clic en 'Moonlight'"
else
    echo "❌ Error al crear el ejecutable"
    exit 1
fi

# Limpiar
deactivate
echo "✨ Proceso completado"