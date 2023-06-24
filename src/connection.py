__doc__ = """
"""


# Import Python packages



# Import installed packages
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.pnconfiguration import PNConfiguration
# import RPi.GPIO as GPIO


# Import custom packages



PUBLISH_KEY="pub-c-f7bd05bd-5826-4e6b-b9f6-d38f14e5052b"
SUBSCRIBE_KEY="sub-c-24e6cf06-9e7c-4b02-b909-bb0af47cc53e"
CHANNEL="RFID-channel"
UUID="UUID"
# SSL_ON=False
PUBLISH_DATA = { "from" : "sourcecode" }


def callback(message, channel):
    # Use the Order Quantity value as the LED trigger
    print(message['order_quantity'])

    # Reset LEDs to OFF
    GPIO.output(11,False)
    GPIO.output(12,False)
    GPIO.output(13,False)
    
    if (message['order_quantity'] >= 100) and (message['order_quantity'] < 200):
        GPIO.output(11,True) # Turn on GREEN
    elif (message['order_quantity'] >= 200) and (message['order_quantity'] < 400):
        GPIO.output(12,True) # Turn on YELLOW
    elif (message['order_quantity'] >= 400):
        GPIO.output(13,True) # Turn on RED

class PubNubWrapper(object):
    """
    """
    def __init__(
        self,
        publish_key: str,
        subscribe_key: str,
        channel: str,
        uuid: str,
        ) -> None:

        # Class data attributes
        self.publisher = publish_key
        self.subscriber = subscribe_key
        self.channel = channel
        self.uuid = uuid

        # Instantiate class PNConfiguration
        pubnub_config = PNConfiguration()
        # Configure
        pubnub_config.publish_key = self.publisher
        pubnub_config.subscribe_key = self.subscriber
        pubnub_config.uuid = self.uuid
        # Instantiate PubNub
        # Class data attr : manager
        self.manager = PubNub(pubnub_config)

        # Instantiate class SubscribeListener
        # To read message from the Broker/ server
        self.listener = SubscribeListener()

    def subscribe_and_listen(self,):
        """Listen on given channel for messages."""
        # Add listener object to manager
        self.manager.add_listener(self.listener)
        # Subscribe
        self.manager.subscribe().channels(self.channel).execute()
        # Wait for the listener to connect to required channel on Broker
        self.listener.wait_for_connect()
        print(f"Connected to, and listening on {self.channel}")

    def send_msg(self, payload: str,):
            self.manager.publish().channel(self.channel).message(payload).sync()
            print('Message successfully sent.')

    def receive_msg(self,):
            msg = self.listener.wait_for_message_on(self.channel)
            print(f'Message successfully received. From channel: {msg.message}')



# GPIO.setmode(GPIO.BOARD) ## Use board pin numbering

# GPIO.setup(11, GPIO.OUT) ## Setup GPIO Pin 17 to OUT - Green
# GPIO.setup(12, GPIO.OUT) ## Setup GPIO Pin 18 to OUT - Yellow
# GPIO.setup(13, GPIO.OUT) ## Setup GPIO Pin 27 to OUT - Red

# GPIO.output(11,False) ## Turn on GPIO pin 17
# GPIO.output(12,False) ## Turn on GPIO pin 18
# GPIO.output(13,False) ## Turn on GPIO pin 27


if __name__ == '__main__':

    pubnub_manager = PubNubWrapper(
        publish_key=PUBLISH_KEY,
        subscribe_key=SUBSCRIBE_KEY,
        channel=CHANNEL,
        uuid=UUID,
    )

    pubnub_manager.subscribe_and_listen()

    tag_manager = RFIDWrapper()

    if tag_manager.write_to_tag():
        pubnub_manager.send_msg(payload=PUBLISH_DATA)

    if tag_manager.read_from_tag():
        pubnub_manager.send_msg(payload=PUBLISH_DATA)

        pubnub_manager.receive_msg()
