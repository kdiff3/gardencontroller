import paho.mqtt.client as mqtt

from views.clientdatasocketadapter import *

class MqttView:
    def __init__(self, config):
        self.config = config
        self.adapter = clientDataSocketAdapter()
        self.view_data = self.adapter.get_view_data()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(self.config["mqtt_username"], password=self.config["mqtt_password"])
        print("Welcome to Gardencontroller MQTT")
        self.client.connect(self.config["mqtt_broker"], 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def update(self):
        self.view_data = self.adapter.get_view_data()
        self.client.publish("garden/temperature", self.view_data["soil_temperature"])
        self.client.publish("garden/luminocity", self.view_data["soil_luminocity"])
        self.client.publish("garden/moist", self.view_data["soil_moisture"])
        self.client.publish("garden/battery", self.view_data["battery_charge_status"])
        self.client.publish("garden/cistern", self.view_data["cistern_level"])
        self.client.publish("garden/source", self.view_data["source_wet"])
        self.client.publish("garden/pumpout", (self.view_data["pump_out_status"] and self.view_data["pump_out_enabled"]))
        self.client.publish("garden/pumpin", (self.view_data["pump_in_status"] and self.view_data["pump_in_enabled"]))
