from gyron.bot import BotClient
from gyron.models import Keypad, KeypadRow, Button, Update
from gyron.filters import filters
import asyncio

app = BotClient('TOKEN')

keypad = Keypad(
    rows=[
        KeypadRow(
            buttons= [
                Button('اشتراک گذاری شماره', request_contact= True)
            ]
        )
    , KeypadRow(
        buttons= [
            Button('اشتراک گذاری لوکیشن', request_location= True)
        ]
    )],
one_time= False,
resize= True
)

@app.on_update(filters.text('/start'))
async def start(update:Update):

    await app.reply('تست reply keypad', markup= keypad)

@app.on_update(filters.contact())
async def contact(update:Update):

    await app.reply(f'شماره شما دریافت شد : {update.contact.phone_number}')

@app.on_update(filters.location())
async def location(update:Update):

    await app.reply(f'لوکیشن شما دریافت شد \n latitude : {update.location.latitude}\n longitude : {update.location.longitude}')



asyncio.run(app.run())
