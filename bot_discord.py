
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import discord
from discord import Intents
import asyncio

# Configuration Discord
TOKEN = ''
GUILD_ID = ''
CHANNEL_ID = ''

def find_links_with_word(url, words):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links_with_word = []
    stage_links = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)  # Join base URL with relative URL
            link_text = link.text.lower()
            if any(re.search(r'\b' + re.escape(word.lower()) + r'\b', full_url.lower()) or re.search(r'\b' + re.escape(word.lower()) + r'\b', link_text) for word in words):
                if 'stage' in link_text:
                    stage_links.append(full_url)
                else:
                    links_with_word.append(full_url)

    return links_with_word, stage_links

async def post_announcements(links):
    intents = Intents.default()
    intents.typing = False
    intents.presences = False
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        guild = bot.get_guild(int(GUILD_ID))
        channel = await guild.fetch_channel(int(CHANNEL_ID))
        if channel is not None:
            for link in links:
                await channel.send(link)

        await bot.close()

    await bot.start(TOKEN)

async def main():
    url = "https://emploi.afjv.com/index.php"
    words = ["unity", "unity3d", "Unity", "Unity3D"]
    links, stage_links = find_links_with_word(url, words)

    # Tri des liens par ordre décroissant de date
    links_sorted = sorted(links, key=lambda x: x.split("/")[-1], reverse=True)

    for link in links_sorted:
        print(link)

    await post_announcements(links_sorted)

# Exécution de la fonction principale asynchrone avec asyncio.run()
asyncio.run(main())




