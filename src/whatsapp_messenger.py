__doc__ = """Script to send a WhatsApp message.

Send required message to defined phone number 3 minutes post execution of script.
"""


# Import Python packages
from datetime import datetime, timedelta


# Import installed packages
import pywhatkit
import pyautogui


# Define your message and WhatsApp number
WHATSAPP_MSG = ("Hello, this is an automated message. You are next in queue."
    " Approximately: 5 minutes till your reservation.")
WHATSAPP_NO = "1234567890"


def send_whatsapp_message(
    whatsapp_msg: str,
    whatsapp_no: int,
    msg_delay: int = 3,
) -> None:
    """Send WhatsApp message. Return None."""
    country_code = '+1'
    number = country_code + str(whatsapp_no)

    # Simulated queue time
    wait_time = msg_delay # minutes

    now = datetime.now()
    act_now = now + timedelta(minutes=wait_time)
    act_hr = int(act_now.strftime("%H"))
    act_min = int(act_now.strftime("%M"))

    try:
        pywhatkit.sendwhatmsg(number, whatsapp_msg, act_hr, act_min, 90)
        print('Successfully sent WhatsApp message')

    except Exception as ex:
        print(f'Could not send WhatsApp message - ({ex})')


if __name__ == "__main__":
    send_whatsapp_message(whatsapp_msg=WHATSAPP_MSG, whatsapp_no=WHATSAPP_NO,)
    