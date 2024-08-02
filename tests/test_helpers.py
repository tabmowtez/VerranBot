import json
import pytest
from utils.helpers import find_json_nodes, get_formatted_item


def create_sample_json():
    """Create a sample JSON structure for testing."""
    return {
        "items": [
            {"name": "Sword", "cost": "100", "is_cosmetic": "No", "obtain": "Shop", "primary_attribute": "Strength",
             "rarity": "Rare", "slot": "Hand", "wiki_link": "https://example.com/sword"},
            {"name": "Shield", "cost": "150", "is_cosmetic": "Yes", "obtain": "Dungeon", "primary_attribute": "Defense",
             "rarity": "Uncommon", "slot": "Arm", "wiki_link": "https://example.com/shield"}
        ]
    }


@pytest.mark.asyncio
class TestHelperFunctions:

    @pytest.mark.asyncio
    async def test_find_json_nodes(self):
        json_response = create_sample_json()
        search_value = "Sword"
        key = "name"
        result = await find_json_nodes(json_response, key, search_value)
        assert len(result) == 1
        assert result[0]['name'] == "Sword"

    @pytest.mark.asyncio
    async def test_find_json_nodes_with_string_input(self):
        json_response = json.dumps(create_sample_json())
        search_value = "Shield"
        key = "name"
        result = await find_json_nodes(json_response, key, search_value)
        assert len(result) == 1
        assert result[0]['name'] == "Shield"

    @pytest.mark.asyncio
    async def test_find_json_nodes_no_match(self):
        json_response = create_sample_json()
        search_value = "Helmet"
        key = "name"
        result = await find_json_nodes(json_response, key, search_value)
        assert not result

    @pytest.mark.asyncio
    async def test_get_formatted_item(self):
        item = {"name": "Sword", "cost": "100", "is_cosmetic": "No", "obtain": "Shop", "primary_attribute": "Strength",
                "rarity": "Rare", "slot": "Hand", "wiki_link": "https://example.com/sword"}
        expected_message = (
            "**Name:** Sword\n"
            "**Cost:** 100\n"
            "**Cosmetic:** No\n"
            "**Obtain:** Shop\n"
            "**Primary Attribute:** Strength\n"
            "**Rarity:** Rare\n"
            "**Slot:** Hand\n"
            "**Wiki Link:** <https://example.com/sword>"
        )
        result = await get_formatted_item(item)
        assert result == expected_message
