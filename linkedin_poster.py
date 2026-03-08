import os
import asyncio
from pyrogram import Client
from groq import Groq # Gemini ki jagah Groq
from PIL import Image, ImageDraw

def get_env(name):
    return os.environ.get(name, '').strip()

# Configuration
API_ID = int(get_env('API_ID')) if get_env('API_ID') else None
API_HASH = get_env('API_HASH')
GROQ_KEY = get_env('GROQ_API_KEY')
BOT_TOKEN = get_env('LINKEDIN_BOT_TOKEN')
CHAT_ID = get_env('PRIVATE_CHAT_ID')

async def main():
    if not all([API_ID, API_HASH, GROQ_KEY]):
        print("❌ Error: Missing Secrets in GitHub!")
        return

    # Groq Setup
    client = Groq(api_key=GROQ_KEY)
    
    # Job Details (Testing TCS)
    company, role, batch = "TCS", "Software Developer", "2024-2026"

    # Your Proven 50K Strategy Prompt
    prompt = f"Generate a high-CTR LinkedIn post for {company} hiring {role} for {batch}. Use the 🚨 format exactly."

    try:
        # Groq Model: Llama-3-70b (Bahut powerful model hai)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
        )
        caption = chat_completion.choices[0].message.content
        
        # Image Generation (Same Pin-board Style)
        img = Image.new('RGB', (1080, 1350), color=(210, 180, 140))
        d = ImageDraw.Draw(img)
        d.rectangle([50, 50, 1030, 1300], fill=(255, 255, 255))
        d.text((100, 200), f"{company} IS HIRING", fill=(81, 45, 168))
        
        img_path = "linkedin_post.png"
        img.save(img_path)

        async with Client("Awork_LinkedIn", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
            await app.send_photo(chat_id=CHAT_ID, photo=img_path, caption=caption)
            print("🚀 Success! Draft sent via Groq API.")
            
    except Exception as e:
        print(f"⚠️ Groq Process Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
