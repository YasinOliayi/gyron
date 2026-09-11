import asyncio
import time
import random
import utils
from gyron.bot import BotClient
from gyron.filters import filters


bot = BotClient(
        '',
        global_queue_maxsize=50000000,
        user_queue_maxsize=100
    )



@bot.on_update(filters.callback_query('button_data'))
async def handler1(update):
    pass


@bot.on_update(filters.private())
async def handler2(update):
    pass


@bot.on_update(filters.text())
async def handler3(update):
    pass


@bot.on_update(filters.command('start'))
async def handler4(update):
    pass


@bot.on_update(filters.command('help'))
async def handler5(update):
    pass


@bot.on_update(filters.callback_query('menu'))
async def handler6(update):
    pass


@bot.on_update(filters.callback_query('settings'))
async def handler7(update):
    pass


@bot.on_update(filters.callback_query('profile'))
async def handler8(update):
    pass


@bot.on_update(filters.callback_query('back'))
async def handler9(update):
    pass


@bot.on_update(filters.private())
async def handler10(update):
    pass


@bot.on_update(filters.text())
async def handler11(update):
    pass


@bot.on_update(filters.command('test'))
async def handler12(update):
    pass


@bot.on_update(filters.command('game'))
async def handler13(update):
    pass


@bot.on_update(filters.callback_query('play'))
async def handler14(update):
    pass


@bot.on_update(filters.callback_query('exit'))
async def handler15(update):
    pass


@bot.on_update(filters.callback_query('confirm'))
async def handler16(update):
    pass


@bot.on_update(filters.callback_query('cancel'))
async def handler17(update):
    pass


@bot.on_update(filters.private())
async def handler18(update):
    pass


@bot.on_update(filters.text())
async def handler19(update):
    pass


@bot.on_update(filters.command('about'))
async def handler20(update):
    pass






import asyncio
import time
import psutil


async def benchmark(updates):

    process = psutil.Process()


    memory_before = process.memory_info().rss

  
    process.cpu_percent(None)

    start = time.perf_counter()

    for update in updates:
        await bot.global_queue.put(update)

    await bot.global_queue.join()

    elapsed = time.perf_counter() - start

   
    cpu = process.cpu_percent(None)

    
    memory_after = process.memory_info().rss

    memory_before_mb = memory_before / 1024 / 1024
    memory_after_mb = memory_after / 1024 / 1024

    print()
    print(f"Updates: {len(updates):,}")
    print(f"Time: {elapsed:.3f}s")
    print(f"Throughput: {len(updates) / elapsed:,.0f} updates/sec")
    print(f"CPU: {cpu:.1f}%")
    print(f"Memory before: {memory_before_mb:.1f} MB")
    print(f"Memory after: {memory_after_mb:.1f} MB")





async def main():

    

    asyncio.create_task(bot._extract_user_id())

    updates = []

    update_generators = [
        utils.make_message_update,
        utils.make_callback_update,
        utils.make_document_update,
    ]

    user_count = 50_000
    updates_per_user = 20

    for user_id in range(user_count):

        for _ in range(updates_per_user):

            make_update = random.choice(update_generators)

            update = make_update(user_id)

            updates.append(update)

    print(f"Generated {len(updates):,} updates")

    await benchmark(updates)


asyncio.run(main())