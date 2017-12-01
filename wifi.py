import config
import network
import logger
import time


def connect(timeout_s=5):
    log = logger.get_logger()
    sta_if = network.WLAN(network.STA_IF)
    log.log_msg(logger.INFO, "Connecting to wifi")
    try:
        if not sta_if.isconnected():
            sta_if.active(True)
            for connection_details in config.conf["wifi"]:
                log.log_msg(logger.INFO, "Trying to connect to {} with timeout of {} seconds".format(connection_details["ssid"], timeout_s))
                sta_if.connect(connection_details["ssid"], connection_details["password"])
                end_time = time.time() + timeout_s
                while not sta_if.isconnected() and (time.time() < end_time):
                    pass
                if sta_if.isconnected():
                    log.log_msg(logger.INFO, "Connected successfully with ip {}".format(sta_if.ifconfig()[0]))
                    return sta_if.ifconfig()[0]
                else:
                    log.log_msg(logger.ERROR, "Connection time out")
        else:
            log.log_msg(logger.INFO, "Already connected with ip {}".format(sta_if.ifconfig()[0]))
            return sta_if.ifconfig()[0]
        return ""
    except Exception as e:
        log.log_msg(logger.ERROR, "Could not connect to wifi: {}".format(e))
        return ""
