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
            self.measure()
            log.log_msg(logger.INFO, "Initiation done")
        except Exception as e:
            log.log_msg(logger.ERROR, "Could not initiate sensor: {}".format(e))

    def measure(self):
        self._dht.measure()
        return self._dht.temperature(), self._dht.humidity()
