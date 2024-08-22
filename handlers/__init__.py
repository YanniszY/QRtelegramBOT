from aiogram import Dispatcher
from .qr_handlers import router as qr_router

def register_handlers(dp: Dispatcher):
    dp.include_router(qr_router)
