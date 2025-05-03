from polaroidsupercolorinstantcamera import bot as polaroid
from dotenv import load_dotenv
import os
import logging

handler = logging.FileHandler(filename='polaroid.log', encoding='utf-8', mode='w')


if __name__ == '__main__':
    load_dotenv('polaroid_key.env')

    polaroid_key = os.getenv('POLAROID_KEY')

    polaroid.run(polaroid_key)