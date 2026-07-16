from gyron.bot import BotClient
from gyron.models import Update, InlineButton, InlineRow, InlineKeypad, CopyTextButton
from gyron.filters import filters
import asyncio

app = BotClient('TOKEN')

keypad = InlineKeypad(
    rows= [
        InlineRow(
            buttons= [
                InlineButton(text= 'دکمه 1', callback_data= 'btn1', copy_text= CopyTextButton('متنی که باید کپی بشه'))
            ]
        ),
        InlineRow(
            buttons= [
                InlineButton(text= 'دکمه 2', callback_data='btn2')
            ]

        )
    ]
)

@app.on_update(filters.text('/start'))
async def start(update:Update):

    await app.reply('تست inline keypad', markup= keypad)


@app.on_update(filters.callback_query('btn2'))
async def button2(update:Update):

    await app.send_message(update.callback_query.message.chat.id, 'کلیک کردی روی دکمه 2')


asyncio.run(app.run())