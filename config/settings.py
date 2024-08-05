import os
import logging
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("VERRAN_CODEX_API_KEY")
CACHE_DURATION = os.getenv("CACHE_DURATION", 60)

# Set up logging
# Get the logging level from the environment variable
log_level = os.getenv("LOG_LEVEL", "INFO")

# Map environment variable to logging level
logging_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


def setup_logging():
    logging.basicConfig(level=logging_levels.get(log_level, logging.INFO),  # Capture all levels of log messages
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        handlers=[
                            logging.FileHandler("bot.log", encoding="utf-8"),  # Log messages to a file
                            logging.StreamHandler()  # Also log messages to the console
                        ])


logger = logging.getLogger(__name__)
