from aiogram import Bot
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext

from states import AnketaState
from config import group_id

CHANNEL_ID = group_id



async def start_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Anketani boshlash")]],
        resize_keyboard=True
    )

    await message.answer(
        "Assalomu alaykum 👋\nAnketani boshlash uchun tugmani bosing.",
        reply_markup=keyboard
    )



async def anketa_start(message: Message, state: FSMContext):
    await message.answer("F.I.O kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AnketaState.fio)



async def get_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Telefon yuborish", request_contact=True)]],
        resize_keyboard=True
    )

    await message.answer("Telefon raqamingizni yuboring:", reply_markup=keyboard)
    await state.set_state(AnketaState.phone)



async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)

    await message.answer(
        "Ish tajribangiz (masalan: 1-3 yil):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AnketaState.tajriba)



async def get_tajriba(message: Message, state: FSMContext):
    await state.update_data(tajriba=message.text)

    await message.answer("Oldingi ish joyingiz va lavozimingiz:")
    await state.set_state(AnketaState.old_ish)



async def get_old_ish(message: Message, state: FSMContext):
    await state.update_data(old_ish=message.text)

    await message.answer("Oldingi oyligingizni kiriting (faqat raqam):")
    await state.set_state(AnketaState.oylik)



async def get_oylik(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Faqat raqam kiriting va joy tashlamay kiriting.")
        return

    await state.update_data(oylik=message.text)

    await message.answer("CV yuboring (PDF yoki rasm):")
    await state.set_state(AnketaState.cv)



async def get_cv(message: Message, state: FSMContext):
    if message.document:
        if message.document.mime_type != "application/pdf":
            await message.answer("❗ Faqat PDF yuboring.")
            return

        await state.update_data(
            cv_file_id=message.document.file_id,
            cv_type="document"
        )

    elif message.photo:
        await state.update_data(
            cv_file_id=message.photo[-1].file_id,
            cv_type="photo"
        )

    else:
        await message.answer("❗ PDF yoki rasm yuboring.")
        return

    await message.answer("Tasdiqlash uchun voice yoki video yuboring:")
    await state.set_state(AnketaState.tasdiq)


async def get_tasdiq(message: Message, state: FSMContext, bot: Bot):
    if not (message.voice or message.video):
        await message.answer("❗ Voice yoki video yuboring.")
        return

    data = await state.get_data()

    text = f"""
📋 YANGI FOYDALANUVCHI !

👤 F.I.O: {data['fio']}
📞 Telefon: {data['phone']}
💼 Tajriba: {data['tajriba']}
🏢 Oldingi ish: {data['old_ish']}
💰 Oylik: {data['oylik']}
"""

    await bot.send_message(CHANNEL_ID, text)

    # CV ni to‘g‘ri turda yuborish
    if data["cv_type"] == "document":
        await bot.send_document(CHANNEL_ID, data["cv_file_id"])
    else:
        await bot.send_photo(CHANNEL_ID, data["cv_file_id"])

    # Voice yoki Video
    if message.voice:
        await bot.send_voice(CHANNEL_ID, message.voice.file_id)
    else:
        await bot.send_video(CHANNEL_ID, message.video.file_id)

    await message.answer("✅ Anketangiz qabul qilindi, Rahmat!")
    await state.clear()
