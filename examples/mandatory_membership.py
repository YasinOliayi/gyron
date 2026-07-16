from gyron.bot import BotClient
from gyron.models import Update
from gyron.filters import filters
import asyncio


app = BotClient('TOKEN')

@app.on_update(filters.is_joined("CHAT_ID"), filters.private())
async def joined(update:Update):

    await app.reply('جوین هستی')

@app.on_update(filters.not_is_joined("CHAT_ID"), filters.private())
async def not_joined(update:Update):

    await app.reply('جوین نیستی')

asyncio.run(app.run())