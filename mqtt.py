#author= Christian Huppertz

import paho.mqtt.client as mqtt
import strip as st
import logging

class main:
    #Create logging module
    logging.basicConfig(filename='WS2812Controller.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d.%m.%y %I:%M:%S %p')
    logging.info('Main programm started')

    global strip #why has it to be global?
    strip = st.strip_config(58, 12) #2nd param should be reset to 18 after remote testing

    def on_connect(client, userdata, flags, rc):
        logging.info("Mqtt connection established - " +str(rc))
        print("Connectet")
        
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("zimmer/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        
        if msg.topic == "zimmer/project2/brightness/set":
            strip.fadeStripBrightness(int(msg.payload),True)

        elif msg.topic == "zimmer/project2/light/switch":
            strip.switch(msg.payload)

        elif msg.topic == "zimmer/project2/rgb/set":
            values = msg.payload.split(',')
            strip.fadeColor(int(values[0]),int(values[1]),int(values[2]))
        
        elif msg.topic == "zimmer/project2/effect/set":
            strip.setFadeSpeed(msg.payload)

        elif msg.topic == "zimmer/project2/temp/set":
            strip.setWhiteValue(msg.payload, True)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    #client.connect("127.0.0.1", 1883, 60) #local setup
    client.connect("192.168.2.114", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Forced Shutdown")

mqqt_start = main()
