from .imports import smtplib, MIMEText, MIMEMultipart, logging


class EmailSender:
    """
    A class to send emails using SMTP.

    Attributes:
        None
    """

    @staticmethod
    def send_email(sender_email, receiver_email, app_password, sheet_url):
        """
        Sends an email with the Google Spreadsheet link and GitHub repo link.

        Args:
            sender_email (str): The sender's email address.
            receiver_email (str): The receiver's email address.
            app_password (str): The App Password for the sender's email.
            sheet_url (str): The URL of the Google Spreadsheet.

        Raises:
            Exception: If there's an error during the email sending process.
        """
        try:
            # Define email content
            github_repo_link = "https://github.com/DipNkr/NYT_News_Scraper"
            subject = "The New York Times News Report"
            body = f"""
            Hello,

            Please find the NYT news report below along with the link to the github repo that hosts this code:
            Google Spreadsheet Link: {sheet_url}
            GitHub Repo: {github_repo_link}

            Best regards,
            Team NYT
            """

            # Create a multipart message
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject

            # Add body to email
            msg.attach(MIMEText(body, "plain"))

            # Create SMTP session
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            # Login to the email account using App Password
            server.login(sender_email, app_password)

            # Send email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            logging.info("Email sent successfully!")

        except Exception as e:
            logging.error(f"Error sending email: {e}")
            raise
