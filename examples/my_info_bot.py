from gyron.bot import BotClient, Update
from gyron.filters import filters
import asyncio


app = BotClient('enter your token here')


@app.on_update(filters.private())
async def send_info(update: Update):

    chat_id = update.chat_id
    user_id = update.user_id

    response = await app.get_chat(chat_id)

    profile_text = f"""
        بیوگرافی: {response.bio}
        یوزرنیم: @{response.username}
        آیدی عددی: {user_id}
        چت آیدی: {chat_id}
        """

    text = f"""
        اطلاعات پیام شما:

        ```{update}```

        اطلاعات شما:

        ```{profile_text}```
        """

    await app.send_message(chat_id, text)


asyncio.run(app.run())

