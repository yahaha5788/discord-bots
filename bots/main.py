from harold_cogs import bot as harold
#from polaroidsupercolorinstantcamera import bot as polaroid
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    load_dotenv('keys.env')

    harold_key = os.getenv('HAROLD_KEY')
    #polaroid_key = os.getenv('POLAROID_KEY')

    harold.run(harold_key)
    #polaroid.run(polaroid_key)