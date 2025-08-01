from polaroidsupercolorinstantcamera import bot as polaroid
from dotenv import load_dotenv
import os
import logging

handler = logging.FileHandler(filename='polaroid.log', encoding='utf-8', mode='w')


if __name__ == '__main__': # main program for testing, since the bot is active in servers
    load_dotenv('keys.env')

    polaroid_key = os.getenv('POLAROID_TEST_KEY')

    polaroid.run(polaroid_key, log_handler=handler, log_level=logging.DEBUG)