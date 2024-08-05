# Discord - VerranBot
This bot allows discord users to retrieve results from the Verran Codex API (https://verrancodex.com/documentation).

## Requirements
- Built with Python 3.12 - should work with 3.x
- See requirements.txt for a list of Python packages required to run/built/test the bot.

## How to run
The easiest way is checkout the source code from GitHub (https://github.com/tabmowtez/VerranBot).
You will need 4 main environment variables (.env files supported):
- DISCORD_TOKEN - Taken from Discord Developer Portal
- VERRAN_CODEX_API_KEY - Generated from https://verrancodex.com/ 
- LOG_LEVEL - Defaults to INFO - set to DEBUG if you are encountering issues
- CACHE_DURATION - Defaults to 60 (minutes), the amount of time the Verran Codex API calls are cached

Then you can either:
- Run directly via Python
    ```
    pip install -r requirements.txt
    python bot.py
    ```
- Run in a container
  - Docker
    ```
    docker build -t my-image-name .
    docker run -d --name my-container-name my-image-name
    ```
  - Docker Compose (recommended)
    ```
    docker compose up -d
    ```

## Functionality
Each Verran Codex API is implemented - See [List of Bot @commands here](cogs/verran_codex.py) 
