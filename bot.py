import os
import asyncio
import logging
import discord
from discord.ext import commands
from config.settings import TOKEN, setup_logging

# Create an instance of discord.Intents and set the required intents
intents = discord.Intents.default()  # This will enable the default intents

# If you need additional intents, enable them as follows:
intents.message_content = True  # Enable message content intent if your bot needs to read message content
intents.messages = True  # Ensure the bot has the messages intent enabled
intents.members = True  # Ensure the members intent is enabled

# Create an instance of commands.Bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)
# Set up logging
setup_logging()


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name}')
        logging.info('Bot is ready')


async def load_cogs(my_bot):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog = filename[:-3]
            try:
                await my_bot.load_extension(f'cogs.{cog}')
                logging.info('Loaded cog: %s', cog)
            except Exception as e:
                logging.error('Failed to load cog %s: %s', cog, e)


async def main():
    my_intents = discord.Intents.default()
    my_intents.messages = True
    my_intents.message_content = True  # Required for reading message content
    my_intents.members = True  # Ensure the members intent is enabled

    my_bot = MyBot(command_prefix='!', intents=my_intents)

    # Load all cogs
    await load_cogs(my_bot)

    # Start the bot
    await my_bot.start(TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
