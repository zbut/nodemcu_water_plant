import esp
from flashbdev import bdev
import machine
import logger

ADC_MODE_VCC = 255
ADC_MODE_ADC = 0

_num_to_mode = {ADC_MODE_ADC: "ADC", ADC_MODE_VCC: "VCC"}


class ADC(object):
    def __init__(self, adc_mode):
        log = logger.get_logger()
        # Verify that ADC mode matches current one
        if adc_mode not in [ADC_MODE_VCC, ADC_MODE_ADC]:
            log.log_msg(logger.ERROR, "Bad adc mode {}".format(adc_mode))
            return
        if self.set_adc_mode(adc_mode):
            log.log_msg(logger.INFO, "ADC mode set to {}".format(_num_to_mode[adc_mode]))
            self._mode = adc_mode
        else:
            log.log_msg(logger.ERROR, "ADC mode is changed, restart to use it")
            self._mode = ADC_MODE_VCC - adc_mode  # The other one

    @staticmethod
    def set_adc_mode(mode):
        sector_size = bdev.SEC_SIZE
        flash_size = esp.flash_size()  # device dependent
        init_sector = int(flash_size / sector_size - 4)
        try:
            data = bytearray(esp.flash_read(init_sector * sector_size, sector_size))
            if data[107] == mode:
                return True  # flash is already correct; nothing to do
            else:
                data[107] = mode  # re-write flash
                esp.flash_erase(init_sector)
                esp.flash_write(init_sector * sector_size, data)
                return False
        except MemoryError:
            log = logger.get_logger()
            log.log_msg(logger.ERROR, "Could not allocate memory for setting adc mode, assuming it's {}".format(_num_to_mode[mode]))
            return True

    def read_vcc(self):
        log = logger.get_logger()
        if self._mode != ADC_MODE_VCC:
            log.log_msg(logger.ERROR, "Could not read VCC, mode is currently set to ADC")
            return 0
        vcc = machine.ADC(1)
        vcc_val = vcc.read() * 0.001024
        log.log_msg(logger.INFO, "VCC value is {}".format(vcc_val))
        return vcc_val

    def read_adc(self):
        log = logger.get_logger()
        if self._mode != ADC_MODE_ADC:
            log.log_msg(logger.ERROR, "Could not read ADC, mode is currently set to VCC")
            return 0
        adc_obj = machine.ADC(0)
        adc_val = adc_obj.read()
        log.log_msg(logger.INFO, "ADC value is {}".format(adc_val))
        return adc_val
