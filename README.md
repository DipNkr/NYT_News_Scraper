# NYT News Scraper

This project is a Python-based web scraper that fetches news articles from The New York Times based on user-defined search criteria and stores the data in a Google Spreadsheet. Additionally, it sends an email report with the Google Spreadsheet link.

## Prerequisites

- Python 3.x installed
- Google Chrome installed (for Selenium WebDriver)
- Gmail account with App Password enabled
- Google Cloud Platform account with Google Sheets API enabled

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/DipNkr/NYT_News_Scraper.git
```

### Navigate to the Project Directory

Navigate to the project directory using the following command:

```
cd NYT_News_Scraper
```

### Install Dependencies

Install the required dependencies using the following command:

```
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the root directory and populate it with the following variables:

```
SEARCH_PHRASE=INDIA
NEWS_SECTION=Arts,World,Food,U.S.,Podcasts
MONTHS=2
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECEIVER_EMAIL=receiver_email@gmail.com
```

Replace `your_email@gmail.com` with your sender email and `your_app_password` with your Gmail App Password.

### Run the Script

To run the script, use the following command:

```
python main.py
```

The script will start fetching news articles from The New York Times based on the provided search criteria, store the data in a Google Spreadsheet, and send an email report with the Google Spreadsheet link.
