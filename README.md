This Python script automates the process of extracting contact information and industry details from the Apollo platform using Selenium. 
It is designed to streamline the collection of business data by reading a list of company names from a CSV file and scraping relevant details such as names, positions, emails, and industries.

Key Features:

Utilizes Selenium WebDriver for browser automation with Chrome.
Reads company names from an input CSV file.
Searches for companies on Apollo and navigates to the "People" or "Employees" section.
Filters results based on specific keywords (e.g., Director, Sales).
Extracts data such as name, position, email, and industry details.
Dynamically generates CSS selectors for robust element identification.
Saves the scraped data into a structured CSV file.
Technologies Used:

Python
Selenium
Pandas
Usage Instructions:

Update the Chrome user profile path and CSV file path in the script.
Run the script to initiate automated data scraping.
The output CSV file will contain the collected data.
Prerequisites:

Chrome browser installed with a pre-configured profile.
Python installed with the required libraries (selenium, pandas).
This script is ideal for automating lead generation or data collection tasks involving Apollo's platform.
