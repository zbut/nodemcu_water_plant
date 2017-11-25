import mqtt
import logger
import config


class ThingspeakComm(object):

    def __init__(self):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Initiating communication to Thingspeak")
        try:
            client = mqtt.MQTTClient(config.conf["thingspeak"]["channel_id"], config.conf["thingspeak"]["host"], config.conf["thingspeak"]["port"])
            client.connect()
            client.disconnect()
            log.log_msg(logger.INFO, "Connection successful")
        except Exception as e:
            log.log_msg(logger.ERROR, "Could not connect: {}".format(e))

    def send_data(self, dict_of_fields):
        log = logger.get_logger()
        log.log_msg(logger.INFO, "Sending data to thingspeak")
        try:
            client = mqtt.MQTTClient(config.conf["thingspeak"]["channel_id"], config.conf["thingspeak"]["host"], config.conf["thingspeak"]["port"])
            client.connect()
            credentials = "channels/{:s}/publish/{:s}".format(config.conf["thingspeak"]["channel_id"], config.conf["thingspeak"]["write_api_key"])
            payload = "&".join(["{}={}".format(key, value) for key, value in dict_of_fields.items()]) + "\n"
            client.publish(credentials, payload)
            client.disconnect()
            log.log_msg("Data was sent")
        except Exception as e:
            log.log_msg(logger.ERROR, "Could not send data: {}".format(e))