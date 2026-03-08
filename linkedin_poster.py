import os
import asyncio
from pyrogram import Client
from groq import Groq
from PIL import Image, ImageDraw

# Config
def get_env(name):
    return os.environ.get(name, '').strip()

API_ID = int(get_env('API_ID')) if get_env('API_ID') else None
API_HASH = get_env('API_HASH')
GROQ_KEY = get_env('GROQ_API_KEY')
BOT_TOKEN = get_env('LINKEDIN_BOT_TOKEN')
CHAT_ID = get_env('PRIVATE_CHAT_ID')

async def main():
    if not all([API_ID, API_HASH, GROQ_KEY]):
        print("❌ Error: Secrets missing!")
        return

    client = Groq(api_key=GROQ_KEY)
    company, role, batch = "TCS", "Software Developer", "2025-2027"
    
    # High-CTR Prompt
    prompt = f"Write a professional LinkedIn post for {company} hiring {role} for {batch}. Use the 🚨 format with emojis."

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
        )
        caption = chat_completion.choices[0].message.content
        
        # Image Logic (Corkboard style)
        img = Image.new('RGB', (1080, 1350), color=(210, 180, 140))
        img.save("linkedin_post.png")

        async with Client("Awork_LinkedIn", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
            await app.send_photo(chat_id=CHAT_ID, photo="linkedin_post.png", caption=caption)
            print("🚀 Success! Draft sent via Groq.")
            
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    
