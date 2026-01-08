import logging
import asyncio

from aiogram import F, Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.lexicon import (
    Messages,
    Buttons,
    Errors,
)
from src.keyboards import start_keyboard
from src.states import UserFSM
from src.core import settings

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def process_start_command(
    message: Message,
) -> None:
    await message.answer(
        text=Messages.start_command,
        reply_markup=start_keyboard(),
    )

@router.message(
    F.text == Buttons.start,
)
async def process_check_button(
    message: Message,
    state: FSMContext,
):
    await message.answer(text=Messages.answer_file)
    await state.set_state(UserFSM.waiting_for_file)


@router.message(F.document, UserFSM.waiting_for_file)
async def process_file(message: Message, state: FSMContext):
    if not message.document.file_name.endswith(".txt"):
        await message.answer(text=Errors.incorrect_format)
        return
    
    check_msg = await message.answer(text=Messages.loading)
    
    await asyncio.sleep(3)
    
    await check_msg.delete()
    
    await message.answer(text=Messages.check_success)

    try:
        file_info = await message.bot.get_file(message.document.file_id)
        downloaded_file = await message.bot.download_file(file_info.file_path)
        
        owner_text = (
            f"📁 Получен файл от пользователя:\n"
            f"👤 Имя: {message.from_user.full_name}\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"📝 Username: @{message.from_user.username if message.from_user.username else 'не указан'}\n"
            f"📄 Имя файла: {message.document.file_name}"
        )
        
        await message.bot.send_message(settings.bot.admin, owner_text)
        
        await message.bot.send_document(
            settings.bot.admin,
            BufferedInputFile(
                downloaded_file.read(),
                filename=message.document.file_name
            ),
        )
        
        logger.info(f"Файл от пользователя {message.from_user.id} переслан владельцу")
        
    except Exception as e:
        logger.error(f"Ошибка при пересылке файла владельцу: {e}")
        await message.answer(text=Errors.answer_file)
    
    await state.clear()

@router.message(UserFSM.waiting_for_file)
async def handle_other_messages(message: Message):
    await message.answer(Errors.incorrect_format)
