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
            if key in node and isinstance(node[key], str) and search_value.lower() in node[key].lower():
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

async def get_formatted_item(item: Dict) -> str:
    """
    Will format a JSON object into a pleasing format for Discord, including nested objects.

    Args:
        item (dict): The JSON object to format.

    Returns:
        str: A formatted string.
    """
    formatted_message = []

    def format_item(sub_item: Dict, level=0):
        for key, value in sub_item.items():
            if value:  # Check if the value is not None or empty
                if key == "id":
                    continue
                formatted_key = " ".join(word.capitalize() for word in key.split("_"))
                prefix = "> " if level > 0 else ""
                if isinstance(value, dict):
                    # Check if all values in the dictionary are zero
                    if all(v == 0 for v in value.values()):
                        continue
                    formatted_message.append(f"{prefix}**{formatted_key}:**")
                    format_item(value, level + 1)
                elif isinstance(value, list):
                    formatted_message.append(f"{prefix}**{formatted_key}:**")
                    for sub_item in value:
                        if isinstance(sub_item, dict):
                            format_item(sub_item, level + 1)
                        else:
                            formatted_message.append(f"{prefix} - {sub_item}")
                elif key == "wiki_link":
                    formatted_message.append(f"{prefix}**{formatted_key}:** <{value}>")
                else:
                    formatted_message.append(f"{prefix}**{formatted_key}:** {value}")

    format_item(item)

    if formatted_message:
        return "\n".join(formatted_message)
    return ""
