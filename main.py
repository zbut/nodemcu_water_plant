import machine
import time
import os
import micropython
import logger
import temp_humidity_sensor
micropython.alloc_emergency_exception_buf(100)

# Timer IDS
MOISTURE_MEASURE_TIMER = 1
TEMP_HUMID_MEASURE_TIMER = 2
WATER_PUMP_START_TIMER = 3
WATER_PUMP_STOP_TIMER = 4

# class MoistureMeasurer(Periodical):
#     ADC_PIN = 0
#     MEASURE_POWER_PIN = 0  # D3 on board
#
#     def __init__(self, logger, period_id, period_min):
#         super().__init__(logger, period_id, period_min)
#         self._adc = machine.ADC(MoistureMeasurer.ADC_PIN)
#         self._power_pin = machine.Pin(MoistureMeasurer.MEASURE_POWER_PIN, machine.Pin.OUT)
#         self._power_pin.value(0)
#
#     def periodic_action(self, timer):
#         # Turn on the measure power
#         self._power_pin.value(1)
#         # Wait for a while
#         time.sleep(1)
#         self._logger.log_moisture(self._adc.read())
#
#
# class WaterPump(Periodical):
#     PUMP_PIN = 5  # D1 on board
#     WATERING_TIME = 1  # min
#
#     def __init__(self, logger, period_id, period_min):
#         super().__init__(logger, period_id, period_min)
#         self._pump_pin = machine.Pin(WaterPump.PUMP_PIN, machine.Pin.OUT)
#         self._pump_pin.value(0)
#
#     def periodic_action(self, timer):
#         self._pump_pin.value(1)
#         self._logger.log_water(True)
#         tim = machine.Timer(WATER_PUMP_STOP_TIMER)
#
#         def stop_water(timer):
#             self._pump_pin.value(0)
#             self._logger.log_water(False)
#
#         tim.init(period=WaterPump.WATERING_TIME*60*1000, mode=machine.Timer.ONE_SHOT, callback=stop_water)


class Logic(object):

    PERIOD_ID = 0
    PERIOD_MIN = 1

    def __init__(self):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Starting logic")
        self._temp_humid_sensor = temp_humidity_sensor.TempHumiditySensor()

    def periodic_start(self):
        tim = machine.Timer(Logic.PERIOD_ID)
        tim.init(period=Logic.PERIOD_MIN * 60 * 1000, mode=machine.Timer.PERIODIC, callback=self.periodic_action)

    def periodic_action(self, timer):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Starting periodic action")
        try:
            temp, humid = self._temp_humid_sensor.measure()
            log.log_msg(logger.INFO, "Measured temperature {} and humidity {}".format(temp, humid))
        except Exception as e:
            log.log_msg(logger.ERROR, "Periodic action failed: {}".format(e))


def run_it():
    logic = Logic()
    logic.periodic_start()


if __name__ == "__main__":
    run_it()