from gyron.bot import BotClient
from gyron.models import Update
from gyron.filters import filters
from gyron.state import StateManager
import asyncio

app = BotClient('TOKEN')
state_manager = StateManager(auto_clear=True) 


@app.on_update(filters.text('شروع'))
async def set_state(message:Update):

    await state_manager.set_state_for(message, 'awaiting_email', expire= 100)
    await app.reply('لطفا ایمیل خود را ارسال کنید')

@app.on_update(filters.text('کنسل'))
async def clear_state(message:Update):

    await state_manager.clear_state_for(message)
    await app.reply('کنسل شد')

@app.on_update(filters.at_state(state_manager, 'awaiting_email'))
async def received_email(message:Update):

    await app.reply(f'ایمیل شما دریافت شد : {message.text}')
    await state_manager.clear_state_for(message)
 

asyncio.run(app.run())