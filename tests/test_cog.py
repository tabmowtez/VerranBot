import pytest
import discord
from discord.ext import commands
from unittest.mock import patch, AsyncMock
from cogs.my_cog import MyCog


# Fixture to set up a bot instance for testing
@pytest.fixture
def bot():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)
    return bot


# MockApiClient for use in the test
class MockApiClient:
    def get_data(self):
        return {"mock_key": "mock_value"}


# Helper function to create a mock context
async def get_context(bot, *, prefix, command_name):
    message = discord.Message(state=None, channel=None, data={'id': 123456789, 'content': f'{prefix}{command_name}'})
    ctx = commands.Context(prefix=prefix, message=message, bot=bot, view=commands.view.StringView(message.content))
    ctx.send = AsyncMock()
    return ctx


# Test the get_data command
@pytest.mark.asyncio
async def test_get_data(bot):
    # Mock the API client
    with patch('api.api_client.ApiClient', new_callable=lambda: MockApiClient):
        # Load the cog with the mocked API client
        await bot.add_cog(MyCog(bot))

        # Create a mock context
        ctx = await get_context(bot, prefix="!", command_name="get_data")

        # Invoke the command
        command = bot.get_command("get_data")
        await command.invoke(ctx)

        # Check that the bot sent the expected message
        ctx.send.assert_called_once_with('Data: {"mock_key": "mock_value"}')
