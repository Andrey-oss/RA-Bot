
# Bot Installation Guide

This bot uses several dependencies that need to be installed. This guide provides instructions for installing the required dependencies on various Linux distributions

## Dependencies

- pytelegrambotapi
- speedtest-cli
- requests
- playsound
- psutil
- opencv-python
- pillow

In addition, `alsa-utils` is required for audio functionality

## Installation Instructions

### Debian-based (Ubuntu, etc.)
To install the required dependencies, run the following commands:

```bash
sudo apt update
sudo apt install -y python3-pip alsa-utils
pip3 install pytelegrambotapi speedtest-cli requests playsound psutil opencv-python pillow
```

### Arch-based (Manjaro, etc.)
For Arch Linux and its derivatives, use `pacman` to install system packages, and `pip` for Python dependencies:

```bash
sudo pacman -Syu
sudo pacman -S python-pip alsa-utils
pip install pytelegrambotapi speedtest-cli requests playsound psutil opencv-python pillow
```

### openSUSE
On openSUSE, install the necessary packages using `zypper`:

```bash
sudo zypper refresh
sudo zypper install python3-pip alsa-utils
pip3 install pytelegrambotapi speedtest-cli requests playsound psutil opencv-python pillow
```

### Fedora
For Fedora-based systems, use `dnf` to install system packages:

```bash
sudo dnf check-update
sudo dnf install python3-pip alsa-utils
pip3 install pytelegrambotapi speedtest-cli requests playsound psutil opencv-python pillow
```

### Gentoo-based
On Gentoo systems, first ensure that you have `pip` and the necessary system packages:

```bash
sudo emerge --sync
sudo emerge dev-python/pip media-sound/alsa-utils
pip3 install pytelegrambotapi speedtest-cli requests playsound psutil opencv-python pillow
```

If everything is installed successfully, you are ready to run the bot!

## Troubleshooting

- **Pip version issues**: Ensure you're using the correct version of pip. If there are any issues, you can upgrade pip:

  ```bash
  python3 -m pip install --upgrade pip
  ```

- **Alsa-utils**: Make sure `alsa-utils` is correctly installed for audio functionality, as `playsound` depends on it

## License

This project is licensed under the GPL 2 License. See the [LICENSE](LICENSE) file for more details