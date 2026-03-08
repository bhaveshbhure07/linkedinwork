import os
import asyncio
from pyrogram import Client
from google import genai
from PIL import Image, ImageDraw

# --- Config Handling ---
def get_env(name):
    return os.environ.get(name, '').strip()

API_ID = int(get_env('API_ID')) if get_env('API_ID') else None
API_HASH = get_env('API_HASH')
GEMINI_KEY = get_env('GEMINI_API_KEY')
BOT_TOKEN = get_env('LINKEDIN_BOT_TOKEN')
CHAT_ID = get_env('PRIVATE_CHAT_ID')

async def main():
    if not all([API_ID, API_HASH, GEMINI_KEY]):
        print("❌ Error: Missing Secrets in GitHub!")
        return

    client = genai.Client(api_key=GEMINI_KEY)
    
    # Example Job for Testing
    company, role, batch = "TCS", "Software Developer", "2024-2026"

    # Your Proven 50K Strategy Prompt
    prompt = f"Write a LinkedIn post for {company} hiring {role} for {batch}. Use the 🚨 format exactly."
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    
    # Image logic (Simple pin-board style)
    img = Image.new('RGB', (1080, 1350), color=(210, 180, 140))
    img.save("linkedin_post.png")

    async with Client("Awork_LinkedIn", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
        await app.send_photo(chat_id=CHAT_ID, photo="linkedin_post.png", caption=response.text)
        print("🚀 Success! Check your private Telegram group.")

if __name__ == "__main__":
    asyncio.run(main())
