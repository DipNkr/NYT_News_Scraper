# config.py

# Standard library imports
import os

# Local imports
from .imports import logging
from src.imports import load_dotenv

class Config:
    """
    A class to manage configuration settings for the news scraper.

    Attributes:
        None
    """

    @staticmethod
    def load():
        """
        Loads the configuration settings from environment variables.

        Returns:
            dict: A dictionary containing the configuration settings.
        """
        try:
            return {
                "SEARCH_PHRASE": os.getenv("SEARCH_PHRASE"),
                "NEWS_SECTION": os.getenv("NEWS_SECTION"),
                "MONTHS": os.getenv("MONTHS"),
                "SENDER_EMAIL": os.getenv("SENDER_EMAIL"),
                "SENDER_PASSWORD": os.getenv("SENDER_PASSWORD"),
                "RECEIVER_EMAIL": os.getenv("RECEIVER_EMAIL")
            }
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            raise
