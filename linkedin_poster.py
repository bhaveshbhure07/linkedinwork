import os
import asyncio
import requests
from pyrogram import Client
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random


# =========================
# CONFIG (GitHub Secrets)
# =========================

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
GROQ_KEY = os.environ.get("GROQ_API_KEY")
BOT_TOKEN = os.environ.get("LINKEDIN_BOT_TOKEN")
CHAT_ID = int(os.environ.get("PRIVATE_CHAT_ID"))


# =========================
# FETCH JOBS
# =========================

def fetch_jobs():

    url = "https://remotive.com/api/remote-jobs"

    try:

        response = requests.get(url, timeout=10)
        data = response.json()

        jobs = []

        for job in data["jobs"][:25]:

            jobs.append({
                "company": job["company_name"],
                "role": job["title"],
                "link": job["url"]
            })

        return jobs

    except:
        return []


# =========================
# SELECT BEST JOB
# =========================

def pick_best_job(jobs):

    big_companies = [
        "Google",
        "Amazon",
        "Microsoft",
        "Meta",
        "Apple",
        "Netflix",
        "Adobe",
        "Intel",
        "IBM"
    ]

    for job in jobs:

        if job["company"] in big_companies:

            return job

    if jobs:
        return random.choice(jobs)

    return {
        "company": "TCS",
        "role": "Software Developer",
        "link": "https://linkedin.com/jobs"
    }


# =========================
# AI CAPTION GENERATOR
# =========================

def generate_caption(company, role, link):

    client = Groq(api_key=GROQ_KEY)

    prompt = f"""
Write a VIRAL LinkedIn hiring post.

Company: {company}
Role: {role}

Rules:
Short hook line
Explain opportunity
Call to action: Comment INTERESTED

Add emojis.

Max 120 words.
"""

    chat = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return chat.choices[0].message.content


# =========================
# BANNER GENERATOR
# =========================

def create_banner(company, role):

    width = 1080
    height = 1080

    img = Image.new("RGB", (width, height), (20, 25, 35))

    draw = ImageDraw.Draw(img)

    try:
        font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 45)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    title = "WE ARE HIRING"

    role_text = textwrap.fill(role, width=18)

    draw.text((200, 200), title, fill="white", font=font_big)
    draw.text((200, 420), role_text, fill="cyan", font=font_small)
    draw.text((200, 720), company, fill="white", font=font_small)

    path = "linkedin_post.png"

    img.save(path)

    return path


# =========================
# TELEGRAM SEND
# =========================

async def send_to_telegram(image, caption):

    async with Client(
        "Awork_Bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    ) as app:

        await app.get_chat(CHAT_ID)

        await app.send_photo(
            chat_id=CHAT_ID,
            photo=image,
            caption=caption
        )

        print("✅ Post sent to Telegram")


# =========================
# MAIN PIPELINE
# =========================

async def main():

    if not all([API_ID, API_HASH, GROQ_KEY, BOT_TOKEN, CHAT_ID]):

        print("❌ Missing GitHub Secrets")
        return

    print("🚀 Fetching jobs...")

    jobs = fetch_jobs()

    job = pick_best_job(jobs)

    company = job["company"]
    role = job["role"]
    link = job["link"]

    print("🤖 Generating AI caption...")

    caption = generate_caption(company, role, link)

    print("🎨 Creating banner...")

    banner = create_banner(company, role)

    print("📤 Sending to Telegram...")

    await send_to_telegram(banner, caption)

    print("✅ Done!")


# =========================
if __name__ == "__main__":

    asyncio.run(main())
