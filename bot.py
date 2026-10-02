import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from rag import get_rag_answer

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class SynaptoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # This registers your slash commands with Discord — required once per change
        await self.tree.sync()

bot = SynaptoBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="ask", description="Ask a question about SynaptoFlow")
@app_commands.describe(question="Your question about the project")
async def ask(interaction: discord.Interaction, question: str):
    # defer() tells Discord "I got it, still working" — RAG calls take a couple seconds,
    # and without this Discord will show the command as failed after 3 seconds
    await interaction.response.defer()
    answer = get_rag_answer(question)
    await interaction.followup.send(answer)

bot.run(os.environ["DISCORD_BOT_TOKEN"])