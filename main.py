import logging
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import os
import google.generativeai as genai
import asyncio

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

model = genai.GenerativeModel("gemini-1.5-flash")

@dp.message_handler(commands=['start', 'help'])
async def start_or_help_command(message: types.Message):
    if message.text == '/start':
        welcome_message = "Hello! I'm your bot. How can I assist you?"
    else:
        welcome_message = (
            "Hi There, I'm a Telegram bot created by Adithya! Please follow these commands - \n"
            "/start - to start the conversation\n"
            "/clear - to clear the past conversation and context.\n"
            "/help - to get this help menu.\n"
            "I hope this helps. :)"
        )
    await message.answer(welcome_message)

@dp.message_handler(commands=['clear'])
async def clear_command(message: types.Message):
    await message.answer("I've cleared the past conversation and context.")


@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    await async_prompt(message, user_input)

async def async_prompt(message: types.Message, user_input: str):
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        ]
    )
    response = chat.send_message(user_input)
    await message.answer(response.text)



async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())