from gyron.bot import BotClient
from gyron.models import Update
from gyron.filters import filters
import asyncio
import os


app = BotClient('TOKEN')

@app.on_update(filters.document())
async def download_and_send(update: Update):

    reply = await app.reply("در حال دانلود فایل شما هستیم...")
  
    try:
        file_id = update.document.id
        file = await app.get_file(file_id)

        url = await app.create_download_link(file.path)

        file_name = f"{update.chat.id}_{update.message_id}"

        await app.download(url, file_name=file_name)

        await app.send_document(
            update.chat.id,
            file=file_name,
            is_local_file=True
        )

    finally:
        await app.delete_message(update.chat.id, reply.message_id)
        os.remove(file_name)

asyncio.run(app.run())