# Imports
from SenseiInputIFClass import SenseiInputIF
from dataclasses import dataclass

BARKER = b'\xFE\xCA'
RX_BARKER = b'\xfe\xca'

@dataclass
class USRP_CONFIG:
    address: int
    value: int
    length: int

def protocol_wrapper(config : USRP_CONFIG):
    return BARKER + config.length.to_bytes(1, byteorder="big")  \
                  + config.address.to_bytes(1, byteorder="big") \
                  + config.value.to_bytes(1, byteorder="big")   \
                  + config.length.to_bytes(1, byteorder="big")  

def calculate_intensity(detection):
    return detection["maxVal"] * (2 ** detection["BlkExp"])

def extract_fields(data):
    if len(data) != 8:
        raise ValueError("Data must be exactly 8 bytes long")

    # Combine the 8 bytes into a single 64-bit integer
    combined_data = int.from_bytes(data, byteorder='big')

    # Extract the fields
    is_detected = (combined_data >> 54) & 0x1
    is_high_band = (combined_data >> 53) & 0x1
    stage1idx = (combined_data >> 49) & 0xF
    stage2idx = (combined_data >> 45) & 0xF
    FFTIdx = (combined_data >> 29) & 0xFFFF
    maxVal = (combined_data >> 21) & 0xFF
    BlkExp = combined_data & 0x1F

    # Validate stage1idx and stage2idx
    if stage1idx > 9 or stage2idx > 9:
        raise ValueError("stage1idx and stage2idx must be between 0 and 9")

    return {
        "is_detected": is_detected,
        "is_high_band": is_high_band,
        "stage1idx": stage1idx,
        "stage2idx": stage2idx,
        "FFTIdx": FFTIdx,
        "maxVal": maxVal,
        "BlkExp": BlkExp
    }

def calculate_band(detection):
    return 420

class Parser:
    def __init__(self, input_if: SenseiInputIF):
        self.input_if = input_if
        self.input_if.setup(protocol_wrapper(USRP_CONFIG(address=3, value=6, length=6)))

    def get_detection(self):
        for packet in self.input_if.read_input():
            detection = extract_fields(packet)
            intensity = calculate_intensity(detection)
            band = calculate_band(detection)
            yield int(band), int(intensity)
