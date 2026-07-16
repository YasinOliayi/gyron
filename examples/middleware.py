from gyron.bot import BotClient
import asyncio


app = BotClient('TOKEN')


@app.middleware()
async def middleware(update, call_next):

    print('before handler')
    await call_next()
    print('after handler')


@app.on_update()
async def echo(update):

    await app.reply(update.text)

  
asyncio.run(app.run())