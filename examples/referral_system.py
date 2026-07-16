from gyron.bot import BotClient
from gyron.filters import filters
from gyron.models import Update
import asyncio

app = BotClient('TOKEN')


@app.on_update(filters.equals('/start'), filters.private())
async def start(update:Update):

    result = await app.create_referral_link(update.author.id)
    
    await app.reply(f'لینک دعوت اختصاصی شما : {result}')

@app.on_update(filters.is_referral())
async def referral_received(update:Update):

    result = await app.extract_referral_payload(update.text)

    await app.reply(f'شما دعوت شده اید از طرف {result}')

asyncio.run(app.run())