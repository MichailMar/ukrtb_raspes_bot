from aiogram import Bot, Dispatcher, types
import config
import logging
import commands
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage


logging.basicConfig(level=config.LOGGING)

async def main():
    
    bot = Bot(token=config.TOKEN)
    dp  = Dispatcher(storage=MemoryStorage())

    dp.include_router(commands.timetable.timetable)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())