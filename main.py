import asyncio


from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command


from functions import (
    start_handler,
    anketa_start,
    get_fio,
    get_phone,
    get_tajriba,
    get_old_ish,
    get_oylik,
    get_cv,
    get_tasdiq
)
from states import AnketaState
from config import TOKEN

TOKEN = TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


def register_handlers():
    dp.message.register(start_handler, Command("start"))
    dp.message.register(anketa_start, F.text == "Anketani boshlash")
    dp.message.register(get_fio, AnketaState.fio)
    dp.message.register(get_phone, AnketaState.phone, F.contact)
    dp.message.register(get_tajriba, AnketaState.tajriba)
    dp.message.register(get_old_ish, AnketaState.old_ish)
    dp.message.register(get_oylik, AnketaState.oylik)
    dp.message.register(get_cv, AnketaState.cv)
    dp.message.register(get_tasdiq, AnketaState.tasdiq)


async def main():
    register_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
