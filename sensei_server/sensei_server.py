from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, DEVTYPE, ID_MODEL_ID, ID_VENDOR
import os, stat
import shutil
import subprocess
import time

USB_MOUNTING_TIME = 1
SENSEI_APP_DEPLOYMENT_PATH = "/home/sensei/Documents/Sensei_app"
SENSEI_APP_DEPLOYMENT_PATH_WIN = "C:\\Users\\adare\\repos\\Senpi\\Deployed\\Sensei_app"
SENSEI_APP_DEPLOYMENT_PATH = SENSEI_APP_DEPLOYMENT_PATH_WIN
sensei_app_process = None

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
			print(f"killing current running app...")
			sensei_app_process.kill()
		print(f"removing '{installed_path}' ...")
		shutil.rmtree(installed_path)
		print(f"folder '{installed_path} has been removed.")
	except FileNotFoundError:
		print(f"folder '{installed_path} does not exist.")
	except Exception as e:
		print(f"an error occured: {e}")

def run_app_win(app_path = SENSEI_APP_DEPLOYMENT_PATH):
	command = f"python {app_path}\\src\\main.py"
	print(f"Running Sensei app: {command}")
	sensei_app_process = subprocess.run(["powershell", "-Command", command], shell=True, capture_output=True, text=True)


def run_app(app_path = SENSEI_APP_DEPLOYMENT_PATH):
	command = f"{app_path}/app_venv/bin/python {app_path}/src/main.py"
	print(f"Running Sensei app: {command}")
	sensei_app_process = subprocess.run(command, shell = True, executable="/bin/bash")

def make_install_script_exe(dest):
	os.chmod(f"{dest}/install_app.sh", stat.S_IRWXU)

def install_sensei_app_win(source, dest = SENSEI_APP_DEPLOYMENT_PATH):
	shutil.copytree(source, dest)

def install_sensei_app(source, dest = SENSEI_APP_DEPLOYMENT_PATH):
	shutil.copytree(source, dest)
	make_install_script_exe(dest)
	command = f"{dest}/install_app.sh {dest}"
	print(f"Running install script: {command}")
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
		return
	
	print("Waiting for device mounting...")
	time.sleep(USB_MOUNTING_TIME)
	drop_path = find_drop_win("sensei")
	if drop_path == None:
		print("sensei app was not found")
		return

	uninstall_sensei()	

	install_sensei_app_win(drop_path)

	run_app_win()

def on_disconnect(device_id, device_info):
	print(f"Disconnected: {device_info_str(device_info)}")


if __name__ == "__main__":
	# Create the USBMonitor instance
	monitor = USBMonitor()

	# Get the current devices
	devices_dict = monitor.get_available_devices()
	for device_id, device_info in devices_dict.items():
		on_connect(device_id=device_id, device_info=device_info)
	
	if sensei_app_process != None:
		run_app()
	
	while True:
		pass

# sensei_app_process = subprocess.run([f"{SENSEI_APP_DEPLOYMENT_PATH}/venv/bin/python",f"{SENSEI_APP_DEPLOYMENT_PATH}/src/main.py"])
# monitor = USBMonitor()
# monitor.start_monitoring(on_connect=on_connect, on_disconnect=on_disconnect)

# try:
# 	while True:
# 		pass
# except KeyboardInterrupt:
# 	monitor.start_monitoring()


