from polaroidsupercolorinstantcamera import bot as polaroid
#from harold import bot as harold
from dotenv import load_dotenv
from pathlib import Path
import os

path_to_env = Path("C:/Users/thomp/pycharmprojects/discord-bots/misc/keys.env")
load_dotenv(dotenv_path=path_to_env)

polaroid_key = os.getenv('POLAROID_KEY')
#harold_key = os.getenv('HAROLD_KEY')

polaroid.run(polaroid_key)
#harold.run(harold_key)