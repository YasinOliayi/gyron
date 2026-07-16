from gyron.bot import BotClient
import asyncio


app = BotClient('TOKEN')


@app.on_update()
async def echo(update):

    await app.reply(update.text)

  
asyncio.run(app.run())