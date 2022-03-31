from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
import os

TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
    await bot.set_webhook(os.getenv('APP_URL'))

async def on_shutdown(dp):
    await bot.delete_webhook()


subscription_check_button = KeyboardButton('Проверить подписку')
subscription_check_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(subscription_check_button)

not_subscribed_message = f'Привет!\n' \
                         f'Меня зовут Женя Сегеда, я занимаюсь маркетингом с 2014 года. А ты скорее всего хочешь получить обещанный в рекламе стикер-пак для сторис. Сделать это можно в два шага:\n' \
                         f'1. Подпишись на мой телеграм канал о маркетинге JenyaSegeda\n' \
                         f'2. Нажми кнопку "Проверить подписку" в боте.'

subscribed_message = f'Стикеры для сторис можно скачать по ссылке: \n' \
                     f'https://drive.google.com/drive/u/0/folders/15P5t8LhC_98iZpfbzmv61AL0AAxLSUnA\n' \
                     f'Если вы никогда раньше не пользовались стикерами в сторис, смотрите инструкцию на моем сайте: https://jenyasegeda.com/stikers '

@dp.message_handler(commands=['start', 'help'])
async def start(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=not_subscribed_message,
        reply_markup=subscription_check_keyboard
    )

@dp.message_handler()
async def check_subscription(message: Message):
    if message.text == 'Проверить подписку':
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        if chat_member['status'] != 'left':
            await bot.send_message(
                chat_id=message.from_user.id,
                text=subscribed_message,
                reply_markup=subscription_check_keyboard
            )
        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=not_subscribed_message,
                reply_markup=subscription_check_keyboard
            )


executor.start_webhook(
                    dispatcher=dp,
                    webhook_path='',
                    on_startup=on_startup,
                    on_shutdown=on_shutdown,
                    skip_updates=True,
                    host="0.0.0.0",
                    port=int(os.getenv("PORT", 5000))
)
