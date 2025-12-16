# Moonlight Monitor

Moonlight Monitor is a lightweight desktop utility designed to monitor and manage Moonlight-related activity on Linux systems. The project is structured to follow standard Linux filesystem conventions and supports installation as a system package.

## Features

* System-wide installation using standard Linux directories
* Desktop launcher integration
* Application icon support
* Simple command-line entry point
* Clean and minimal Python-based implementation

## Project Structure

```
moonlight-monitor/
├── DEBIAN/
│   └── control
├── opt/
│   └── moonlight-monitor/
│       └── moonlight.py
├── usr/
│   ├── bin/
│   │   └── moonlight
│   ├── share/
│   │   ├── applications/
│   │   │   └── moonlight.desktop
│   │   └── icons/
│   │       └── hicolor/
│   │           └── 256x256/
│   │               └── apps/
│   │                   └── logo.png
└── install.sh
```

## Requirements

* Linux-based operating system
* Python 3.9 or newer
* Desktop environment with `.desktop` file support

## Installation

### Using the install script

Clone the repository and run:

```bash
chmod +x install.sh
sudo ./install.sh
```

### Manual installation (advanced)

Copy files to their respective locations:

* Application code: `/opt/moonlight-monitor/`
* Executable: `/usr/bin/moonlight`
* Desktop entry: `/usr/share/applications/moonlight.desktop`
* Icon: `/usr/share/icons/hicolor/256x256/apps/logo.png`

## Usage

After installation, you can launch Moonlight Monitor in two ways:

* From your desktop application menu
* From the terminal:

```bash
moonlight
```

## Development

To contribute or modify the project:

```bash
git clone https://github.com/sedsujim/moonlight-monitor.git
cd moonlight-monitor
```

Make your changes, then commit and push them following standard Git workflows.

## License

This project is licensed under the MIT License.

## Disclaimer

Moonlight Monitor is an independent project and is not officially affiliated with the Moonlight project or its maintainers.
