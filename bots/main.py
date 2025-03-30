from polaroidsupercolorinstantcamera import bot as polaroid
from harold import bot as harold
from dotenv import load_dotenv
import os

load_dotenv()

polaroid.run(os.getenv("POLAROID_KEY"))
harold.run(os.getenv("HAROLD_KEY"))