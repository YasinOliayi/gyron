from gyron.bot import BotClient, Update
from gyron.filters import filters

import asyncio


TOKEN = "enter your bot-token here"


app = BotClient(TOKEN)


@app.on_update(filters.equals('سکوت'), filters.group(),
               filters.reply())
async def mute(update: Update):

    chat_id = update.chat.id

    target_user_id = update.reply_to_message.author.id

    response = await app.restrict_member(chat_id, target_user_id, can_send_messages=False)

    if response.ok:

        await app.reply('کاربر سکوت شد.')


@app.on_update(filters.equals('رفع سکوت'), filters.group(),
               filters.reply())
async def un_mute(update: Update):

    chat_id = update.chat.id

    target_user_id = update.reply_to_message.author.id

    response = await app.restrict_member(chat_id, target_user_id, can_send_messages=True)

    if response.ok:

        await app.reply('کاربر از سکوت خارج شد.')


asyncio.run(app.run())
