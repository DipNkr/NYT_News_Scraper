from .imports import gspread, ServiceAccountCredentials, logging


class GoogleSheetsManager:
    """
    A class to manage Google Sheets operations like initialization and data appending.

    Attributes:
        sheet: Google Sheet instance.
    """

    def __init__(self):
        """
        Initializes the GoogleSheetsManager class and sets up the Google Sheet.

        Raises:
            Exception: If there's an error initializing the Google Sheet.
        """
        try:
            # Define the required OAuth2.0 scopes
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"
            ]

            # Load credentials from the JSON key file
            creds = ServiceAccountCredentials.from_json_keyfile_name("./credentials/credentials.json", scope)

            # Authorize the client using the credentials
            client = gspread.authorize(creds)

            # Open the specific Google Sheet
            self.sheet = client.open("nyt-articles").sheet1

        except Exception as e:
            logging.error(f"Error initializing Google Sheets: {e}")
            raise

    def append_data(self, data):
        """
        Appends the provided data to the Google Sheet.

        Args:
            data (list): A list of dictionaries containing article details.

        Returns:
            str: The URL of the updated Google Sheet.

        Raises:
            Exception: If there's an error during the data appending process.
        """
        try:
            # Clear the existing data in the sheet
            self.sheet.clear()

            # Define the headers
            headers = ["Title", "Date", "Description", "Image Link", "Article Link"]

            # Append the headers to the sheet
            self.sheet.append_row(headers)

            # Append each article's data to the sheet
            for d in data:
                data_row = [d['title'], d['date'], d['description'], d['image'], d['article_link']]
                self.sheet.append_row(data_row)

            # Return the URL of the updated sheet
            return self.sheet.url
        except Exception as e:
            logging.error(f"Error appending row to Google Sheets: {e}")
            raise
