import os
import asyncio
import logging
import discord
from discord.ext import commands
from config.settings import TOKEN, setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        logger.info("Logged in as %s", self.user.name)
        logger.info("Bot is ready")


async def load_cogs(my_bot):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog = filename[:-3]
            try:
                await my_bot.load_extension(f"cogs.{cog}")
                logger.info("Loaded cog: %s", cog)
            except discord.ext.commands.ExtensionAlreadyLoaded:
                logger.warning("Cog %s is already loaded.", cog)
            except discord.ext.commands.ExtensionNotFound:
                logger.error("Cog %s not found.", cog)
            except discord.ext.commands.ExtensionFailed as e:
                logger.error("Failed to load cog %s: %s", cog, e)


async def main():
    my_intents = discord.Intents.default()
    my_intents.messages = True
    my_intents.message_content = True  # Required for reading message content
    my_intents.members = True  # Ensure the members intent is enabled

    my_bot = MyBot(command_prefix="!", intents=my_intents)

    # Load all cogs
    await load_cogs(my_bot)

    # Start the bot
    await my_bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
