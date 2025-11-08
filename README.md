# NVIDIA GPU Power Controller

GPU power management tool with automatic detection and real-time monitoring.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

## Features

- **Automatic GPU Detection**: Automatically detects your NVIDIA GPU and its power limits
- **Real-time Monitoring**: Live display of temperature, power draw, and GPU utilization
- **Dynamic Power Control**: Adjust power limits with a precise slider control
- **Industrial UI Design**: Clean, professional interface inspired by monitoring software
- **Universal Compatibility**: Works with any NVIDIA GPU that supports power limit adjustment
- **Safe Operation**: Confirms changes before applying and preserves system stability

## Screenshot

```
┌─────────────────────────────────────┐
│  RTX 5060                           │
│  Temp: 45°C  |  Power: 98W  | 34%  │
├─────────────────────────────────────┤
│                                      │
│  POWER LIMIT CONTROL                │
│  135W (93%)                         │
│  [━━━━━━━●━━━]                      │
│  Min: 123W ────────────── Max: 145W │
│                                      │
│  [APPLY]  [RESET]  [HELP]           │
└─────────────────────────────────────┘
```

## Requirements

- Python 3.6 or higher
- NVIDIA GPU with proprietary drivers installed
- nvidia-smi command-line tool
- Tkinter (Python GUI library)
- pkexec or sudo (for applying power limits)

## Installation

### Install Dependencies

**Ubuntu/Debian/Pop!_OS:**
```bash
sudo apt update
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

### Download and Run

```bash
# Clone the repository
git clone https://github.com/yourusername/nvidia-gpu-power-controller.git
cd nvidia-gpu-power-controller

# Make executable
chmod +x nvidia_gpu_power_controller.py

# Run the application
python3 nvidia_gpu_power_controller.py
```

## Usage

### Basic Operation

1. Launch the application
2. The tool will automatically detect your GPU and its power limits
3. Use the slider to select desired power limit
4. Click **APPLY** to set the new limit (requires root privileges)
5. Click **RESET** to restore default power limit
6. Click **HELP** for detailed information

### Creating Desktop Shortcut

Create a file `~/.local/share/applications/gpu-power-control.desktop`:

```desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=GPU Power Controller
Comment=NVIDIA GPU Power Management
Exec=/path/to/nvidia_gpu_power_controller.py
Icon=nvidia-settings
Terminal=false
Categories=System;Settings;
```

Update the desktop database:
```bash
update-desktop-database ~/.local/share/applications/
```

## How It Works

The application uses the nvidia-smi utility to interface with your NVIDIA GPU:

**Reading GPU Information:**
```bash
nvidia-smi --query-gpu=name,temperature.gpu,power.draw,utilization.gpu --format=csv
nvidia-smi -q  # For detailed power limit information
```

**Setting Power Limits:**
```bash
sudo nvidia-smi -pl <watts>
```

The tool automatically parses the output to determine:
- GPU model name
- Minimum power limit
- Maximum power limit  
- Default power limit
- Current power limit

## Technical Details

### Power Limit Detection

The application parses the output of `nvidia-smi -q` to extract:
- **Min Power Limit**: Lowest allowable power limit for your GPU
- **Max Power Limit**: Highest allowable power limit for your GPU
- **Default Power Limit**: Factory default setting
- **Current Power Limit**: Currently active power limit

### Real-time Monitoring

A background thread polls GPU statistics every 2 seconds to update:
- Temperature (Celsius)
- Power draw (Watts)
- GPU utilization (Percentage)

### Power Limit Persistence

**Important**: Power limit changes do not persist after system reboot. The GPU will reset to its default power limit when the system restarts.

To apply power limits automatically at boot, create a systemd service:

```bash
sudo nano /etc/systemd/system/gpu-power-limit.service
```

Add the following content:
```ini
[Unit]
Description=NVIDIA GPU Power Limit
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/bin/nvidia-smi -pl 123
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable gpu-power-limit.service
sudo systemctl start gpu-power-limit.service
```

## Uninstall

To completely remove the application:

```bash
# Remove the script
rm nvidia_gpu_power_controller.py

# Remove desktop shortcut
rm ~/.local/share/applications/gpu-power-control.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/
```

## Troubleshooting

### Application Does Not Start

**Check Tkinter installation:**
```bash
python3 -c "import tkinter"
```

If this fails, install python3-tk (see Installation section).

### Cannot Apply Power Limit

**Verify nvidia-smi works:**
```bash
nvidia-smi
```

**Check if pkexec is installed:**
```bash
which pkexec
```

If pkexec is not available, apply manually:
```bash
sudo nvidia-smi -pl <watts>
```

### Permission Denied

The application requires root privileges to set power limits. It uses pkexec for graphical authentication.

**Alternative**: Configure passwordless sudo for nvidia-smi:
```bash
sudo visudo
```

Add this line (replace USERNAME):
```
USERNAME ALL=(ALL) NOPASSWD: /usr/bin/nvidia-smi
```

**Warning**: This allows running nvidia-smi without password. Use with caution.

## Safety Notes

- Reducing power limits decreases performance and heat output
- Setting too low power limits may cause instability under load
- The tool only adjusts power limits within manufacturer-approved ranges
- All changes are reversible and non-permanent

## Compatibility

Tested on:
- Ubuntu 22.04 / 24.04
- Pop!_OS 22.04
- Fedora 38+
- Arch Linux

GPUs tested:
- RTX 40-series (Ada Lovelace)
- RTX 50-series (Blackwell)
- Should work with any NVIDIA GPU supporting power limit adjustment

## Contributing

Contributions are welcome. Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with a clear description

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments

- Built with Python and Tkinter
- Uses NVIDIA's nvidia-smi utility
- Inspired by MSI Afterburner and similar GPU monitoring tools

## Disclaimer

This software is provided as-is without warranty. Use at your own risk. The authors are not responsible for any damage to hardware or data loss resulting from use of this software.
