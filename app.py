from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config
from loader import db, bot
from utils.misc.month_broadcast import month_broadcast


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    scheduler = AsyncIOScheduler(timezone="UTC")

    try:
        db.create_table_users()
    except Exception as e:
        print(e)

    print(db.select_all_users())

    try:
        db.create_table_reviews()
    except Exception as e:
        print(e)

    try:
        db.create_table_month_reviews()
    except Exception as e:
        print(e)

    scheduler.add_job(month_broadcast, "cron", day="1", hour="18", minute="0", second="0", args=[bot, config])
    scheduler.start()



if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
