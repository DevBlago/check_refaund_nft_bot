import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.core import settings
from src.keyboards import get_main_menu_commands
from src.handlers import users_router

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
           "%(lineno)d - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

async def main() -> None:
    bot = Bot(
        token=settings.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    await bot.set_my_commands(get_main_menu_commands())

    dp.include_router(users_router)

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher) -> None:
    logging.info("Bot started up")

async def shutdown(dispatcher: Dispatcher) -> None:
    logging.info("Bot shutting down")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped")