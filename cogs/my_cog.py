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
        logger.debug("%s initialised.", __name__)

    @commands.command(name="armors")
    async def armors(self, ctx, *, args=None):
        await self.search_for_item(ctx, "armors", args)

    @commands.command(name="biomes")
    async def biomes(self, ctx, *, args=None):
        await self.search_for_item(ctx, "biomes", args)

    @commands.command(name="bosses")
    async def bosses(self, ctx, *, args=None):
        await self.search_for_item(ctx, "bosses", args)

    @commands.command(name="buildings")
    async def buildings(self, ctx, *, args=None):
        await self.search_for_item(ctx, "node_buildings", args)

    @commands.command(name="commodities")
    async def commodities(self, ctx, *, args=None):
        await self.search_for_item(ctx, "node_commodities", args)

    @commands.command(name="dungeons")
    async def dungeons(self, ctx, *, args=None):
        await self.search_for_item(ctx, "dungeons", args)

    @commands.command(name="guilds")
    async def guilds(self, ctx, *, args=None):
        await self.search_for_item(ctx, "guilds", args)

    @commands.command(name="mats")
    async def mats(self, ctx, *, args=None):
        await self.search_for_item(ctx, "crafting_materials", args)

    @commands.command(name="mounts")
    async def mounts(self, ctx, *, args=None):
        await self.search_for_item(ctx, "mounts", args)

    @commands.command(name="mobs")
    async def mobs(self, ctx, *, args=None):
        await self.search_for_item(ctx, "mobs", args)

    @commands.command(name="nodes")
    async def nodes(self, ctx, *, args=None):
        await self.search_for_item(ctx, "nodes", args)

    @commands.command(name="pets")
    async def pets(self, ctx, *, args=None):
        await self.search_for_item(ctx, "pets", args)

    @commands.command(name="quests")
    async def quests(self, ctx, *, args=None):
        await self.search_for_item(ctx, "quests", args)

    @commands.command(name="resources")
    async def resources(self, ctx, *, args=None):
        await self.search_for_item(ctx, "resources", args)

    @commands.command(name="story")
    async def story(self, ctx, *, args=None):
        await self.search_for_item(ctx, "story_arcs", args)

    @commands.command(name="tools")
    async def tools(self, ctx, *, args=None):
        await self.search_for_item(ctx, "tools", args)

    @commands.command(name="weapons")
    async def weapons(self, ctx, *, args=None):
        await self.search_for_item(ctx, "weapons", args)

    @commands.command(name="owner")
    async def owner(self, ctx):
        # Get the username of the user who sent the command
        user_name = ctx.author.name
        logger.debug("Owner command requested by: %s", user_name)
        try:
            # Get the guild (server) from the context
            guild = ctx.guild

            if guild:
                # Access the owner attribute
                guild_owner = guild.owner
                if guild_owner:
                    await ctx.send(
                        f"The owner of this server is {guild_owner.name}"
                        f"#{guild_owner.discriminator}" if guild_owner.discriminator != "0" else ""
                    )

                else:
                    await ctx.send("Could not retrieve the owner information. The owner attribute is None.")
            else:
                await ctx.send("This command can only be used in a server.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            raise e

    async def search_for_item(self, ctx, item_type, args):
        user_name = ctx.author.name
        logger.debug(f"{item_type.capitalize()} command requested by: %s", user_name)

        if args is None:
            await ctx.reply(f"I need a name of the {item_type} to search for!")
            return

        try:
            data = await self.api_client.fetch_data_with_cache(item_type)
            logger.debug("Data is: %s", data)
            search_results = await find_json_nodes(data, "name", args)
            logger.debug("Result is: %s", search_results)
            await ctx.reply(f"There are {len(search_results)} results")
            for item in search_results:
                await ctx.reply(await get_formatted_item(item))
        except requests.RequestException as e:
            await ctx.reply(f"Failed to get data: {e}")


async def setup(bot):
    logger.debug("Setting up %s.", __name__)
    await bot.add_cog(MyCog(bot))
    logger.debug("%s has been added to the bot.", __name__)
