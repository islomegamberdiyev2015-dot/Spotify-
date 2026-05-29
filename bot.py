import os
import glob
import asyncio
import subprocess

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Spotify link yuboring 🎵")

@dp.message()
async def download_song(message: types.Message):
    url = message.text

    if "spotify.com" not in url:
        await message.answer("Spotify link yuboring.")
        return

    msg = await message.answer("⬇️ Yuklanmoqda...")

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: subprocess.run(["spotdl", url, "--output", "."], capture_output=True)
    )

    files = glob.glob("*.mp3")
    if files:
        audio = FSInputFile(files[0])
        await msg.delete()
        await message.answer_audio(audio)
        os.remove(files[0])
    else:
        await msg.edit_text("❌ Xato yuz berdi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
