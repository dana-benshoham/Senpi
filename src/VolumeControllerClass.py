# Imports
import subprocess
import re
import time


def get_current_volume():
    """Get the current volume level."""
    result = subprocess.run(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'], capture_output=True, text=True)
    # Example output: "Volume: 50% / 50% / -10.00dB"
    match = re.search(r'(\d+)%', result.stdout)
    if match:
        return int(match.group(1))
    return None


def list_devices():
    """List all input devices using xinput."""
    result = subprocess.run(['xinput', '--list'], capture_output=True, text=True)
    return result.stdout


def get_device_id(device_name):
    """Get the device ID for a given device name."""
    devices = list_devices()
    pattern = re.compile(r'{}.*id=(\d+)'.format(re.escape(device_name)))
    for line in devices.splitlines():
        if device_name in line:
            match = pattern.search(line)
            if match:
                return int(match.group(1))
    return None


def set_volume(volume):
    """Set the volume level."""
    subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{volume}%'])


class VolumeController:
    def __init__(self, device_name):
        self.device_name = device_name
        self.device_id = get_device_id(device_name)
        self.current_volume = get_current_volume()

    def control_volume(self, action):
        """Control system volume based on the action."""
        if action == 'mute':
            subprocess.run(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', 'toggle'])
        elif action == 'volume_up':
            if self.current_volume is not None:
                new_volume = min(self.current_volume + 5, 100)  # Ensure volume does not exceed 100%
                set_volume(new_volume)
        elif action == 'volume_down':
            if self.current_volume is not None:
                new_volume = max(self.current_volume - 5, 0)  # Ensure volume does not go below 0%
                set_volume(new_volume)
        else:
            print(f"Unknown action: {action}")

    def monitor_device(self):
        """Monitor events from the specified device."""
        if not self.device_id:
            print(f"Device '{self.device_name}' not found.")
            return

        try:
            proc = subprocess.Popen(
                ['xinput', 'test', str(self.device_id)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            while True:
                output = proc.stdout.readline()
                if output:
                    if 'KEY_VOLUMEUP' in output:
                        print("Volume Up Pressed")
                        self.current_volume = get_current_volume()  # Update current volume
                        if self.current_volume is not None:
                            self.control_volume('volume_up')
                    elif 'KEY_VOLUMEDOWN' in output:
                        print("Volume Down Pressed")
                        self.current_volume = get_current_volume()  # Update current volume
                        if self.current_volume is not None:
                            self.control_volume('volume_down')
                    elif 'KEY_MUTE' in output:
                        print("Mute Pressed")
                        self.control_volume('mute')
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Monitoring stopped.")
        finally:
            proc.terminate()
