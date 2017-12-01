import dht
import machine
import logger


class TempHumiditySensor(object):
    DATA_PIN = 4  # D2 on board

    def __init__(self):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Initiating Temperature and Humidity sensor")
        try:
            self._dht = dht.DHT22(machine.Pin(TempHumiditySensor.DATA_PIN))
            # Try to measure
            self._dht.measure()
            log.log_msg(logger.INFO, "Initiation done")
        except Exception as e:
            log.log_msg(logger.ERROR, "Could not initiate sensor: {}".format(e))

    def measure(self):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Measuring temp and humid")
        temp = -1
        humid = -1
        try:
            self._dht.measure()
            temp = self._dht.temperature()
            humid = self._dht.humidity()
            log.log_msg(logger.INFO, "Measured temperature {} and humidity {}".format(temp, humid))
        except Exception as e:
            log.log_msg("Could not measure: {}".format(e))
        finally:
            return temp, humid
