import os
import asyncio
from pyrogram import Client
from groq import Groq
from PIL import Image, ImageDraw, ImageFont

# Config
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
GROQ_KEY = os.environ.get('GROQ_API_KEY')
BOT_TOKEN = os.environ.get('LINKEDIN_BOT_TOKEN')
CHAT_ID = -1003422278522 # Tera Private Group ID

async def main():
    # Groq setup for Caption
    client = Groq(api_key=GROQ_KEY)
    company, role, batch = "TCS", "Software Developer", "2025-2027"
    
    # Tera High-CTR Format
    prompt = f"Write a professional LinkedIn post for {company} hiring {role} for {batch}. Use 🚨 emojis, bullet points, and a clear 'Apply Link' placeholder. Keep it catchy for students."

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        caption = chat_completion.choices[0].message.content
        
        # Image Creation (Jo tune format manga tha)
        img = Image.new('RGB', (1080, 1350), color=(210, 180, 140)) # Corkboard color
        d = ImageDraw.Draw(img)
        # Yahan tum chaho toh d.text use karke image pe job title likh sakte ho
        img.save("linkedin_post.png")

        # Telegram Send
        async with Client("Awork_Session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
            print("🔗 Connecting to Private Group...")
            await asyncio.sleep(2) # Connection stabilize hone do
            
            # Message bhejna
            await app.send_photo(
                chat_id=CHAT_ID,
                photo="linkedin_post.png",
                caption=caption
            )
            print("🚀 Success! Check your Telegram Group.")
            
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    
