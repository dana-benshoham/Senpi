# Server
## Install
chmod +x scripts/install_service.sh
sudo scripts/install_service.sh
the script installs the "sensei.service" systemd service in the system
## Logs
"Real Time" Logs 
sudo journalctl -u sensei.service -f
## Workflow
Listen to usb changes with USBMonitor pip package.
Once a usb device has been connected, the server checks if it has a folder with a substring sensei in it.
if so, it checks for a a version number, if it is higher than the current installed app, it uninstalls the current app and installs the new version.

# App
## Install
the server uses the install_app.sh to install the app.
## Drop
To create a new app drop to be installed run the script:
create_drop.sh
it uses the version.json to install a new version.

# Raspberry Pi Setup
## Install USRP Dependecies
1. Enter https://pysdr.org/content/usrp.html and follow instructions.
* it requires internet connection for apt-get installations and git clone

