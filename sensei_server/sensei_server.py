from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, DEVTYPE, ID_MODEL_ID, ID_VENDOR
import os, stat
import shutil
import subprocess
import time

SENSEI_APP_DEPLOYMENT_PATH = "/home/sensei/Documents/Sensei_app"
sensei_app_process = None

def device_info_str(device_info):
	return f" \
		{device_info[ID_MODEL]} - \
		{device_info[DEVTYPE]} - \
		{device_info[ID_VENDOR]})"

def is_usb_device_connected(device_info):
	return device_info[DEVTYPE] == 'usb_device'

def uninstall_sensei(installed_path):
	try:
		if sensei_app_process != None:
			print(f"killing current running app...")
			sensei_app_process.kill()
		print(f"removing '{installed_path}' ...")
		shutil.rmtree(installed_path)
		print(f"folder '{installed_path} has been removed.")
	except FileNotFoundError:
		print(f"folder '{installed_path} does not exist.")
	except Exception as e:
		print(f"an error occured: {e}")

def make_install_script_exe(dest):
	os.chmod(f"{dest}/install.sh", stat.S_IRWXU)

def install_sensei(source, dest):
	shutil.copytree(source, dest)
	make_install_script_exe(dest)
	command = f"{dest}/install.sh {dest}"
	print(f"Running install script: {command}")
	subprocess.run(command, shell = True, executable="/bin/bash")

def find_drop():
	MEDIA_PATH = "/media/sensei"
	substring = "sensei"
	command = f"find {MEDIA_PATH} -type d -iname '*{substring}*'"	
	result  = subprocess.run(command, shell=True, capture_output=True, text=True)
	output = result.stdout.strip().split('\n')
	app_folder = output[1] if len(output) > 1 else None
	return app_folder 

def on_connect(device_id, device_info):
	if not is_usb_device_connected(device_info):
		return
	
	print("Waiting for device mounting...")
	time.sleep(5)
	drop_path = find_drop()
	print(drop_path)
	if drop_path == None:
		print("sensei app was not found")
		return

	uninstall_sensei(SENSEI_APP_DEPLOYMENT_PATH)	

	install_sensei(drop_path, SENSEI_APP_DEPLOYMENT_PATH)

	sensei_app_process = subprocess.run([f"{SENSEI_APP_DEPLOYMENT_PATH}/venv/bin/python",f"{SENSEI_APP_DEPLOYMENT_PATH}/src/main.py"])


def on_disconnect(device_id, device_info):
	print(f"Disconnected: {device_info_str(device_info)}")

# sensei_app_process = subprocess.run([f"{SENSEI_APP_DEPLOYMENT_PATH}/venv/bin/python",f"{SENSEI_APP_DEPLOYMENT_PATH}/src/main.py"])
monitor = USBMonitor()
monitor.start_monitoring(on_connect=on_connect, on_disconnect=on_disconnect)

try:
	while True:
		pass
except KeyboardInterrupt:
	monitor.start_monitoring()
