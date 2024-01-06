import os
import io
import time
import base64
import discord
from selenium import webdriver

def trim_text(text, pos):
    return text[pos:].split(' ')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        num = message.content.find('https://www.google.com/travel/flights/s')
        if (num < 0):
            pass
        else:
            url = trim_text(message.content, num)[0]
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument('--hide-scrollbars')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(2)
            page_rect = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
            screenshot_config = {
                "captureBeyondViewport": True,
                "clip": {
                    "width": page_rect["contentSize"]["width"] * 0.9,
                    "height": 300,
                    "x": page_rect["contentSize"]["width"] * 0.05,
                    "y": 105,
                    "scale": 1,
                },
            }
            base64_image = driver.execute_cdp_cmd("Page.captureScreenshot", screenshot_config)
            driver.quit()
            file = discord.File(io.BytesIO(base64.b64decode(base64_image["data"])), filename='img.png')
            await message.channel.send(file=file)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.environ["GOOGLIGHTS_PICASSO_BOT_TOKEN"])