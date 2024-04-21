from datetime import datetime
from src.config import Config
from src.nyt_scraper import NYTScraper
from src.google_sheets_manager import GoogleSheetsManager
from src.email_sender import EmailSender
from src.imports import load_dotenv, logging
from dateutil.relativedelta import relativedelta

# Load environment variables from .env file
load_dotenv()

# Configure logging level
logging.basicConfig(level=logging.INFO)


def calculate_date_range(months):
    """
    Calculate the date range based on the given number of months.

    Parameters:
    months (int): Number of months to include in the date range.
                  For example, 0 for the current month, 1 for the current and previous month, etc.

    Returns:
    tuple: A tuple containing the start and end dates in '%m/%d/%Y' format.
           For example, ('04/01/2024', '04/21/2024')

    Raises:
    ValueError: If the input `months` is negative.
    """

    # Check if months is negative
    if months < 0:
        raise ValueError("Months should be a non-negative integer.")

    # Get today's date
    today = datetime.today()

    # Calculate the start date
    start_date = today.replace(day=1)

    # Calculate the end date (today's date)
    end_date = today

    # Adjust the start date based on the input months
    if months > 0 or months > 1:
        # Subtract months from the current month
        start_date -= relativedelta(months=months - 1)

    # Format dates as strings
    start_date_str = start_date.strftime('%m/%d/%Y')
    end_date_str = end_date.strftime('%m/%d/%Y')

    return start_date_str, end_date_str


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
        try:
            start_date, end_date = calculate_date_range(months)
        except ValueError as e:
            print(e)

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
