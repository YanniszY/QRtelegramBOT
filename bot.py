from aiogram import Bot, F, Router, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram import types
import asyncio
import segno
import tempfile
import sqlite3
from config import BOT_TOKEN
from handlers import register_handlers

#from States.states import UserOptions
#from keyboards.kb import kb, size_kb





async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())