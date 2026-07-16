from gyron.bot import BotClient
from gyron.filters import filters
from gyron.models import Update
import asyncio


app = BotClient('TOKEN')


@app.on_update(filters.new_member())
async def welcome(update : Update):

    await app.send_message(update.chat.id, 'خوش آمدید')


@app.on_update(filters.left_member())
async def good_by(update : Update):

    await app.send_message(update.chat.id, 'خدا نگه دار')



  
asyncio.run(app.run())