import logger
import machine
import temp_humidity_sensor
import micropython
import thingspeak
micropython.alloc_emergency_exception_buf(100)


class Logic(object):

    PERIOD_ID = 0
    PERIOD_MIN = 1

    def __init__(self):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Starting logic")
        self._temp_humid_sensor = temp_humidity_sensor.TempHumiditySensor()
        self._thingspeak_comm = thingspeak.ThingspeakComm()

    def periodic_start(self):
        tim = machine.Timer(Logic.PERIOD_ID)
        tim.init(period=Logic.PERIOD_MIN * 60 * 1000, mode=machine.Timer.PERIODIC, callback=self.periodic_action)

    def periodic_action(self, timer):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Starting periodic action")
        temp = 0
        humid = 0
        try:
            temp, humid = self._temp_humid_sensor.measure()
            log.log_msg(logger.INFO, "Measured temperature {} and humidity {}".format(temp, humid))
        except Exception as e:
            log.log_msg(logger.ERROR, "Periodic action failed: {}".format(e))
        # Send it if valid
        if temp and humid:
            dict_of_fields = {"field1": temp, "field2": humid}
            self._thingspeak_comm.send_data(dict_of_fields)


def run_it():
    logic = Logic()
    logic.periodic_start()


if __name__ == "__main__":
    run_it()