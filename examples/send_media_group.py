from gyron.bot import BotClient
from gyron.models import Update, InputMediaPhoto
import asyncio


app = BotClient('TOKEN')

@app.on_update()
async def sendmediagroup(update:Update):
   
    await app.send_media_group(
    update.chat.id,
    [
        InputMediaPhoto(
            media="https://www.beytoote.com/images/stories/fun/sky-profile-picture-2.jpg", is_local_file=False
        ),
        InputMediaPhoto(
            media="sky-profile-picture-2.jpg", is_local_file=True
      
        )
     
    ]
)
    

asyncio.run(app.run())