from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, DEVTYPE, ID_MODEL_ID, ID_VENDOR
import os, stat
import shutil
import subprocess
import time
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import logging
import logging.handlers

# Configure the root logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.handlers.TimedRotatingFileHandler('server.log', when='midnight', interval=1, backupCount=7),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger("Server")

USB_MOUNTING_TIME = 1
SENSEI_APP_DEPLOYMENT_PATH = "/home/sensei/Documents/Sensei_app"
sensei_app_process = None

def copy_log_file(source_dir, destination_dir, filename="app.log"):
    # Construct the full file paths
    source_file = os.path.join(source_dir, filename)
    destination_file = os.path.join(destination_dir, filename)
    
    # Copy the file
    try:
        shutil.copy(source_file, destination_file)
        logger.info(f"Copied {filename} from {source_dir} to {destination_dir}")
    except FileNotFoundError:
        logger.error(f"File {filename} not found in {source_dir}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def device_info_str(device_info):
	return f" \
		{device_info[ID_MODEL]} - \
		{device_info[DEVTYPE]} - \
		{device_info[ID_VENDOR]})"

def is_usb_device_connected(device_info): 
	return device_info[DEVTYPE] == 'usb_device' or \
		   device_info[DEVTYPE] == 'USBSTOR'

def uninstall_sensei(installed_path = SENSEI_APP_DEPLOYMENT_PATH):
	try:
		if sensei_app_process != None:
			logger.debug(f"killing current running app...")
			sensei_app_process.kill()
		logger.debug(f"removing '{installed_path}' ...")
		shutil.rmtree(installed_path)
		logger.info(f"folder '{installed_path} has been removed.")
	except FileNotFoundError:
		logger.error(f"folder '{installed_path} does not exist.")
	except Exception as e:
		logger.error(f"an error occured: {e}")

def run_app_win(app_path = SENSEI_APP_DEPLOYMENT_PATH):
	# command = f'start powershell -NoExit -Command "python {app_path}\\src\\main.py"'
	command = f'C:\\Users\\adare\\repos\\Senpi\\venv\\Scripts\\python.exe {app_path}\\src\\main.py'
	logger.info(f"Running Sensei app: {command}")
	# Run the command and capture the output
	sensei_app_process = subprocess.Popen(command)
	process = sensei_app_process


def run_app(app_path = SENSEI_APP_DEPLOYMENT_PATH):
	command = f"{app_path}/app_venv/bin/python {app_path}/src/main.py"
	logger.info(f"Running Sensei app: {command}")
	sensei_app_process = subprocess.run(command, shell = True, executable="/bin/bash")

def make_install_script_exe(dest):
	os.chmod(f"{dest}/install_app.sh", stat.S_IRWXU)

def install_sensei_app_win(source, dest = SENSEI_APP_DEPLOYMENT_PATH):
	shutil.copytree(source, dest, dirs_exist_ok=True)

def install_sensei_app(source, dest = SENSEI_APP_DEPLOYMENT_PATH):
	shutil.copytree(source, dest)
	logger.info("Drop copied to local memory")
	make_install_script_exe(dest)
	command = f"{dest}/install_app.sh {dest}"
	logger.debug(f"Running install script: {command}")
	subprocess.run(command, shell = True, executable="/bin/bash")

def find_drop_win(drop_name):
	MEDIA_PATH = "D:\\"
	substring = drop_name
	command = f"Get-ChildItem -Path {MEDIA_PATH} -Directory -Filter '*{substring}*' | Select-Object -ExpandProperty Name"
	result = subprocess.run(["powershell", "-Command", command], shell=True, capture_output=True, text=True)
	output = result.stdout.strip().split('\r\n')
	return f"{MEDIA_PATH}{output[0]}" if len(output) > 0 else None 

def find_drop(drop_name):
	MEDIA_PATH = "/media/sensei"
	substring = drop_name
	command = f"find {MEDIA_PATH} -type d -iname '*{substring}*'"	
	result  = subprocess.run(command, shell=True, capture_output=True, text=True)
	output = result.stdout.strip().split('\n')
	app_folder = output[1] if len(output) > 1 else None
	return app_folder 

def on_connect(device_id, device_info):
	if not is_usb_device_connected(device_info):
		logger.debug("Not a USB Storage Device, Skipping...")
		return False
	
	logger.debug("Waiting for device mounting...")
	time.sleep(USB_MOUNTING_TIME)

	copy_log_file(SENSEI_APP_DEPLOYMENT_PATH_WIN, "D:\\", "app.log"),
	copy_log_file(SENSEI_APP_DEPLOYMENT_PATH_WIN, "D:\\", "server.log"),

	drop_path = find_drop_win("sensei")
	if drop_path == None:
		logger.error("app was not found")
		return False

	logger.info("app was found, version: -")
	uninstall_sensei()	

	install_sensei_app_win(drop_path)

	run_app_win()

	return True

def on_disconnect(device_id, device_info):
	logger.info(f"Disconnected: {device_info_str(device_info)}")


if __name__ == "__main__":
	logger.info("Server Started")
	# Create the USBMonitor instance
	monitor = USBMonitor()

	logger.info("Enumerating USB Devices")
	# Get the current devices
	devices_dict = monitor.get_available_devices()
	for device_id, device_info in devices_dict.items():
		logger.debug(f"Found device with id: {device_id} and info: {device_info}")
		logger.debug(f"Searching Drop")
		result = on_connect(device_id=device_id, device_info=device_info)
		if result==True:
			break
	
	if sensei_app_process == None:
		run_app_win()
	
	while True:
		pass



