import os
import asyncio
from pyrogram import Client
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont

# --- Config ---
BIG_TECH = ["Google", "Microsoft", "Amazon", "TCS", "Infosys", "Wipro", "Meta", "Apple", "Netflix", "Adobe", "Salesforce"]
BOT_TOKEN = os.environ.get('LINKEDIN_BOT_TOKEN')
CHAT_ID = os.environ.get('PRIVATE_CHAT_ID')
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# --- Image Generator (Pin-board Template Logic) ---
def create_job_image(company, role, batch):
    # Main blank template generate kar raha hoon (1080x1620 for LinkedIn Portrait)
    img = Image.new('RGB', (1080, 1620), color=(210, 180, 140)) # Wood/Cork color
    d = ImageDraw.Draw(img)
    
    # Simple Rectangle for Paper
    d.rectangle([100, 100, 980, 1500], fill=(245, 245, 245), outline=(200, 200, 200))
    
    # Text Placement (Basic)
    d.text((150, 200), f"{company} IS HIRING!", fill=(81, 45, 168)) # Purple color like your image
    d.text((150, 400), f"ROLE: {role}", fill=(0, 0, 0))
    d.text((150, 600), f"BATCH: {batch}", fill=(0, 0, 0))
    d.text((150, 1300), "Comment 'INTERESTED' for Apply Link", fill=(255, 0, 0))
    
    path = "linkedin_post.png"
    img.save(path)
    return path

async def main():
    # 1. Scanning (Using your Telegram source logic but filtering Big Tech)
    # [Yahan wahi scan logic aayega jo pehle tha, par hum sirf BIG_TECH match karenge]
    
    # Example logic for one post
    company = "TCS" # Ye scan se aayega
    if company in BIG_TECH:
        role = "Software Developer"
        batch = "2024-2026"
        
        # 2. Caption Generator (Your 50K Strategy Prompt)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Generate LinkedIn caption for {company}, {role}, {batch}. Use the exact format: 🚨 [Company] Hiring... [Your Provided Format]"
        response = model.generate_content(prompt)
        
        # 3. Create Image
        img_path = create_job_image(company, role, batch)
        
        # 4. Send to Private Telegram Group
        async with Client("Awork_Private", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
            await app.send_photo(chat_id=CHAT_ID, photo=img_path, caption=response.text)
            print("✅ Bhavesh, LinkedIn Draft bhej diya hai!")

if __name__ == "__main__":
    asyncio.run(main())
