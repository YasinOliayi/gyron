from gyron.bot import BotClient
from gyron.models import Update
from gyron.filters import filters
import asyncio

app = BotClient('TOKEN')

@app.on_update(filters.is_admin())
async def admin(update:Update):
    await app.reply('you are admin')

@app.on_update(filters.is_creator())
async def creator(update:Update):
    await app.reply('you are creator')

@app.on_update(filters.is_member())
async def member(update:Update):
    await app.reply('you are member')

@app.on_update(filters.is_restricted())
async def restricted(update:Update):
    await app.reply('you are restricted')

asyncio.run(app.run())