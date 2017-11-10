import machine
import time
import dht
import os
import micropython
micropython.alloc_emergency_exception_buf(100)

# Timer IDS
MOISTURE_MEASURE_TIMER = 1
TEMP_HUMID_MEASURE_TIMER = 2
WATER_PUMP_START_TIMER = 3
WATER_PUMP_STOP_TIMER = 4


class Periodical:
    def __init__(self, logger, period_id, period_min):
        self._logger = logger
        tim = machine.Timer(period_id)
        tim.init(period=period_min * 60 * 1000, mode=machine.Timer.PERIODIC, callback=self.periodic_action)

    def periodic_action(self, timer):
        pass

    def periodic_action_with_exceptions(self, timer):
        try:
            self.periodic_action(timer)
        except Exception as e:
            self._logger.log_exception(e)


class MoistureMeasurer(Periodical):
    ADC_PIN = 0
    MEASURE_POWER_PIN = 0  # D3 on board

    def __init__(self, logger, period_id, period_min):
        super().__init__(logger, period_id, period_min)
        self._adc = machine.ADC(MoistureMeasurer.ADC_PIN)
        self._power_pin = machine.Pin(MoistureMeasurer.MEASURE_POWER_PIN, machine.Pin.OUT)
        self._power_pin.value(0)

    def periodic_action(self, timer):
        # Turn on the measure power
        self._power_pin.value(1)
        # Wait for a while
        time.sleep(1)
        self._logger.log_moisture(self._adc.read())


class TempHumidMeasurer(Periodical):
    DATA_PIN = 4  # D2 on board

    def __init__(self, logger, period_id, period_min):
        super().__init__(logger, period_id, period_min)
        self._dht = dht.DHT22(machine.Pin(TempHumidMeasurer.DATA_PIN))

    def periodic_action(self, timer):
        self._dht.measure()
        self._logger.log_temp_humid(self._dht.temperature(), self._dht.humidity())


class WaterPump(Periodical):
    PUMP_PIN = 5  # D1 on board
    WATERING_TIME = 1  # min

    def __init__(self, logger, period_id, period_min):
        super().__init__(logger, period_id, period_min)
        self._pump_pin = machine.Pin(WaterPump.PUMP_PIN, machine.Pin.OUT)
        self._pump_pin.value(0)

    def periodic_action(self, timer):
        self._pump_pin.value(1)
        self._logger.log_water(True)
        tim = machine.Timer(WATER_PUMP_STOP_TIMER)

        def stop_water(timer):
            self._pump_pin.value(0)
            self._logger.log_water(False)

        tim.init(period=WaterPump.WATERING_TIME*60*1000, mode=machine.Timer.ONE_SHOT, callback=stop_water)


class WaterLogger:
    def __init__(self, log_file_path):
        self._log_file_path = log_file_path
        if log_file_path in os.listdir("."):  # os.path is unavailable
            os.remove(log_file_path)
        self._rtc = machine.RTC()

    def log_moisture(self, moisture_value):
        cur_time = self._rtc.datetime()
        self.log_msg("Time: {}, Moisture: {}\n".format(cur_time, moisture_value))

    def log_temp_humid(self, temp_value, humid_value):
        cur_time = self._rtc.datetime()
        self.log_msg("Time: {}, Temp: {}, Humid: {}\n".format(cur_time, temp_value, humid_value))

    def log_water(self, is_start):
        cur_time = self._rtc.datetime()
        word = "Starting" if is_start else "Stopping"
        self.log_msg("Time: {}, {} to water the plants\n".format(cur_time, word))

    def log_exception(self, msg):
        cur_time = self._rtc.datetime()
        msg_with_time = "Time: {}, {}".format(cur_time, msg)
        self.log_msg(msg_with_time)

    def log_msg(self, msg):
        with open(self._log_file_path, "a") as f:
            f.write(msg)


def run_it():
    water_logger = WaterLogger("log.txt")
    moist = MoistureMeasurer(water_logger, MOISTURE_MEASURE_TIMER, 2)
    temp_humid = TempHumidMeasurer(water_logger, TEMP_HUMID_MEASURE_TIMER, 3)
    water_pump = WaterPump(water_logger, WATER_PUMP_START_TIMER, 2)


if __name__ == "__main__":
    run_it()