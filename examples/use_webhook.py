from gyron.bot import BotClient
import asyncio


token = 'TOKEN'
webhook_url = 'https://dgjzs-217-218-35-75.free.pinggy.net/webhk'


app = BotClient(token, use_webhook=True)


@app.on_update()
async def start(update):

    await app.reply('سلام')

async def main():

    res = await app.set_webhook(webhook_url)

    if res:
        print('started')
        await app.run(webhook_path='/webhk')


asyncio.run(main())