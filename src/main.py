__doc__ = """Code to detect, read, and write to a MFRC522 RFID module and tag.

Useful links:
    [pimylifeup](https://github.com/pimylifeup/MFRC522-python/tree/master)
    [pubnub-console](https://www.pubnub.com/docs/console)
    [pubnub-admin-page](https://admin.pubnub.com/#/login)
"""

# Import Python packages
from datetime import datetime, timedelta
import sys
import time


# Import installed packages
from mfrc522 import MFRC522, SimpleMFRC522
import pywhatkit
import RPi.GPIO as GPIO


# Instantiate classes
rfid_manager = MFRC522()
rfid = SimpleMFRC522()


def detect_rfid_tag() -> bool:
    """Detect RFID tag. Return boolean status."""
    success = False
    try:
        while True:
            status, _ = rfid_manager.MFRC522_Request(rfid_manager.PICC_REQIDL)

            if status == rfid_manager.MI_OK:
                print("[INFO] : RFID tag detected!")

                status, uid = rfid_manager.MFRC522_Anticoll()
                if status == rfid_manager.MI_OK:
                    print(f"[INFO] : UID - ({uid})")
                    print("[INFO] : UID Hex - ({0})".format(":".join([hex(x)[2:].zfill(2) for x in uid])))
                    success = True
                    return success

            print('[WARNING] : Could not find RFID tag.')
            break

    except KeyboardInterrupt:
        print('\n[WARNING] : User interrupt')
        return success

    finally:
        print('[INFO] : Cleaning up GPIO')
        GPIO.cleanup()


def write_to_tag(message) -> bool:
    """Write user message to tag. Return write status as boolean."""
    success = False

    try:
        print('[WARNING] : Can only write to tag once!')
        print('[INFO] : Sleeping for 5 seconds...')
        time.sleep(5)
        print('[INFO] : Ready to write. Hold tag near module...')
        rfid.write(message)
        print('[INFO] : Success!')
        print(f'[INFO] : {message} written to tag')
        success = True
        return success

    except KeyboardInterrupt:
        print('\n[WARNING] : User interrupt')
        return success
        sys.exit(0)

    except Exception as ex:
        print(f'\n[EXCEPTION] : ({ex})')
        return success

    finally:
        print('[INFO] : Cleaning up GPIO')
        GPIO.cleanup()


def read_from_tag() -> tuple:
    """Read tag id and data. Return Tuple."""
    while True:
        try:
            print('[INFO] : Module ready to ready')
            print('[INFO] : Hold tag near module')
            tag_id, tag_text = rfid.read()
            print(f"[INFO] : Tag ID - ({tag_id})")
            print(f"[INFO] : Tag Data - ({tag_text})")
            return (tag_id, tag_text)

        except KeyboardInterrupt:
            print()
            print('[INFO] : User interrupted')
            sys.exit(0)

        finally:
            print('[INFO] : Cleaning up GPIO')
            GPIO.cleanup()


def send_whatsapp_message(
    whatsapp_msg: str,
    whatsapp_no: int,
    msg_delay: int = 3,
) -> None:
    """Send WhatsApp message. Return None."""
    country_code = '+1'
    number: str = country_code + str(whatsapp_no)

    # Simulated queue time
    wait_time = msg_delay # minutes

    now: str = datetime.now()
    act_now = now + timedelta(minutes=wait_time)
    act_hr = int(act_now.strftime("%H"))
    act_min = int(act_now.strftime("%M"))

    try:
        pywhatkit.sendwhatmsg(number, whatsapp_msg, act_hr, act_min, 90)
        print('Successfully sent WhatsApp message')

    except Exception as ex:
        print(f'Could not send WhatsApp message - ({ex})')


if __name__ == '__main__':
    WHATSAPP_MSG = ("Hello, this is an automated message. You are next in queue."
    " Approximately: 5 minutes till your reservation.")

    tag_found = detect_rfid_tag()

    if tag_found:
        print('[INFO] : Tag found. Start read.')
        tag_uid, tag_data = read_from_tag()
        print('[INFO] : Sending WhatsApp message')
        send_whatsapp_message(
            whatsapp_msg=WHATSAPP_MSG, whatsapp_no=tag_data, msg_delay= 2
        )

    if tag_found and tag_data is None:
        print('[INFO] : The tag does not have any data.')
        do_write = str(input('Write to tag? (y/N): ')).lower()

        if do_write == 'n':
            print('[INFO] : Not writing to tag.')
            print('[INFO] : Exiting program.')
            sys.exit(0)
        elif do_write == 'y':
            WHATSAPP_NUM = int(input('[INFO] : Enter your 10-digit Canadian phone number : '))
            # data = input('[INFO] : Enter data to write to tag here - ')
            write_to_tag(message=WHATSAPP_NUM)
            tag_uid, tad_data = read_from_tag()
            send_whatsapp_message(
                whatsapp_msg=WHATSAPP_MSG, whatsapp_no=tag_data,
            )
        else:
            print(f'[WARNING] : {do_write} not accepted as input.')

    print('[INFO] : Completed.')

