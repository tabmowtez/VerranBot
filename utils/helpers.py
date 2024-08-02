import json
from typing import Union, List, Dict


async def find_json_nodes(json_response: Union[str, Dict, list], key: str, search_value: str) -> List[Dict]:
    """
    Search for nodes in a JSON response where the specified key contains a specific substring and return those nodes

    Args:
        json_response (list): The JSON response to parse.
        key (str): The key to search for.
        search_value (str): The substring to search for in the specified key's value.

    Returns:
        list: A list of nodes (dictionaries) where the specified key contains the given substring.
    """
    # If json_response is a string, parse it to a Python dictionary
    if isinstance(json_response, str):
        json_response = json.loads(json_response)

    # Initialize an empty list to store the nodes
    nodes = []

    # Define a recursive function to traverse the JSON tree
    def traverse(node):
        if isinstance(node, dict):
            # Check if the specified key exists and if its value contains the search_value
            if key in node and isinstance(node[key], str) and search_value in node[key]:
                nodes.append(node)
            # Continue traversing child nodes
            for child in node.values():
                traverse(child)
        elif isinstance(node, list):
            # Continue traversing each item in the list
            for item in node:
                traverse(item)

    # Start traversing the JSON tree
    traverse(json_response)

    # Return the list of nodes
    return nodes


async def get_formatted_item(item: [Dict]):
    """
    Will format a json object into a pleasing format for Discord

    Args:
        item (str or dict): The JSON string to format

    Returns:
        list: A formatted string.
    """
    # Create a formatted string for each item
    formatted_message = []

    if item.get('name'):
        formatted_message.append(f"**Name:** {item.get('name')}")
    if item.get('cost'):
        formatted_message.append(f"**Cost:** {item.get('cost')}")
    if item.get('is_cosmetic'):
        formatted_message.append(f"**Cosmetic:** {item.get('is_cosmetic')}")
    if item.get('obtain'):
        formatted_message.append(f"**Obtain:** {item.get('obtain')}")
    if item.get('primary_attribute'):
        formatted_message.append(f"**Primary Attribute:** {item.get('primary_attribute')}")
    if item.get('rarity'):
        formatted_message.append(f"**Rarity:** {item.get('rarity')}")
    if item.get('slot'):
        formatted_message.append(f"**Slot:** {item.get('slot')}")
    if item.get('wiki_link'):
        formatted_message.append(f"**Wiki Link:** <{item.get('wiki_link')}>")

    # Join the formatted message parts and send if not empty
    if formatted_message:
        return '\n'.join(formatted_message)
