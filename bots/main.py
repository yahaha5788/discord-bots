from polaroidsupercolorinstantcamera import bot as polaroid
from harold import bot as harold
from dotenv import load_dotenv
from pathlib import Path
import os
import asyncio


if __name__ == "__main__":
    path_to_env = Path("C:/Users/thomp/pycharmprojects/discord-bots/misc/keys.env")
    load_dotenv(dotenv_path=path_to_env)

    polaroid_key = os.getenv('POLAROID_KEY')
    harold_key = os.getenv('HAROLD_KEY')


    async def runAll():
        try:
            await asyncio.gather(
                polaroid.start(polaroid_key),
                harold.start(harold_key)
            )
        except KeyboardInterrupt:
            await polaroid.close()
            await harold.close()


    asyncio.run(runAll())
