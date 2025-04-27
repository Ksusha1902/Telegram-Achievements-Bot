import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token='YOUR BOT ID')
dp = Dispatcher()
async def on_startup():
    print('Bot launched successfully.')

@dp.message(Command('start'))
async def cmd(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    response = f"Привет, {first_name} {last_name or ''}! 👋\n" \
               f"Ваше имя пользователя: @{username or 'не указано'}\n"\
               f"Ваш ID: {user_id}"


    await message.answer(response)

async def main():
    await on_startup()
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(5)  # Ждем перед повторной попыткой

if __name__ == '__main__':
    asyncio.run(main())
