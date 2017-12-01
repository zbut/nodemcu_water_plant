
conf = {
    "wifi": [
        {
            "ssid": '',
            "password": ''
        },
        {
            "ssid": "",
            "password": ""
        }
    ],
    "thingspeak": {
        "host": "mqtt.thingspeak.com",
        "port": 1883,
        "client_id": "nodemcu_plant_water",
        "channel_id": "",
        "write_api_key": "",
        "fields": {
            "temperature": "field1",
            "humidity": "field2",
            "vcc": "field3"
        }
    }
}


def get_thingspeak_field(field_name):
    return conf["thingspeak"]["fields"][field_name]