# Imports
from SenseiInputIFClass import SenseiInputIF
from dataclasses import dataclass
import logging
logger = logging.getLogger(__name__)

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



class Parser:
    def __init__(self, input_if: SenseiInputIF, log_level = logging.DEBUG):
        self.input_if = input_if
        self.input_if.setup(protocol_wrapper(USRP_CONFIG(address=3, value=6, length=6)))
        logger.setLevel(level=log_level)

    def close(self):
        logger.info("Closing Parser...")
        self.input_if.close()

    def get_band(self):
        for packet in self.input_if.read_input():
            band = extract_fields(packet)
            yield band
