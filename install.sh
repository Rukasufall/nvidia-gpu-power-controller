#!/bin/bash
# Installation script for NVIDIA GPU Power Controller

echo "======================================"
echo "  NVIDIA GPU Power Controller"
echo "  Installation Script"
echo "======================================"
echo ""

# Check for nvidia-smi
if ! command -v nvidia-smi &> /dev/null; then
    echo "ERROR: nvidia-smi not found!"
    echo "Please install NVIDIA drivers first."
    exit 1
fi

echo "✓ nvidia-smi found"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found!"
    exit 1
fi

echo "✓ Python 3 found"

# Check for Tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo ""
    echo "ERROR: Tkinter not installed!"
    echo ""
    echo "Install it with:"
    echo "  Ubuntu/Debian: sudo apt install python3-tk"
    echo "  Fedora: sudo dnf install python3-tkinter"
    echo "  Arch: sudo pacman -S tk"
    echo ""
    exit 1
fi

echo "✓ Tkinter installed"
echo ""

# Installation directory
INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"

# Copy script
echo "Installing application..."
cp nvidia_gpu_power_controller.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/nvidia_gpu_power_controller.py"

echo "✓ Application installed to $INSTALL_DIR"

# Create desktop shortcut
read -p "Create desktop menu shortcut? [Y/n]: " create_shortcut

if [[ $create_shortcut != "n" && $create_shortcut != "N" ]]; then
    cat > "$DESKTOP_DIR/gpu-power-control.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=GPU Power Controller
Comment=NVIDIA GPU Power Management
Exec=$INSTALL_DIR/nvidia_gpu_power_controller.py
Icon=nvidia-settings
Terminal=false
Categories=System;Settings;
Keywords=nvidia;gpu;power;
EOF
    
    chmod +x "$DESKTOP_DIR/gpu-power-control.desktop"
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR"
    fi
    
    echo "✓ Desktop shortcut created"
fi

echo ""
echo "======================================"
echo "  Installation Complete!"
echo "======================================"
echo ""
echo "Run the application:"
echo "  nvidia_gpu_power_controller.py"
echo ""
echo "Or search for 'GPU Power Controller' in your application menu."
echo ""
