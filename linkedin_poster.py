import os
import asyncio
from pyrogram import Client
from google import genai
from PIL import Image, ImageDraw

# --- Config Handling ---
def get_env(name):
    val = os.environ.get(name, '').strip()
    if not val:
        print(f"❌ Error: Secret {name} is missing or empty!")
    return val

try:
    API_ID = int(get_env('API_ID'))
    API_HASH = get_env('API_HASH')
    GEMINI_KEY = get_env('GEMINI_API_KEY')
    BOT_TOKEN = get_env('LINKEDIN_BOT_TOKEN')
    CHAT_ID = get_env('PRIVATE_CHAT_ID')
except Exception as e:
    print(f"❌ Config Error: {e}")
    exit(1)

# AI Setup (New Library)
client = genai.Client(api_key=GEMINI_KEY)

def create_job_image(company, role, batch):
    # Pin-board style template (Simple version)
    img = Image.new('RGB', (1080, 1350), color=(210, 180, 140))
    d = ImageDraw.Draw(img)
    d.rectangle([50, 50, 1030, 1300], fill=(255, 255, 255))
    d.text((100, 150), f"{company} IS HIRING!", fill=(81, 45, 168))
    d.text((100, 300), f"Role: {role}", fill=(0, 0, 0))
    d.text((100, 450), f"Batch: {batch}", fill=(0, 0, 0))
    path = "linkedin_post.png"
    img.save(path)
    return path

async def main():
    # Dummy data for Big Tech check
    company = "TCS" 
    role = "Software Developer"
    batch = "2024-2026"

    # Caption Generator with your prompt
    prompt = f"Generate a high-CTR LinkedIn caption for {company} {role} {batch} using the exact 🚨 format I provided."
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    
    img_path = create_job_image(company, role, batch)

    async with Client("Awork_LinkedIn", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
        await app.send_photo(chat_id=CHAT_ID, photo=img_path, caption=response.text)
        print("🚀 Success! Draft sent to private group.")

if __name__ == "__main__":
    asyncio.run(main())
