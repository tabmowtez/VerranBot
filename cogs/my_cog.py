import requests
import logging
from discord.ext import commands
from api.api_client import ApiClient
from utils.helpers import find_json_nodes, send_formatted_items

# Configure logging
logger = logging.getLogger(__name__)


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_client = ApiClient()
        logger.debug('%s initialised.', __name__)

    @commands.command(name='armor')
    async def get_data(self, ctx, *, args=None):
        if args is None:
            await ctx.send('I need a name of the armor to search for!')
            return
        logger.debug('In armor command')
        try:
            data = self.api_client.get_data()
            logger.debug('Data is: %s', data)
            result = await find_json_nodes(data, 'name', args)
            logger.debug('Result is: %s', result)
            await send_formatted_items(ctx, result)
        except requests.RequestException as e:
            await ctx.send(f'Failed to get data: {e}')

    @commands.command(name='owner')
    async def owner(self, ctx):
        logger.debug('In owner command')
        try:
            # Get the guild (server) from the context
            guild = ctx.guild

            if guild:
                # Access the owner attribute
                guild_owner = guild.owner
                if guild_owner:
                    await ctx.send(
                        f'The owner of this server is '
                        f'{guild_owner.name}{f"#{guild_owner.discriminator}" if guild_owner.discriminator != "0" else ""}')
                else:
                    await ctx.send('Could not retrieve the owner information. The owner attribute is None.')
            else:
                await ctx.send('This command can only be used in a server.')
        except Exception as e:
            await ctx.send(f'An error occurred: {e}')
            raise e


async def setup(bot):
    logger.debug('Setting up %s.', __name__)
    await bot.add_cog(MyCog(bot))
    logger.debug('%s has been added to the bot.', __name__)
