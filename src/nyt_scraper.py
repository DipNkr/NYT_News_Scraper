from .imports import *
from src.imports import logging


class NYTScraper:
    """
    A class to interact with The New York Times website to search and scrape news articles.

    Attributes:
        driver: Selenium WebDriver instance.
    """

    def __init__(self):
        """
        Initializes the NYTScraper class and sets up the Chrome WebDriver.

        Raises:
            Exception: If there's an error initializing the Chrome WebDriver.
        """
        try:
            # Initialize Chrome WebDriver
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        except Exception as e:
            logging.error(f"Error initializing Chrome webdriver: {e}")
            raise

    def search_news(self, search_phrase, news_section, start_date, end_date):
        """
        Searches for news articles based on the provided parameters.

        Args:
            search_phrase (str): The search phrase to look for.
            news_section (str): Comma-separated news sections to search within.
            start_date (str): Start date for the news search.
            end_date (str): End date for the news search.

        Raises:
            Exception: If there's an error during the search process.
        """
        try:
            self.driver.get("https://www.nytimes.com/")

            # Enters a phrase in the search field.
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div[2]/div[2]/header/section[1]/div[1]/div/button"))
            ).click()
            search_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div[2]/div[2]/header/section[1]/div[1]/div/div/form/div/input"))
            )
            search_input.send_keys(search_phrase)
            search_input.send_keys(Keys.RETURN)

            # sets the date input for provided months
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/button"))
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/div/ul/li[6]/button"))
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/div/div[2]/div/label[1]/input"))
            ).send_keys(start_date)

            enddate = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[1]/div/div/div/div[2]/div/label[2]/input"))
            )
            enddate.send_keys(end_date)
            enddate.send_keys(Keys.RETURN)

            # selects sections
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div[2]/main/div/div[1]/div[2]/div/div/div[2]/div/div/button"))
            ).click()

            section_values = news_section.split(",")
            wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds for the element to be clickable

            try:
                # Wait for the section elements to be present
                elements = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="css-64f9ga"]/li/label/span')))

                for value in section_values:
                    # Reset the elements to ensure the correct elements are fetched for each value
                    elements = wait.until(
                        EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="css-64f9ga"]/li/label/span')))

                    for element in elements:
                        try:
                            if value in element.text:
                                element.click()
                                # Wait for a short moment to allow the selection to be processed
                                time.sleep(2)

                                # Check if the value is selected
                                selected_elements = self.driver.find_elements(By.XPATH,
                                                                              '//ul[@class="css-64f9ga"]/li/label/span[@aria-checked="true"]')
                                if any(value in elem.text for elem in selected_elements):
                                    break  # Exit the inner loop once the value is selected
                        except StaleElementReferenceException:
                            # Handle the exception by fetching the element again
                            elements = wait.until(EC.presence_of_all_elements_located(
                                (By.XPATH, '//ul[@class="css-64f9ga"]/li/label/span')))
                            break  # Break the inner loop to fetch the updated elements

            except TimeoutException:
                logging.error("Timeout occurred while waiting for the section elements to be clickable")

            # chooses the latest (i.e., newest) news.
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//select/option[@value='newest']"))
            ).click()

            time.sleep(10)

        except Exception as e:
            logging.error(f"Error searching news: {e}")
            raise

    def scrape_articles(self):
        """
        Scrapes the articles from the search results page.

        Returns:
            list: A list of dictionaries containing article details.

        Raises:
            Exception: If there's an error during the scraping process.
        """
        try:
            articles = []

            # Wait for articles to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//li[@class="css-1l4w6pd"]'))
            )

            # Get the HTML content of the page
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find all article list items
            article_elements = soup.find_all('li', class_='css-1l4w6pd')

            for article in article_elements:
                title = article.find('h4', class_='css-2fgx4k').text.strip() if article.find('h4',
                                                                                             class_='css-2fgx4k') else ""
                date = article.find('span', class_='css-17ubb9w').text.strip() if article.find('span',
                                                                                               class_='css-17ubb9w') else ""
                description = article.find('p', class_='css-16nhkrn').text.strip() if article.find('p',
                                                                                                   class_='css-16nhkrn') else ""
                image = article.find('img', class_='css-rq4mmj')['src'] if article.find('img',
                                                                                        class_='css-rq4mmj') else ""
                article_link = "https://www.nytimes.com/" + article.find('a')['href'] if article.find('a') else ""

                articles.append({
                    "title": title,
                    "date": date,
                    "description": description,
                    "image": image,
                    "article_link": article_link
                })

            return articles

        except Exception as e:
            logging.error(f"Error scraping articles: {e}")
            raise

    def close(self):
        """
        Closes the Chrome WebDriver.

        Raises:
            Exception: If there's an error closing the Chrome WebDriver.
        """
        try:
            self.driver.quit()
        except Exception as e:
            logging.error(f"Error closing Chrome webdriver: {e}")
