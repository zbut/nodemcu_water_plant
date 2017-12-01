import logger
import machine
import micropython
import config
micropython.alloc_emergency_exception_buf(100)


class Logic(object):

    PERIOD_ID = 0
    PERIOD_MIN = 1

    def __init__(self):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Starting logic")
        import adc
        self._adc = adc.ADC(adc.ADC_MODE_VCC)
        import temp_humidity_sensor
        self._temp_humid_sensor = temp_humidity_sensor.TempHumiditySensor()
        import thingspeak
        self._thingspeak_comm = thingspeak.ThingspeakComm()
        import wifi
        ip = wifi.connect()
        if ip:
            self._thingspeak_comm.send_data({"status": "Connected with ip {}".format(ip)})

    def periodic_start(self):
        tim = machine.Timer(Logic.PERIOD_ID)
        tim.init(period=Logic.PERIOD_MIN * 60 * 1000, mode=machine.Timer.PERIODIC, callback=self.periodic_action)

    def measure_and_send_temp_humid(self, dict_of_fields):
        temp, humid = self._temp_humid_sensor.measure()
        # Send it if valid
        if temp and humid:
            dict_of_fields.update({config.get_thingspeak_field("temperature"): temp, config.get_thingspeak_field("humidity"): humid})

    def measure_and_send_vcc(self, dict_of_fields):
        vcc = self._adc.read_vcc()
        # Send if valid
        if vcc:
            dict_of_fields.update({config.get_thingspeak_field("vcc"): vcc})

    def periodic_action(self, timer):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Starting periodic action")
        dict_of_fields = {}
        self.measure_and_send_temp_humid(dict_of_fields)
        self.measure_and_send_vcc(dict_of_fields)
        self._thingspeak_comm.send_data(dict_of_fields)

def run_it():
    logic = Logic()
    logic.periodic_start()


if __name__ == "__main__":
    run_it()