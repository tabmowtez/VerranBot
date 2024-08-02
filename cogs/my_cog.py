import logging
import requests
from discord.ext import commands

from api.api_client import ApiClient
from utils.helpers import find_json_nodes, get_formatted_item

# Configure logging
logger = logging.getLogger(__name__)


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_client = ApiClient()
        logger.debug('%s initialised.', __name__)

    @commands.command(name='armor')
    async def get_data(self, ctx, *, args=None):
        # Get the username of the user who sent the command
        user_name = ctx.author.name
        logger.debug('armor command requested by: %s', user_name)

        if args is None:
            await ctx.reply('I need a name of the armor to search for!')
            return
        try:
            data = self.api_client.get_data('armors')
            logger.debug('Data is: %s', data)
            search_results = await find_json_nodes(data, 'name', args)
            logger.debug('Result is: %s', search_results)
            await ctx.reply(f'There are {len(search_results)} results')
            for item in search_results:
                await ctx.reply(await get_formatted_item(item))
        except requests.RequestException as e:
            await ctx.reply(f'Failed to get data: {e}')

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
                        f'The owner of this server is {guild_owner.name}'
                        f'#{guild_owner.discriminator}' if guild_owner.discriminator != "0" else ''
                    )

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
