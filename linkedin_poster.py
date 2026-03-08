import os
import asyncio
from pyrogram import Client
from groq import Groq
from PIL import Image

# Config - Direct values for testing (ya env se lo)
API_ID = int(os.environ.get('API_ID', 'YOUR_API_ID'))
API_HASH = os.environ.get('API_HASH', 'YOUR_API_HASH')
GROQ_KEY = os.environ.get('GROQ_API_KEY', 'YOUR_GROQ_KEY')
BOT_TOKEN = os.environ.get('LINKEDIN_BOT_TOKEN', 'YOUR_NEW_BOT_TOKEN') # Naya wala token!
CHAT_ID = -1003422278522  # Tumhara verified ID

async def main():
    if not all([API_ID, API_HASH, GROQ_KEY, BOT_TOKEN]):
        print("❌ Error: Secrets/Token missing!")
        return

    # Groq Logic (Llama 3.3)
    client = Groq(api_key=GROQ_KEY)
    company, role, batch = "TCS", "Software Developer", "2025-2027"
    
    prompt = f"Write a professional LinkedIn post for {company} hiring {role} for {batch}. Use the 🚨 format with emojis."

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        caption = chat_completion.choices[0].message.content
        
        # Image creation
        img = Image.new('RGB', (1080, 1350), color=(210, 180, 140))
        img.save("linkedin_post.png")

        # Pyrogram Client
        async with Client("Awork_LinkedIn", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
            print("🔗 Connecting to peer...")
            # CRITICAL FIX: Pehle chat ko resolve karo
            await app.get_chat(CHAT_ID) 
            
            await app.send_photo(
                chat_id=CHAT_ID, 
                photo="linkedin_post.png", 
                caption=caption
            )
            print("🚀 Success! Post sent to Private Group.")
            
    except Exception as e:
        print(f"⚠️ Error: {e}")
        print("💡 Tip: Agar abhi bhi error aaye, toh 'Awork_LinkedIn.session' file delete karke restart karo.")

if __name__ == "__main__":
    asyncio.run(main())
        
