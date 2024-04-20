import datetime
from src.config import Config
from src.nyt_scraper import NYTScraper
from src.google_sheets_manager import GoogleSheetsManager
from src.email_sender import EmailSender
from src.imports import load_dotenv, logging

# Load environment variables from .env file
load_dotenv()

# Configure logging level
logging.basicConfig(level=logging.INFO)


def calculate_date_range(months):
    """
    Calculate the start and end date based on the given number of months.

    Args:
        months (int): Number of months to consider.

    Returns:
        tuple: Start date and end date in '%m/%d/%Y' format.
    """
    try:
        today = datetime.datetime.now()
        ist = today + datetime.timedelta(hours=5, minutes=30)  # Convert to IST

        # Calculate start date
        start_date = ist.replace(day=1) - datetime.timedelta(days=30 * (months - 1))

        # If start_date is in the future, set it to the 1st day of the current month
        if start_date > ist:
            start_date = ist.replace(day=1)

        # End date is the current date
        end_date = ist
        return start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')

    except Exception as e:
        logging.error(f"Error calculating date range: {e}")
        raise


def main():
    """
    Main function to execute the NYT News Scraper and Email Sender.

    Raises:
        Exception: If any error occurs during the execution.
    """
    try:
        # Load configuration from .env file
        config = Config.load()

        # Initialize NYTScraper
        scraper = NYTScraper()

        # Extract parameters from config
        search_phrase = config["SEARCH_PHRASE"]
        news_section = config["NEWS_SECTION"]
        months = int(config["MONTHS"])

        # Calculate start and end dates
        start_date, end_date = calculate_date_range(months)

        # Search news
        scraper.search_news(search_phrase, news_section, start_date, end_date)

        # Scrape articles
        articles = scraper.scrape_articles()

        # Initialize GoogleSheetsManager
        gs_manager = GoogleSheetsManager()

        # Add articles into spreadsheet
        sheet_link = gs_manager.append_data(articles)

        # Close the scraper
        scraper.close()

        # Extract email parameters
        sender_email = config["SENDER_EMAIL"]
        app_password = config["SENDER_PASSWORD"]
        receiver_email = config["RECEIVER_EMAIL"]

        # Send email
        EmailSender.send_email(sender_email, receiver_email, app_password, sheet_link)

    except Exception as e:
        logging.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
