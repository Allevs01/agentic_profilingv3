import discord
from discord.ext import commands
 
# ====== CONFIG ======
TOKEN = "MTQ1NjkyOTcyMDg3MTQyMDAzOQ.GFSxZH.N4IMKPoJEgaM8_ch23RRR5J3L9RKvTFjvDgKeA"
CHANNEL_ID = 1442860143061762152  # ID del canale
# ====================
 
intents = discord.Intents.default()
intents.message_content = True
 
bot = commands.Bot(command_prefix="!", intents=intents)
 
@bot.event
async def on_ready():
    print(f"Connesso come {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
 
    if channel is None:
        print("Canale non trovato")
        await bot.close()
        return
 
    deleted = 0
 
    async for message in channel.history(limit=None):
        try:
            await message.delete()
            deleted += 1
        except discord.Forbidden:
            print("Permessi insufficienti")
            break
        except discord.HTTPException as e:
            print(f"Errore: {e}")
 
    print(f"Messaggi cancellati: {deleted}")
    await bot.close()
 
bot.run(TOKEN)
 