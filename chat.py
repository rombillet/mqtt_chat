import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions
import sys
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes

if len(sys.argv) < 2:
    print("usage: python chat.py <name>")
    sys.exit(1)

NAME = sys.argv[1]

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print("broker refused connection:", reason_code)
        return
    print("connected")
    client.subscribe("chat", options=SubscribeOptions(qos=2, noLocal=True))

def on_message(client, userdata, msg):
    text = msg.payload.decode()
    print(text)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5, client_id=NAME)
client.on_connect = on_connect
client.on_message = on_message

props = Properties(PacketTypes.CONNECT)
props.SessionExpiryInterval = 30

client.connect("localhost", 1883, clean_start=False, properties=props)
client.loop_start()
client.loop_start()

try:
    while True:
        text = input()
        client.publish("chat", f"{NAME}: {text}", qos=2)
except KeyboardInterrupt:
    info = client.publish("chat", f"{NAME} left the chat", qos=2)
    info.wait_for_publish(timeout=5)
finally:
    client.disconnect()
    client.loop_stop()
