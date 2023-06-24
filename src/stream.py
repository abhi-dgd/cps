# Import Python libraries
import os
import sys
import time

# Importing PubBub libraries
import pubnub
import RPi.GPIO as GPIO
from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback, PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException

# Set constants
CHANNEL = 'course_proj' # Set PubNub channel name
WRITE_KEY: str = '' # Publish key
READ_KEY: str = '' # Subscribe key
CLIENT_ID = 'abhishek' # Universal Unique Identifier
TO_PUBLISH = {"FROM SCRIPT" : "CONNECTED"} # Data to be published
TURN_ON_CAMERA = {'ON', 'on', 'o', 'Start', 'start',}
TURN_OFF_CAMERA = {'OFF', 'off', 'Stop', 'stop',}
QUIT_SCRIPT = {'q', 'Q', 'QUIT', 'quit'}


if __name__ == '__main__':
    # Create PNConfiguration obj
    pnconf = PNConfiguration()

    # Set keys
    pnconf.publish_key = WRITE_KEY
    pnconf.subscribe_key = READ_KEY
    pnconf.uuid = CLIENT_ID

    # Create PubNub from pnconf instance
    pubnub = PubNub(pnconf)

    # Create listener obj to read from Server
    my_listener = SubscribeListener()
    
    # Add listner obj to PubNub obj to subscribe to it
    pubnub.add_listener(my_listener)
    
    # Subscribe created channel. Daemon thread
    pubnub.subscribe().channels(CHANNEL).execute() 
    
    # Wait for the listener obj to connect to the Server channel
    my_listener.wait_for_connect()
    print(f"Connected and listening to '{CHANNEL}'") # Print confirmation msg

    # Publish required data to the mentioned channel
    print(f"Publishing '{TO_PUBLISH}' to PubNub console")
    pubnub.publish().channel(CHANNEL).message(TO_PUBLISH).sync()
    
    while True:
        # Read new msg on the channel
        result = my_listener.wait_for_message_on(CHANNEL)
        print(result.message)
        
        for result, value in (result.message).items():
            
            if value in (TURN_ON_CAMERA): # Start stream
                print('Camera on. Starting stream to Adafruit..')
                os.system("adafruit-io camera start -f cam_feed -m False -r 2")
                
            elif value in (TURN_OFF_CAMERA): # End stream
                print('Camera turning off. Stopping stream..')
                os.system("adafruit-io camera stop -f cam_feed -m False -r 2")
            
            elif value in (QUIT_SCRIPT): # Quit script - for terminal
               print('Exiting script..')
               os._exit(0)