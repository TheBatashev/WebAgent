from json import load
from aiogram import Bot, Dispatcher

from dotenv import load_dotenv, find_dotenv
from config import BotConfig
from agent import get_agent
from handlers import router
import asyncio

load_dotenv(find_dotenv(), override=False)


async def main():

    bot = Bot(BotConfig.bot_token)
    dp = Dispatcher()

    bot.agent = await get_agent()

    dp.include_router(router)

    bot_info = await bot.get_me()
    print(f"Bot started as {bot_info.username}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())