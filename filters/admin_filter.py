from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api.database import get_user

class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        user = await get_user(message.from_user.id)
        if user:
            return user.is_admin == "admin"

        return False