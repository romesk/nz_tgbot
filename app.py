from loader import db
from utils.db_api import postgresql

async def on_startup(dp):
    import filters
    import middlewares
    
    from handlers.users.scheduled import start_checker
    await start_checker(dp)

    filters.setup(dp)
    middlewares.setup(dp)

    # connecting to DB
    await postgresql.on_startup(dp)

    # drop tables
    # await db.gino.drop_all()

    # creating tables
    await db.gino.create_all()

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
