import discord
from discord.ext import commands
import openai
import alpaca_trade_api as tradeapi
import os

# Load your API keys
DISCORD_BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
ALPACA_API_KEY = "YOUR_ALPACA_API_KEY"
ALPACA_SECRET_KEY = "YOUR_ALPACA_SECRET_KEY"
TARGET_CHANNEL_ID = 123456789012345678  # Replace with the actual channel ID

# Initialize APIs
openai.api_key = OPENAI_API_KEY
alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url="https://paper-api.alpaca.markets")

# Set up Discord bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Required for reading messages
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def trade(ctx, *, command: str):
    """Handles trade commands only from the specified channel."""
    if ctx.channel.id != TARGET_CHANNEL_ID:
        return  # Ignore messages from other channels

    await ctx.send(f"Processing trade: `{command}`...")

    # Generate trading code with GPT
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a Python trading bot."},
                  {"role": "user", "content": f"Generate Python code to execute: {command}"}]
    )
    
    generated_code = response["choices"][0]["message"]["content"]

    # Execute the generated code (⚠️ Validate first!)
    try:
        exec(generated_code, globals())  # Be careful running this!
        await ctx.send(f"Trade executed: `{command}`")
    except Exception as e:
        await ctx.send(f"Error executing trade: {e}")

bot.run(DISCORD_BOT_TOKEN)
