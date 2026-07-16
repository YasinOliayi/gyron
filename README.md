An async framework for building powerful bots for Bale Messenger.

# Features

- Fully Async
- Webhook Support
- Long Polling
- Filters System
- FSM / States
- Models
- Fast & Lightweight
- Easy to Use

---

# Installation

```bash
pip install gyron
```

---

# Quick Start

```python
from gyron.bot import BotClient
import asyncio

app = BotClient('TOKEN')

@app.on_update()
async def echo(update):
    await app.reply(update.text)

asyncio.run(app.run())
```

---

# Links

- PyPI: https://pypi.org/project/gyron/
- GitHub: https://github.com/YasinOliayi/gyron

---

# License

MIT License
