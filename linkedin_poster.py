import os
import asyncio
from pyrogram import Client
from groq import Groq
from PIL import Image, ImageDraw

# Config
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
GROQ_KEY = os.environ.get('GROQ_API_KEY')
BOT_TOKEN = os.environ.get('LINKEDIN_BOT_TOKEN')
CHAT_ID = -1003422278522 # Verified Private Group ID

async def main():
    if not all([API_ID, API_HASH, GROQ_KEY, BOT_TOKEN]):
        print("❌ Error: Secrets missing in GitHub Settings!")
        return

    client = Groq(api_key=GROQ_KEY)
    company, role, batch = "TCS", "Software Developer", "2025-2027"
    
    prompt = f"Write a professional LinkedIn post for {company} hiring {role} for {batch}. Use 🚨 emojis, bullet points, and a clear 'Apply Link' placeholder."

    try:
        # 1. Groq se Caption generate karna
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        caption = chat_completion.choices[0].message.content
        
        # 2. Image create karna
        img = Image.new('RGB', (1080, 1350), color=(210, 180, 140))
        img.save("linkedin_post.png")

        # 3. Telegram Send (Pyrogram)
        async with Client("Awork_Session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
            print("🔗 Connecting and resolving peer...")
            
            try:
                # Peer resolve karna compulsory hai GitHub Actions ke liye
                peer = await app.get_chat(CHAT_ID)
                print(f"✅ Group found: {peer.title}")
                
                # Chhota pause connection stabilize karne ke liye
                await asyncio.sleep(3)

                # Ab photo bhejo (Only ONE time)
                await app.send_photo(
                    chat_id=peer.id, 
                    photo="linkedin_post.png", 
                    caption=caption
                )
                print("🚀 Success! Message sent to Group.")

            except Exception as e:
                print(f"❌ Telegram Error: {e}")
                print("💡 Tip: Bot ko group mein Admin banao aur 'Send Media' permission check karo.")
            
    except Exception as e:
        print(f"⚠️ Overall Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    
