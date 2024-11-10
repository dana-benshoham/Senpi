from ParserClass import Parser
import logging
logger = logging.getLogger(__name__)

def calculate_intensity(detection):
    return detection["maxVal"] * (2 ** detection["BlkExp"])

def calculate_band(detection):
    return 420

class Detector:
    def __init__(self, parser: Parser, log_level = logging.DEBUG):
        self.parser = parser
        logger.setLevel(level=log_level)
    
    def get_detection(self):
        for band in self.parser.get_band():
            intensity = int(calculate_intensity(band))
            band = int(calculate_band(band))
            logger.info(f"Detection ! Intensity:{intensity} Band={band}")
            yield band, intensity
