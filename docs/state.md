# `StateManager`

کلاس `StateManager` برای مدیریت وضعیت (**State**) کاربران و پیاده‌سازی جریان‌های چندمرحله‌ای (FSM) استفاده می‌شود. با استفاده از این کلاس می‌توانید وضعیت فعلی هر کاربر را ذخیره، بررسی و در زمان مناسب حذف کنید.

## نحوه‌ی استفاده

```python
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
```

---

## ایجاد `StateManager`

```python
manager = StateManager(...)
```

| پارامتر | نوع | توضیحات |
|---------|------|----------|
| `auto_clear` | `bool` | **اختیاری.** مقدار پیش‌فرض `True` است. در صورت فعال بودن، وضعیت‌های منقضی‌شده به‌صورت خودکار از حافظه حذف می‌شوند. |

---

## `set_state_for`

وضعیت جدیدی برای کاربر ذخیره می‌کند.

| پارامتر | نوع | توضیحات |
|---------|------|----------|
| `update` | `Update` | **اجباری.** آپدیت مربوط به کاربری که وضعیت برای او ذخیره می‌شود. |
| `state` | `str` | **اجباری.** نام یا شناسه‌ی وضعیت موردنظر. |
| `expire` | `int` | **اختیاری.** مدت اعتبار وضعیت بر حسب ثانیه. مقدار پیش‌فرض `30` ثانیه است. |

---

## `get_state_for`

وضعیت فعلی کاربر را برمی‌گرداند.

| مقدار بازگشتی | نوع | توضیحات |
|---------------|------|----------|
| `str \| None` | `str \| None` | در صورت وجود وضعیت فعال، نام آن بازگردانده می‌شود؛ در غیر این صورت مقدار `None` برگردانده خواهد شد. |

---

## `clear_state_for`

وضعیت ذخیره‌شده‌ی کاربر را حذف می‌کند.

| پارامتر | نوع | توضیحات |
|---------|------|----------|
| `update` | `Update` | **اجباری.** آپدیت مربوط به کاربری که وضعیت او باید حذف شود. |