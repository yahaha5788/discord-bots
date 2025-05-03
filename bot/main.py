from harold import bot as harold
from dotenv import load_dotenv
import os
import logging

handler = logging.FileHandler(filename='harold.log', encoding='utf-8', mode='w')


if __name__ == '__main__':
    load_dotenv('harold_key.env')

    harold_key = os.getenv('HAROLD_KEY')
    #polaroid_key = os.getenv('POLAROID_KEY')

    harold.run(harold_key, log_handler=handler, log_level=logging.DEBUG)
    #polaroid.run(polaroid_key)